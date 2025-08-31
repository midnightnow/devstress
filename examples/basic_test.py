#!/usr/bin/env python3
"""
Basic DevStress example - Test a simple API endpoint
"""

import subprocess
import sys

def run_basic_test():
    """Run a basic load test against httpbin.org"""
    
    print("🚀 Running basic DevStress test...")
    print("-" * 50)
    
    # Test httpbin.org (a free testing service)
    result = subprocess.run([
        "python", "../devstress.py",
        "https://httpbin.org/delay/1",
        "--users", "50",
        "--duration", "10"
    ], capture_output=True, text=True)
    
    print(result.stdout)
    
    if result.returncode == 0:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed with issues")
        sys.exit(result.returncode)

if __name__ == "__main__":
    run_basic_test()