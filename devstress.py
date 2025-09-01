#!/usr/bin/env python3
"""
DevStress - Zero-Config Load Testing for Developers
Load test your API in 30 seconds, no setup required.
"""

import asyncio
import aiohttp
import argparse
import json
import time
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import statistics
from dataclasses import dataclass, field
from datetime import datetime
import psutil

__version__ = "1.0.0"

@dataclass
class TestConfig:
    """Load test configuration"""
    url: str
    users: int = 100
    duration: int = 30
    rps: Optional[int] = None
    scenario: str = "steady"
    timeout: int = 10
    headers: Dict[str, str] = field(default_factory=dict)
    
class SystemResources:
    """Monitor and manage system resources"""
    
    @staticmethod
    def get_capacity() -> Dict:
        """Determine system capacity for load testing"""
        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()
        available_memory_gb = memory.available / (1024**3)
        
        # Conservative estimates based on system resources
        max_users = min(
            cpu_count * 250,  # ~250 concurrent connections per CPU core
            int(available_memory_gb * 500),  # ~500 users per GB of available RAM
            5000  # Hard cap for safety
        )
        
        return {
            'cpu_count': cpu_count,
            'memory_gb': available_memory_gb,
            'max_recommended_users': max_users,
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'memory_percent': memory.percent
        }
    
    @staticmethod
    def optimize_connector(users: int) -> aiohttp.TCPConnector:
        """Create optimized connector based on user count"""
        return aiohttp.TCPConnector(
            limit=min(users * 2, 1000),  # Total connection pool
            limit_per_host=min(users, 500),  # Per-host limit
            ttl_dns_cache=300,
            enable_cleanup_closed=True
        )

class RateLimiter:
    """Token bucket rate limiter for RPS control"""
    
    def __init__(self, rate: float):
        self.rate = rate
        self.tokens = rate
        self.last_update = time.perf_counter()
        self.lock = asyncio.Lock()
    
    async def acquire(self) -> None:
        """Acquire a token, waiting if necessary"""
        async with self.lock:
            while self.tokens < 1:
                now = time.perf_counter()
                elapsed = now - self.last_update
                self.tokens = min(self.rate, self.tokens + elapsed * self.rate)
                self.last_update = now
                
                if self.tokens < 1:
                    sleep_time = (1 - self.tokens) / self.rate
                    await asyncio.sleep(sleep_time)
            
            self.tokens -= 1

class DevStressWorker:
    """Optimized worker for load testing"""
    
    def __init__(self, worker_id: int, session: aiohttp.ClientSession, 
                 rate_limiter: Optional[RateLimiter] = None):
        self.worker_id = worker_id
        self.session = session
        self.rate_limiter = rate_limiter
        self.requests_sent = 0
        self.response_times = []
        self.status_codes = {}
        self.errors = []
        
    async def execute_request(self, url: str, headers: Dict, timeout: int) -> Dict:
        """Execute a single HTTP request"""
        if self.rate_limiter:
            await self.rate_limiter.acquire()
        
        start_time = time.perf_counter()
        
        try:
            async with self.session.get(
                url,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=timeout),
                allow_redirects=True
            ) as response:
                await response.read()
                response_time = (time.perf_counter() - start_time) * 1000
                
                self.requests_sent += 1
                self.response_times.append(response_time)
                self.status_codes[response.status] = self.status_codes.get(response.status, 0) + 1
                
                return {
                    'status': response.status,
                    'response_time': response_time,
                    'success': 200 <= response.status < 400
                }
                
        except asyncio.TimeoutError:
            self.errors.append('timeout')
            return {'status': 'timeout', 'response_time': timeout * 1000, 'success': False}
        except aiohttp.ClientError as e:
            self.errors.append(str(type(e).__name__))
            return {'status': 'error', 'response_time': 0, 'success': False}
        except Exception as e:
            self.errors.append(str(e))
            return {'status': 'error', 'response_time': 0, 'success': False}

class DevStressRunner:
    """Main test runner orchestrating workers"""
    
    def __init__(self):
        self.results_dir = Path.home() / ".devstress"
        self.results_dir.mkdir(exist_ok=True)
        
    def print_banner(self):
        """Print the DevStress banner"""
        print("╔══════════════════════════════════════════════════════╗")
        print("║              🚀 DevStress Load Testing 🚀            ║")
        print("║        Zero-Config Load Testing for Developers       ║")
        print("╚══════════════════════════════════════════════════════╝")
        
    def print_progress(self, elapsed: float, duration: float, requests: int, errors: int):
        """Print real-time progress bar"""
        progress = min(elapsed / duration, 1.0)
        bar_length = 40
        filled = int(bar_length * progress)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        rps = requests / elapsed if elapsed > 0 else 0
        error_rate = (errors / requests * 100) if requests > 0 else 0
        
        print(f"\r[{bar}] {progress*100:.1f}% | "
              f"Requests: {requests:,} | "
              f"RPS: {rps:.1f} | "
              f"Errors: {error_rate:.1f}%", end="", flush=True)
    
    async def run_test(self, config: TestConfig) -> Dict:
        """Execute the load test"""
        self.print_banner()
        
        # System resource check
        resources = SystemResources.get_capacity()
        
        # Optimize user count if needed
        actual_users = config.users
        if config.users > resources['max_recommended_users']:
            actual_users = resources['max_recommended_users']
            print(f"⚠️  Reduced users from {config.users} to {actual_users} (system limit)")
        
        print(f"\n📊 Target URL: {config.url}")
        print(f"👥 Users: {actual_users}")
        print(f"⏱️  Duration: {config.duration}s")
        if config.rps:
            print(f"🎯 Target RPS: {config.rps}")
        print(f"📈 Scenario: {config.scenario}")
        print(f"💻 System: {resources['cpu_count']} CPUs, "
              f"{resources['memory_gb']:.1f}GB available RAM")
        print("\n" + "─" * 60 + "\n")
        
        # Setup rate limiter if RPS is specified
        rate_limiter = RateLimiter(config.rps) if config.rps else None
        
        # Create optimized connector
        connector = SystemResources.optimize_connector(actual_users)
        
        start_time = time.time()
        
        async with aiohttp.ClientSession(connector=connector) as session:
            # Create workers
            workers = [
                DevStressWorker(i, session, rate_limiter) 
                for i in range(actual_users)
            ]
            
            # Execute test scenario
            if config.scenario == "ramp":
                test_task = self._run_ramp_test(workers, config, start_time)
            elif config.scenario == "spike":
                test_task = self._run_spike_test(workers, config, start_time)
            else:  # steady
                test_task = self._run_steady_test(workers, config, start_time)
            
            # Progress monitoring task
            monitor_task = self._monitor_progress(workers, config.duration, start_time)
            
            # Run test and monitoring concurrently
            await asyncio.gather(test_task, monitor_task)
            
            # Calculate results
            results = self._calculate_results(workers, config, start_time)
            
            # Generate report
            self._print_results(results)
            report_path = self._save_report(results)
            
            print(f"\n📄 Full report saved: {report_path}")
            
            return results
    
    async def _run_steady_test(self, workers: List[DevStressWorker], 
                               config: TestConfig, start_time: float):
        """Run steady load test"""
        end_time = start_time + config.duration
        
        async def worker_loop(worker):
            while time.time() < end_time:
                await worker.execute_request(config.url, config.headers, config.timeout)
                await asyncio.sleep(0.001)  # Yield to event loop
        
        await asyncio.gather(*[worker_loop(w) for w in workers])
    
    async def _run_ramp_test(self, workers: List[DevStressWorker], 
                            config: TestConfig, start_time: float):
        """Run ramp-up load test"""
        end_time = start_time + config.duration
        ramp_duration = config.duration * 0.3  # 30% ramp-up
        
        async def worker_loop(worker, delay):
            await asyncio.sleep(delay)
            while time.time() < end_time:
                await worker.execute_request(config.url, config.headers, config.timeout)
                await asyncio.sleep(0.001)
        
        delays = [i * (ramp_duration / len(workers)) for i in range(len(workers))]
        await asyncio.gather(*[worker_loop(w, d) for w, d in zip(workers, delays)])
    
    async def _run_spike_test(self, workers: List[DevStressWorker], 
                             config: TestConfig, start_time: float):
        """Run spike load test"""
        # Spike is just steady with immediate full load
        await self._run_steady_test(workers, config, start_time)
    
    async def _monitor_progress(self, workers: List[DevStressWorker], 
                               duration: float, start_time: float):
        """Monitor and display progress"""
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            total_requests = sum(w.requests_sent for w in workers)
            total_errors = sum(len(w.errors) for w in workers)
            
            self.print_progress(elapsed, duration, total_requests, total_errors)
            await asyncio.sleep(0.5)
        
        # Final update
        elapsed = time.time() - start_time
        total_requests = sum(w.requests_sent for w in workers)
        total_errors = sum(len(w.errors) for w in workers)
        self.print_progress(elapsed, duration, total_requests, total_errors)
        print()  # New line after progress bar
    
    def _calculate_results(self, workers: List[DevStressWorker], 
                          config: TestConfig, start_time: float) -> Dict:
        """Calculate comprehensive test results"""
        # Aggregate data from all workers
        all_response_times = []
        all_status_codes = {}
        all_errors = []
        total_requests = 0
        
        for worker in workers:
            all_response_times.extend(worker.response_times)
            total_requests += worker.requests_sent
            all_errors.extend(worker.errors)
            
            for code, count in worker.status_codes.items():
                all_status_codes[code] = all_status_codes.get(code, 0) + count
        
        # Calculate statistics
        actual_duration = time.time() - start_time
        
        if all_response_times:
            avg_response = statistics.mean(all_response_times)
            median_response = statistics.median(all_response_times)
            p95_response = statistics.quantiles(all_response_times, n=20)[18] if len(all_response_times) > 20 else max(all_response_times)
            p99_response = statistics.quantiles(all_response_times, n=100)[98] if len(all_response_times) > 100 else max(all_response_times)
            min_response = min(all_response_times)
            max_response = max(all_response_times)
        else:
            avg_response = median_response = p95_response = p99_response = min_response = max_response = 0
        
        successful_requests = sum(count for code, count in all_status_codes.items() 
                                 if isinstance(code, int) and 200 <= code < 400)
        
        return {
            'url': config.url,
            'duration': actual_duration,
            'users': config.users,
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'failed_requests': len(all_errors),
            'requests_per_second': total_requests / actual_duration if actual_duration > 0 else 0,
            'avg_response_time': avg_response,
            'median_response_time': median_response,
            'min_response_time': min_response,
            'max_response_time': max_response,
            'p95_response_time': p95_response,
            'p99_response_time': p99_response,
            'status_codes': all_status_codes,
            'error_rate': (len(all_errors) / total_requests * 100) if total_requests > 0 else 0,
            'timestamp': datetime.now().isoformat()
        }
    
    def _print_results(self, results: Dict):
        """Print formatted results to console"""
        print("\n" + "═" * 60)
        print("                    TEST RESULTS")
        print("═" * 60)
        
        print(f"\n📊 Performance Metrics:")
        print(f"  • Total Requests: {results['total_requests']:,}")
        print(f"  • Successful: {results['successful_requests']:,}")
        print(f"  • Failed: {results['failed_requests']:,}")
        print(f"  • Requests/Second: {results['requests_per_second']:.1f}")
        print(f"  • Error Rate: {results['error_rate']:.2f}%")
        
        print(f"\n⏱️  Response Times:")
        print(f"  • Average: {results['avg_response_time']:.0f}ms")
        print(f"  • Median: {results['median_response_time']:.0f}ms")
        print(f"  • Min: {results['min_response_time']:.0f}ms")
        print(f"  • Max: {results['max_response_time']:.0f}ms")
        print(f"  • 95th percentile: {results['p95_response_time']:.0f}ms")
        print(f"  • 99th percentile: {results['p99_response_time']:.0f}ms")
        
        if results['status_codes']:
            print(f"\n📈 Status Code Distribution:")
            for code, count in sorted(results['status_codes'].items()):
                percentage = (count / results['total_requests']) * 100
                print(f"  • {code}: {count:,} ({percentage:.1f}%)")
        
        # Performance verdict
        print("\n" + "─" * 60)
        if results['error_rate'] > 5:
            print("❌ High error rate detected. Service may be struggling.")
        elif results['avg_response_time'] > 2000:
            print("⚠️  Slow response times. Consider optimization.")
        elif results['p95_response_time'] > 5000:
            print("⚠️  High tail latency. Some users experiencing slowness.")
        else:
            print("✅ Performance looks good!")
    
    def _save_report(self, results: Dict) -> str:
        """Save detailed HTML report"""
        report_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevStress Report - {results['timestamp']}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 1rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
        .content {{ padding: 2rem; }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }}
        .metric-card {{
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 0.5rem;
            text-align: center;
            transition: transform 0.3s;
        }}
        .metric-card:hover {{ transform: translateY(-5px); }}
        .metric-value {{ 
            font-size: 2rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 0.5rem;
        }}
        .metric-label {{
            color: #666;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 1px;
        }}
        .status-good {{ color: #10b981; }}
        .status-warning {{ color: #f59e0b; }}
        .status-error {{ color: #ef4444; }}
        .chart-container {{
            margin: 2rem 0;
            position: relative;
            height: 300px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
        }}
        th, td {{
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 2rem;
            text-align: center;
            color: #666;
        }}
        .footer a {{ color: #667eea; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 DevStress Load Test Report</h1>
            <p>{results['url']}</p>
            <p>{results['timestamp']}</p>
        </div>
        
        <div class="content">
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">{results['requests_per_second']:.1f}</div>
                    <div class="metric-label">Requests/Second</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{results['avg_response_time']:.0f}ms</div>
                    <div class="metric-label">Avg Response Time</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value {('status-error' if results['error_rate'] > 5 else 'status-good')}">{results['error_rate']:.1f}%</div>
                    <div class="metric-label">Error Rate</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{results['total_requests']:,}</div>
                    <div class="metric-label">Total Requests</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{results['p95_response_time']:.0f}ms</div>
                    <div class="metric-label">95th Percentile</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{results['p99_response_time']:.0f}ms</div>
                    <div class="metric-label">99th Percentile</div>
                </div>
            </div>
            
            <h2>Response Time Distribution</h2>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value (ms)</th>
                </tr>
                <tr>
                    <td>Minimum</td>
                    <td>{results['min_response_time']:.0f}</td>
                </tr>
                <tr>
                    <td>Median</td>
                    <td>{results['median_response_time']:.0f}</td>
                </tr>
                <tr>
                    <td>Average</td>
                    <td>{results['avg_response_time']:.0f}</td>
                </tr>
                <tr>
                    <td>95th Percentile</td>
                    <td>{results['p95_response_time']:.0f}</td>
                </tr>
                <tr>
                    <td>99th Percentile</td>
                    <td>{results['p99_response_time']:.0f}</td>
                </tr>
                <tr>
                    <td>Maximum</td>
                    <td>{results['max_response_time']:.0f}</td>
                </tr>
            </table>
            
            <h2>Status Code Distribution</h2>
            <table>
                <tr>
                    <th>Status Code</th>
                    <th>Count</th>
                    <th>Percentage</th>
                </tr>
                {''.join(f"<tr><td>{code}</td><td>{count:,}</td><td>{(count/results['total_requests']*100):.1f}%</td></tr>" 
                         for code, count in sorted(results.get('status_codes', {}).items()))}
            </table>
        </div>
        
        <div class="footer">
            <p>Generated by <a href="https://github.com/devstress/devstress">DevStress</a> - Zero-Config Load Testing for Developers</p>
        </div>
    </div>
</body>
</html>
        """
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.results_dir / f"report_{timestamp}.html"
        
        with open(report_path, 'w') as f:
            f.write(report_html)
        
        return str(report_path)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='DevStress - Zero-Config Load Testing for Developers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  devstress https://api.example.com              # Quick test with defaults
  devstress https://api.example.com -u 500 -d 60 # 500 users for 60 seconds
  devstress https://api.example.com --rps 100    # Rate-limited to 100 RPS
  devstress https://api.example.com -s ramp      # Ramp-up scenario
        """
    )
    
    parser.add_argument('url', help='Target URL to test')
    parser.add_argument('-u', '--users', type=int, default=100,
                       help='Number of concurrent users (default: 100)')
    parser.add_argument('-d', '--duration', type=int, default=30,
                       help='Test duration in seconds (default: 30)')
    parser.add_argument('-r', '--rps', type=int,
                       help='Target requests per second (optional)')
    parser.add_argument('-s', '--scenario', choices=['steady', 'ramp', 'spike'],
                       default='steady', help='Load pattern (default: steady)')
    parser.add_argument('-t', '--timeout', type=int, default=10,
                       help='Request timeout in seconds (default: 10)')
    parser.add_argument('-H', '--header', action='append',
                       help='Custom header (format: "Name: Value")')
    parser.add_argument('-v', '--version', action='version',
                       version=f'DevStress {__version__}')
    
    return parser.parse_args()

async def main():
    """Main entry point"""
    args = parse_args()
    
    # Parse headers
    headers = {}
    if args.header:
        for header in args.header:
            if ':' in header:
                name, value = header.split(':', 1)
                headers[name.strip()] = value.strip()
    
    # Create configuration
    config = TestConfig(
        url=args.url,
        users=args.users,
        duration=args.duration,
        rps=args.rps,
        scenario=args.scenario,
        timeout=args.timeout,
        headers=headers
    )
    
    # Run test
    runner = DevStressRunner()
    try:
        results = await runner.run_test(config)
        
        # Exit code based on results
        if results['error_rate'] > 5.0:
            sys.exit(1)  # High error rate
        elif results['avg_response_time'] > 2000:
            sys.exit(2)  # Slow response
        else:
            sys.exit(0)  # Success
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(130)