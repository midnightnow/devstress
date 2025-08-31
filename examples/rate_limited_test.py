#!/usr/bin/env python3
"""
Rate-limited DevStress example - Control requests per second
"""

import subprocess

def run_rate_limited_test():
    """Run a rate-limited test to avoid overwhelming the server"""
    
    print("🎯 Running rate-limited DevStress test...")
    print("Limiting to 50 requests per second")
    print("-" * 50)
    
    # Test with controlled RPS
    result = subprocess.run([
        "python", "../devstress.py",
        "https://httpbin.org/get",
        "--users", "100",
        "--duration", "20",
        "--rps", "50"  # Limit to 50 requests per second
    ], capture_output=True, text=True)
    
    print(result.stdout)

if __name__ == "__main__":
    run_rate_limited_test()