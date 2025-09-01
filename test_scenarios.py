#!/usr/bin/env python3
"""
Comprehensive test scenarios for DevStress
"""

import asyncio
import subprocess
import json
import time

def run_test(name, command):
    """Run a test scenario and capture results"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {name}")
    print(f"Command: {command}")
    print('='*60)
    
    start = time.time()
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    duration = time.time() - start
    
    print(f"⏱️  Execution time: {duration:.2f}s")
    print(f"✅ Exit code: {result.returncode}")
    
    if result.returncode != 0:
        print("❌ STDERR:", result.stderr[:500])
    
    # Parse output for metrics
    if "Requests/Second:" in result.stdout:
        lines = result.stdout.split('\n')
        for line in lines:
            if "Requests/Second:" in line or "Error Rate:" in line or "Average:" in line:
                print(f"  📊 {line.strip()}")
    
    return result.returncode == 0

def main():
    """Run all test scenarios"""
    print("🚀 DEVSTRESS COMPREHENSIVE TEST SUITE")
    print("="*60)
    
    tests = [
        # Basic functionality
        ("Version Check", "python3 devstress.py --version"),
        ("Help Display", "python3 devstress.py --help | head -20"),
        
        # Quick tests against httpbin
        ("Minimal Test (10 users, 5 seconds)", 
         "python3 devstress.py https://httpbin.org/get --users 10 --duration 5"),
        
        ("Rate Limited Test (20 RPS)", 
         "python3 devstress.py https://httpbin.org/get --users 50 --duration 5 --rps 20"),
        
        ("Ramp Scenario", 
         "python3 devstress.py https://httpbin.org/get --users 20 --duration 10 --scenario ramp"),
        
        ("Spike Scenario", 
         "python3 devstress.py https://httpbin.org/get --users 30 --duration 5 --scenario spike"),
        
        # Test with headers
        ("Custom Headers", 
         "python3 devstress.py https://httpbin.org/headers --users 10 --duration 5 -H 'X-Test: DevStress' -H 'User-Agent: TestBot'"),
        
        # Test timeout handling
        ("Timeout Handling (short timeout)", 
         "python3 devstress.py https://httpbin.org/delay/3 --users 5 --duration 5 --timeout 2"),
        
        # Test different status codes
        ("404 Response", 
         "python3 devstress.py https://httpbin.org/status/404 --users 10 --duration 5"),
        
        ("Mixed Status Codes", 
         "python3 devstress.py https://httpbin.org/status/200,201,404,500 --users 20 --duration 5"),
        
        # Stress test (higher load)
        ("Higher Load (100 users)", 
         "python3 devstress.py https://httpbin.org/get --users 100 --duration 10"),
    ]
    
    results = []
    for name, command in tests:
        success = run_test(name, command)
        results.append((name, success))
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print(f"\n{'='*60}")
    print("📋 TEST SUMMARY")
    print('='*60)
    
    passed = sum(1 for _, success in results if success)
    failed = len(results) - passed
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n📊 Results: {passed}/{len(results)} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {failed} test(s) failed")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    exit(main())