"""
Basic tests for DevStress
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from devstress import TestConfig, SystemResources, RateLimiter, DevStressWorker

def test_test_config():
    """Test configuration dataclass"""
    config = TestConfig(
        url="https://example.com",
        users=50,
        duration=10
    )
    assert config.url == "https://example.com"
    assert config.users == 50
    assert config.duration == 10
    assert config.scenario == "steady"
    assert config.timeout == 10

def test_system_resources():
    """Test system resource detection"""
    capacity = SystemResources.get_capacity()
    
    assert 'cpu_count' in capacity
    assert 'memory_gb' in capacity
    assert 'max_recommended_users' in capacity
    assert capacity['cpu_count'] > 0
    assert capacity['memory_gb'] > 0
    assert capacity['max_recommended_users'] > 0

@pytest.mark.asyncio
async def test_rate_limiter():
    """Test rate limiting functionality"""
    rate_limiter = RateLimiter(2)  # 2 requests per second for clearer test
    
    start_time = time.time()
    
    # Try to acquire 5 tokens
    # At 2/sec: first 2 are immediate, then 0.5s, 1s, 1.5s
    for _ in range(5):
        await rate_limiter.acquire()
    
    elapsed = time.time() - start_time
    
    # Should take at least 1.5 seconds for 5 tokens at 2/sec rate
    assert elapsed >= 1.4  # Small buffer for timing variations

@pytest.mark.asyncio
async def test_worker_basic():
    """Test basic worker functionality"""
    mock_session = Mock()
    worker = DevStressWorker(1, mock_session)
    
    assert worker.worker_id == 1
    assert worker.requests_sent == 0
    assert len(worker.response_times) == 0
    assert len(worker.errors) == 0

@pytest.mark.asyncio
async def test_connector_optimization():
    """Test connector optimization based on user count"""
    # Need to run in async context for aiohttp
    connector_10 = SystemResources.optimize_connector(10)
    connector_1000 = SystemResources.optimize_connector(1000)
    
    # Check that limits scale with user count
    assert connector_10.limit <= connector_1000.limit
    assert connector_10._limit_per_host <= connector_1000._limit_per_host
    
    # Clean up
    await connector_10.close()
    await connector_1000.close()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])