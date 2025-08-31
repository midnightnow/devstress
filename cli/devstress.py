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
from pathlib import Path
from typing import Dict, List, Optional
import aiosqlite
import psutil
from dataclasses import dataclass
from datetime import datetime
import statistics

@dataclass
class TestConfig:
    """Load test configuration"""
    url: str
    users: int = 100
    duration: int = 30
    scenario: str = "steady"  # steady, spike, ramp, soak
    timeout: int = 10
    headers: Dict[str, str] = None

class DevStressAgent:
    """Optimized load testing agent"""
    
    def __init__(self, agent_id: int, session: aiohttp.ClientSession):
        self.agent_id = agent_id
        self.session = session
        self.requests_sent = 0
        self.response_times = []
        self.errors = 0
        
    async def execute_request(self, url: str, headers: Dict[str, str] = None) -> Dict:
        """Execute single HTTP request with optimal error handling"""
        start_time = time.perf_counter()
        
        try:
            async with self.session.get(
                url, 
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                await response.read()  # Consume response body
                response_time = (time.perf_counter() - start_time) * 1000
                
                self.requests_sent += 1
                self.response_times.append(response_time)
                
                if response.status >= 400:
                    self.errors += 1
                
                return {
                    'agent_id': self.agent_id,
                    'status_code': response.status,
                    'response_time_ms': response_time,
                    'success': response.status < 400
                }
                
        except asyncio.TimeoutError:
            self.errors += 1
            response_time = (time.perf_counter() - start_time) * 1000
            return {
                'agent_id': self.agent_id,
                'status_code': 'timeout',
                'response_time_ms': response_time,
                'success': False
            }
        except Exception as e:
            self.errors += 1
            response_time = (time.perf_counter() - start_time) * 1000
            return {
                'agent_id': self.agent_id,
                'status_code': 'error',
                'response_time_ms': response_time,
                'success': False,
                'error': str(e)
            }

class DevStressEngine:
    """Main load testing engine with async optimizations"""
    
    def __init__(self):
        self.results_dir = Path.home() / ".devstress" / "results"
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.results_dir / "history.db"
        
    async def init_database(self):
        """Initialize async SQLite database"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS tests (
                    id TEXT PRIMARY KEY,
                    url TEXT,
                    users INTEGER,
                    duration INTEGER,
                    scenario TEXT,
                    timestamp REAL,
                    total_requests INTEGER,
                    successful_requests INTEGER,
                    failed_requests INTEGER,
                    avg_response_time_ms REAL,
                    p95_response_time_ms REAL,
                    p99_response_time_ms REAL,
                    requests_per_second REAL,
                    error_rate_percent REAL
                )
            """)
            await db.commit()
    
    def check_system_resources(self) -> Dict:
        """Check system resources with smart scaling"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        # Smart user count recommendation
        available_memory_gb = memory.available / (1024**3)
        recommended_max_users = min(2000, int(available_memory_gb * 500))
        
        return {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'recommended_max_users': recommended_max_users,
            'system_ready': cpu_percent < 80 and memory.percent < 80
        }
    
    async def run_load_test(self, config: TestConfig) -> Dict:
        """Run optimized load test with async database operations"""
        print(f"🚀 DevStress Load Test Starting")
        print(f"📊 Target: {config.url}")
        print(f"👥 Users: {config.users}")
        print(f"⏱️  Duration: {config.duration}s")
        print(f"📈 Scenario: {config.scenario}")
        print("-" * 50)
        
        # System resource check
        system_status = self.check_system_resources()
        if not system_status['system_ready']:
            print(f"⚠️  Warning: High system load detected")
            
        # Optimize user count based on system resources
        optimized_users = min(config.users, system_status['recommended_max_users'])
        if optimized_users < config.users:
            print(f"📉 Reduced users from {config.users} to {optimized_users} (system optimization)")
        
        test_id = f"devstress_{int(time.time())}"
        await self.init_database()
        
        # Configure high-performance connection pool
        connector = aiohttp.TCPConnector(
            limit=optimized_users + 50,
            limit_per_host=optimized_users,
            keepalive_timeout=60,
            enable_cleanup_closed=True
        )
        
        try:
            async with aiohttp.ClientSession(
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=config.timeout)
            ) as session:
                # Create agents
                agents = [DevStressAgent(i, session) for i in range(optimized_users)]
                
                # Execute test based on scenario
                start_time = time.time()
                if config.scenario == "spike":
                    await self._execute_spike_test(agents, config, start_time)
                elif config.scenario == "ramp":
                    await self._execute_ramp_test(agents, config, start_time)
                else:  # steady (default)
                    await self._execute_steady_test(agents, config, start_time)
                
                # Calculate final metrics
                results = await self._calculate_results(agents, config, test_id, start_time)
                
                # Store results in database
                await self._store_results(results)
                
                # Generate report
                report_path = await self._generate_report(results)
                
                print(f"\n✅ Test Completed!")
                print(f"📊 Report: {report_path}")
                print(f"📈 {results['requests_per_second']:.1f} RPS")
                print(f"⚡ {results['avg_response_time_ms']:.0f}ms avg response")
                print(f"❌ {results['error_rate_percent']:.1f}% error rate")
                
                return results
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
            raise
    
    async def _execute_steady_test(self, agents: List[DevStressAgent], config: TestConfig, start_time: float):
        """Execute steady load test with optimal async pattern"""
        end_time = start_time + config.duration
        
        # Create continuous task streams for each agent
        async def agent_task_stream(agent):
            while time.time() < end_time:
                await agent.execute_request(config.url, config.headers)
                await asyncio.sleep(0.001)  # Minimal delay for event loop yielding
        
        # Run all agents concurrently
        await asyncio.gather(*[agent_task_stream(agent) for agent in agents])
    
    async def _execute_spike_test(self, agents: List[DevStressAgent], config: TestConfig, start_time: float):
        """Execute spike test - immediate full load"""
        await self._execute_steady_test(agents, config, start_time)
    
    async def _execute_ramp_test(self, agents: List[DevStressAgent], config: TestConfig, start_time: float):
        """Execute ramp test - gradual load increase"""
        end_time = start_time + config.duration
        ramp_duration = config.duration * 0.3  # 30% for ramp up
        
        async def ramped_agent_stream(agent, delay_factor):
            await asyncio.sleep(delay_factor)  # Stagger agent start times
            while time.time() < end_time:
                await agent.execute_request(config.url, config.headers)
                await asyncio.sleep(0.001)
        
        # Stagger agent starts over ramp period
        delay_increment = ramp_duration / len(agents)
        tasks = [
            ramped_agent_stream(agent, i * delay_increment) 
            for i, agent in enumerate(agents)
        ]
        
        await asyncio.gather(*tasks)
    
    async def _calculate_results(self, agents: List[DevStressAgent], config: TestConfig, 
                               test_id: str, start_time: float) -> Dict:
        """Calculate comprehensive test results"""
        total_requests = sum(agent.requests_sent for agent in agents)
        total_errors = sum(agent.errors for agent in agents)
        
        # Collect all response times
        all_response_times = []
        for agent in agents:
            all_response_times.extend(agent.response_times)
        
        if all_response_times:
            avg_response_time = statistics.mean(all_response_times)
            p95_response_time = statistics.quantiles(all_response_times, n=20)[18]  # 95th percentile
            p99_response_time = statistics.quantiles(all_response_times, n=100)[98]  # 99th percentile
        else:
            avg_response_time = p95_response_time = p99_response_time = 0
        
        actual_duration = time.time() - start_time
        rps = total_requests / actual_duration if actual_duration > 0 else 0
        error_rate = (total_errors / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'test_id': test_id,
            'url': config.url,
            'users': config.users,
            'duration': config.duration,
            'scenario': config.scenario,
            'timestamp': start_time,
            'total_requests': total_requests,
            'successful_requests': total_requests - total_errors,
            'failed_requests': total_errors,
            'avg_response_time_ms': avg_response_time,
            'p95_response_time_ms': p95_response_time,
            'p99_response_time_ms': p99_response_time,
            'requests_per_second': rps,
            'error_rate_percent': error_rate,
            'actual_duration': actual_duration
        }
    
    async def _store_results(self, results: Dict):
        """Store results in async database"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO tests (
                    id, url, users, duration, scenario, timestamp,
                    total_requests, successful_requests, failed_requests,
                    avg_response_time_ms, p95_response_time_ms, p99_response_time_ms,
                    requests_per_second, error_rate_percent
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                results['test_id'], results['url'], results['users'], results['duration'],
                results['scenario'], results['timestamp'], results['total_requests'],
                results['successful_requests'], results['failed_requests'],
                results['avg_response_time_ms'], results['p95_response_time_ms'],
                results['p99_response_time_ms'], results['requests_per_second'],
                results['error_rate_percent']
            ))
            await db.commit()
    
    async def _generate_report(self, results: Dict) -> str:
        """Generate HTML report with charts"""
        report_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevStress Test Report - {results['test_id']}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #333; }}
        .metric-label {{ color: #666; text-transform: uppercase; font-size: 0.9em; }}
        .chart-container {{ width: 100%; height: 400px; margin: 30px 0; }}
        .footer {{ color: #666; text-align: center; margin-top: 40px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 DevStress Load Test Report</h1>
        <p>Target: <strong>{results['url']}</strong></p>
        <p>Test ID: {results['test_id']} | {datetime.fromtimestamp(results['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="metrics">
        <div class="metric">
            <div class="metric-value">{results['requests_per_second']:.1f}</div>
            <div class="metric-label">Requests/Second</div>
        </div>
        <div class="metric">
            <div class="metric-value">{results['avg_response_time_ms']:.0f}ms</div>
            <div class="metric-label">Avg Response Time</div>
        </div>
        <div class="metric">
            <div class="metric-value">{results['error_rate_percent']:.1f}%</div>
            <div class="metric-label">Error Rate</div>
        </div>
        <div class="metric">
            <div class="metric-value">{results['total_requests']:,}</div>
            <div class="metric-label">Total Requests</div>
        </div>
        <div class="metric">
            <div class="metric-value">{results['p95_response_time_ms']:.0f}ms</div>
            <div class="metric-label">95th Percentile</div>
        </div>
        <div class="metric">
            <div class="metric-value">{results['users']}</div>
            <div class="metric-label">Concurrent Users</div>
        </div>
    </div>
    
    <div class="footer">
        <p>Generated by DevStress - Zero-Config Load Testing</p>
        <p>Visit <a href="https://devstress.com">devstress.com</a> for documentation and support</p>
    </div>
</body>
</html>
        """
        
        report_path = self.results_dir / f"{results['test_id']}_report.html"
        with open(report_path, 'w') as f:
            f.write(report_html)
        
        return str(report_path)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='DevStress - Zero-Config Load Testing for Developers'
    )
    parser.add_argument('url', help='Target URL to test')
    parser.add_argument('--users', '-u', type=int, default=100, 
                       help='Number of concurrent users (default: 100)')
    parser.add_argument('--duration', '-d', type=int, default=30,
                       help='Test duration in seconds (default: 30)')
    parser.add_argument('--scenario', '-s', choices=['steady', 'spike', 'ramp'], 
                       default='steady', help='Load pattern (default: steady)')
    parser.add_argument('--timeout', '-t', type=int, default=10,
                       help='Request timeout in seconds (default: 10)')
    parser.add_argument('--header', action='append', 
                       help='Add custom header (format: "Name: Value")')
    
    return parser.parse_args()

async def main():
    """Main CLI entry point"""
    args = parse_args()
    
    # Parse headers
    headers = {}
    if args.header:
        for header in args.header:
            if ':' in header:
                name, value = header.split(':', 1)
                headers[name.strip()] = value.strip()
    
    # Create test configuration
    config = TestConfig(
        url=args.url,
        users=args.users,
        duration=args.duration,
        scenario=args.scenario,
        timeout=args.timeout,
        headers=headers if headers else None
    )
    
    # Run load test
    engine = DevStressEngine()
    try:
        results = await engine.run_load_test(config)
        
        # Exit with appropriate code for CI/CD
        if results['error_rate_percent'] > 5.0:
            print(f"❌ Test failed: Error rate {results['error_rate_percent']:.1f}% exceeds 5% threshold")
            sys.exit(1)
        elif results['avg_response_time_ms'] > 2000:
            print(f"❌ Test failed: Average response time {results['avg_response_time_ms']:.0f}ms exceeds 2000ms threshold")
            sys.exit(1)
        else:
            print(f"✅ Test passed: Performance within acceptable limits")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print(f"\n⚠️  Test interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n⚠️  Interrupted")
        sys.exit(130)