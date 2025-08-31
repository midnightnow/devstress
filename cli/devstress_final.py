#!/usr/bin/env python3
"""
DevStress: Simple, local load testing for developers.
A single-file tool that stress tests your API in 60 seconds with zero setup.
"""

import asyncio
import aiohttp
import aiosqlite
import argparse
import json
import time
import sys
from collections import Counter
from typing import Dict, List, Any, Optional
from pathlib import Path

# Default scenario for simple GET requests
DEFAULT_SCENARIO = {
    "steps": [{"method": "GET", "path": ""}],
    "think_time_ms": [100, 500]
}

class DevStressWorker:
    """A single worker that executes HTTP requests."""
    
    def __init__(self, worker_id: int):
        self.worker_id = worker_id
        self.request_count = 0
    
    async def execute_step(self, session: aiohttp.ClientSession, base_url: str, step: Dict) -> Dict:
        """Execute a single HTTP request step."""
        method = step.get("method", "GET")
        path = step.get("path", "")
        url = base_url + path
        body = step.get("body")
        headers = step.get("headers", {})
        
        start = time.monotonic()
        error = None
        status_code = None
        
        try:
            async with session.request(method, url, json=body, headers=headers) as response:
                status_code = response.status
                await response.read()  # Consume response body
        except asyncio.TimeoutError:
            error = "timeout"
        except Exception as e:
            error = str(e)[:50]  # Truncate long error messages
        
        latency_ms = (time.monotonic() - start) * 1000
        self.request_count += 1
        
        return {
            "worker_id": self.worker_id,
            "timestamp": time.time(),
            "latency_ms": latency_ms,
            "status_code": status_code,
            "error": error
        }

class DevStressRunner:
    """Main runner that orchestrates the load test."""
    
    def __init__(self, config: Dict):
        self.target_url = config["target_url"]
        self.duration_s = config["duration_s"]
        self.workers = config["workers"]
        self.scenario = config.get("scenario", DEFAULT_SCENARIO)
        self.config = config
        self.results: List[Dict] = []
        self.db_path = Path.home() / ".devstress" / "history.db"
        self.db_path.parent.mkdir(exist_ok=True)
    
    async def setup_db(self):
        """Create the database table if it doesn't exist."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS test_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    target_url TEXT,
                    duration_s REAL,
                    workers INTEGER,
                    rps REAL,
                    total_requests INTEGER,
                    success_rate REAL,
                    p95_latency_ms REAL
                )
            """)
            await db.commit()
    
    async def worker_loop(self, session: aiohttp.ClientSession, end_time: float):
        """Main loop for a worker - runs until time expires."""
        worker = DevStressWorker(id(asyncio.current_task()))
        
        while time.monotonic() < end_time:
            # Rate limiting logic (if configured)
            if self.config.get('rps'):
                target_interval = self.workers / self.config['rps']
                await asyncio.sleep(target_interval)
            
            # Execute scenario steps
            for step in self.scenario["steps"]:
                if time.monotonic() >= end_time:
                    break
                
                result = await worker.execute_step(session, self.target_url, step)
                self.results.append(result)
                
                # Think time between steps
                if self.scenario.get("think_time_ms"):
                    min_ms, max_ms = self.scenario["think_time_ms"]
                    think_time = (min_ms + (max_ms - min_ms) / 2) / 1000
                    await asyncio.sleep(think_time)
    
    async def run(self):
        """Execute the full load test."""
        print(f"🚀 Starting test: {self.workers} workers for {self.duration_s}s on {self.target_url}")
        await self.setup_db()
        
        connector = aiohttp.TCPConnector(limit=0, limit_per_host=100)
        timeout = aiohttp.ClientTimeout(total=20)
        
        start_time = time.monotonic()
        end_time = start_time + self.duration_s
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            # Create and start all worker tasks
            tasks = [
                asyncio.create_task(self.worker_loop(session, end_time), name=f"worker-{i}")
                for i in range(self.workers)
            ]
            await asyncio.gather(*tasks)
        
        total_time = time.monotonic() - start_time
        await self._record_run(total_time)
        self._print_results(total_time)
        return self._generate_summary(total_time)
    
    async def _record_run(self, actual_duration: float):
        """Save the test results to the database."""
        if not self.results:
            return
        
        success_count = sum(1 for r in self.results if r["error"] is None)
        latencies = sorted([r["latency_ms"] for r in self.results if r["error"] is None])
        p95 = latencies[int(0.95 * len(latencies))] if latencies else 0
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT INTO test_runs 
                (timestamp, target_url, duration_s, workers, rps, total_requests, success_rate, p95_latency_ms)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    time.strftime("%Y-%m-%d %H:%M:%S"),
                    self.target_url,
                    actual_duration,
                    self.workers,
                    self.config.get('rps'),
                    len(self.results),
                    success_count / len(self.results) if self.results else 0,
                    p95
                )
            )
            await db.commit()
    
    def _print_results(self, total_time: float):
        """Print a formatted summary to the console."""
        if not self.results:
            print("❌ No requests were completed.")
            return
        
        status_codes = Counter(r["status_code"] for r in self.results)
        errors = Counter(r["error"] for r in self.results if r["error"])
        latencies = [r["latency_ms"] for r in self.results if r["error"] is None]
        
        if not latencies:
            print("❌ No successful requests.")
            return
        
        latencies_sorted = sorted(latencies)
        
        print("\n" + "="*60)
        print("                         DEVSTRESS REPORT")
        print("="*60)
        print(f"Target URL:         {self.target_url}")
        print(f"Test Duration:      {total_time:.2f}s")
        print(f"Workers:            {self.workers}")
        print(f"Target RPS:         {self.config.get('rps', 'Unlimited')}")
        print(f"Total Requests:     {len(self.results)}")
        print(f"Actual RPS:         {len(self.results)/total_time:.2f}")
        print(f"Success Rate:       {status_codes.get(200, 0)/len(self.results)*100:.1f}%")
        print(f"Status Codes:       {dict(status_codes)}")
        if errors:
            print(f"Errors:             {dict(errors)}")
        if latencies_sorted:
            print(f"P95 Latency:        {latencies_sorted[int(0.95*len(latencies_sorted))]:.2f}ms")
            print(f"P99 Latency:        {latencies_sorted[int(0.99*len(latencies_sorted))]:.2f}ms")
        print("="*60)
    
    def _generate_summary(self, total_time: float) -> Dict[str, Any]:
        """Generate a structured summary for programmatic use."""
        if not self.results:
            return {"error": "no_requests_completed"}
        
        latencies = [r["latency_ms"] for r in self.results if r["error"] is None]
        status_codes = Counter(r["status_code"] for r in self.results)
        success_count = status_codes.get(200, 0)
        
        return {
            "target_url": self.target_url,
            "duration_s": total_time,
            "workers": self.workers,
            "total_requests": len(self.results),
            "rps": len(self.results) / total_time,
            "success_rate": success_count / len(self.results),
            "p95_latency_ms": sorted(latencies)[int(0.95 * len(latencies))] if latencies else 0,
            "p99_latency_ms": sorted(latencies)[int(0.99 * len(latencies))] if latencies else 0,
            "status_codes": dict(status_codes)
        }

# --- CLI Interface ---
async def main():
    parser = argparse.ArgumentParser(description="DevStress: Simple, local load testing.")
    parser.add_argument("url", help="The target URL to test (e.g., https://api.example.com)")
    parser.add_argument("-d", "--duration", type=int, default=30, help="Test duration in seconds (default: 30)")
    parser.add_argument("-w", "--workers", type=int, default=50, help="Number of concurrent workers (default: 50)")
    parser.add_argument("-r", "--rps", type=float, help="Target requests per second (optional rate limiting)")
    parser.add_argument("--scenario", type=str, help="Path to a JSON scenario file")
    
    args = parser.parse_args()
    
    # Load scenario if provided
    scenario = DEFAULT_SCENARIO
    if args.scenario:
        try:
            with open(args.scenario, 'r') as f:
                scenario = json.load(f)
        except Exception as e:
            print(f"❌ Error loading scenario: {e}")
            sys.exit(1)
    
    config = {
        "target_url": args.url,
        "duration_s": args.duration,
        "workers": args.workers,
        "rps": args.rps,
        "scenario": scenario
    }
    
    runner = DevStressRunner(config)
    try:
        summary = await runner.run()
        # Exit with appropriate code for CI/CD
        if summary.get("success_rate", 0) < 0.95:
            sys.exit(1)  # Fail if success rate < 95%
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()