#!/usr/bin/env python3
"""
Performance benchmark for DevStress
Compare against other tools and measure limits
"""

import asyncio
import time
import subprocess
import psutil
import json

def measure_performance():
    """Measure DevStress performance capabilities"""
    
    print("🏎️  DEVSTRESS PERFORMANCE BENCHMARK")
    print("="*60)
    
    # System info
    print("\n📊 System Information:")
    print(f"  • CPUs: {psutil.cpu_count()}")
    print(f"  • RAM: {psutil.virtual_memory().total / (1024**3):.1f} GB")
    print(f"  • Available RAM: {psutil.virtual_memory().available / (1024**3):.1f} GB")
    print(f"  • CPU Usage: {psutil.cpu_percent(interval=1)}%")
    
    benchmarks = []
    
    # Test 1: Maximum RPS
    print("\n🔥 Test 1: Maximum Requests Per Second")
    print("-" * 40)
    
    test_configs = [
        (10, 5, None, "10 users, no limit"),
        (50, 5, None, "50 users, no limit"),
        (100, 5, None, "100 users, no limit"),
        (200, 5, None, "200 users, no limit"),
    ]
    
    for users, duration, rps, desc in test_configs:
        print(f"\n📈 Testing: {desc}")
        
        rps_arg = f"--rps {rps}" if rps else ""
        cmd = f"python3 devstress.py https://httpbin.org/get --users {users} --duration {duration} {rps_arg}"
        
        # Monitor system during test
        cpu_before = psutil.cpu_percent(interval=0.1)
        mem_before = psutil.virtual_memory().percent
        
        start = time.time()
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        elapsed = time.time() - start
        
        cpu_after = psutil.cpu_percent(interval=0.1)
        mem_after = psutil.virtual_memory().percent
        
        # Parse results
        if "Requests/Second:" in result.stdout:
            lines = result.stdout.split('\n')
            for line in lines:
                if "Requests/Second:" in line:
                    rps_achieved = float(line.split(':')[1].strip())
                    print(f"  ✅ RPS Achieved: {rps_achieved:.1f}")
                    
                    benchmarks.append({
                        'test': desc,
                        'users': users,
                        'rps': rps_achieved,
                        'cpu_delta': cpu_after - cpu_before,
                        'mem_delta': mem_after - mem_before
                    })
                    break
        
        print(f"  💻 CPU Impact: {cpu_after - cpu_before:+.1f}%")
        print(f"  🧠 Memory Impact: {mem_after - mem_before:+.1f}%")
        
        time.sleep(2)  # Cool down between tests
    
    # Test 2: Response time under load
    print("\n⏱️  Test 2: Response Time Under Load")
    print("-" * 40)
    
    print("Testing response time consistency...")
    cmd = "python3 devstress.py https://httpbin.org/get --users 50 --duration 10"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if "Average:" in result.stdout and "95th percentile:" in result.stdout:
        lines = result.stdout.split('\n')
        for line in lines:
            if "Average:" in line or "95th percentile:" in line or "99th percentile:" in line:
                print(f"  {line.strip()}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 BENCHMARK SUMMARY")
    print("="*60)
    
    if benchmarks:
        max_rps = max(b['rps'] for b in benchmarks)
        best_config = next(b for b in benchmarks if b['rps'] == max_rps)
        
        print(f"\n🏆 Best Performance:")
        print(f"  • Configuration: {best_config['test']}")
        print(f"  • Max RPS: {best_config['rps']:.1f}")
        print(f"  • CPU Usage: {best_config['cpu_delta']:.1f}%")
        print(f"  • Memory Usage: {best_config['mem_delta']:.1f}%")
        
        print(f"\n📈 Scaling Analysis:")
        for b in benchmarks:
            efficiency = b['rps'] / b['users'] if b['users'] > 0 else 0
            print(f"  • {b['users']} users: {b['rps']:.1f} RPS ({efficiency:.2f} RPS/user)")
    
    # Comparison with other tools
    print("\n🔄 Comparison with Other Tools:")
    print("  • curl loop: ~1-5 RPS (sequential)")
    print(f"  • DevStress: {max_rps:.1f} RPS (concurrent)")
    print(f"  • Improvement: {max_rps/5:.0f}x faster than curl")
    
    print("\n✅ Benchmark Complete!")

if __name__ == "__main__":
    measure_performance()