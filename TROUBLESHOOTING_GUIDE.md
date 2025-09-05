# 🔧 DevStress Troubleshooting & Debugging Guide

## 🎯 Systematic Problem Diagnosis with DevStress

This comprehensive troubleshooting guide provides methodical approaches to identify, analyze, and resolve performance issues using DevStress as your diagnostic tool.

---

## 🔍 Performance Issue Investigation Framework

### 1. The 5-Phase Diagnostic Approach

**Phase 1: Problem Identification**
```bash
# Quick health check to establish baseline
devstress https://api.example.com/health \
  --users 10 --duration 30 \
  --header "X-Diagnostic: baseline-health"
```

**Phase 2: Load Isolation**
```bash
# Isolate the problem with minimal load
devstress https://api.example.com/problematic-endpoint \
  --users 1 --duration 60 \
  --header "X-Diagnostic: single-user-test"
```

**Phase 3: Scaling Analysis**
```bash
# Test scaling behavior
for users in 10 25 50 100; do
  devstress https://api.example.com/problematic-endpoint \
    --users $users --duration 120 \
    --header "X-Diagnostic: scaling-test-${users}" > "diagnostic-${users}users.log"
done
```

**Phase 4: Pattern Analysis**
```bash
# Test different load patterns
devstress https://api.example.com/problematic-endpoint --scenario steady --users 100 --duration 300
devstress https://api.example.com/problematic-endpoint --scenario ramp --users 100 --duration 300  
devstress https://api.example.com/problematic-endpoint --scenario spike --users 100 --duration 300
```

**Phase 5: Root Cause Isolation**
```bash
# Component isolation testing
devstress https://database.api.example.com/query --users 50 --duration 180
devstress https://cache.api.example.com/get --users 50 --duration 180
devstress https://auth.api.example.com/validate --users 50 --duration 180
```

---

## 🐛 Common Performance Issues & Diagnostics

### 1. High Response Times

**Symptom**: Average response times consistently above expected thresholds

**Diagnostic Commands**:
```bash
# Test with different timeout values to identify hanging requests
devstress https://api.example.com/slow-endpoint \
  --users 50 --duration 300 --timeout 5 \
  --header "X-Debug: timeout-analysis-5s"

devstress https://api.example.com/slow-endpoint \
  --users 50 --duration 300 --timeout 30 \
  --header "X-Debug: timeout-analysis-30s"

# Test response time distribution
devstress https://api.example.com/slow-endpoint \
  --users 100 --duration 600 \
  --header "X-Debug: response-distribution" > response-times.log

# Extract detailed timing analysis
grep -E "(Average|Median|95th|99th)" response-times.log
```

**Analysis Script**:
```bash
#!/bin/bash
# response-time-analysis.sh

echo "🔍 Response Time Analysis"

# Test different concurrency levels
concurrency_levels=(1 5 10 25 50 100)

echo "concurrency,avg_response,p95_response,p99_response" > response-analysis.csv

for level in "${concurrency_levels[@]}"; do
  echo "Testing concurrency level: ${level}"
  
  devstress https://api.example.com/endpoint \
    --users $level --duration 180 \
    --header "X-Concurrency-Test: ${level}" > "response-${level}.log"
  
  avg_response=$(grep "Average:" "response-${level}.log" | cut -d: -f2 | tr -d ' ms')
  p95_response=$(grep "95th percentile:" "response-${level}.log" | cut -d: -f2 | tr -d ' ms')
  p99_response=$(grep "99th percentile:" "response-${level}.log" | cut -d: -f2 | tr -d ' ms')
  
  echo "${level},${avg_response},${p95_response},${p99_response}" >> response-analysis.csv
  echo "Level ${level}: ${avg_response}ms avg, ${p95_response}ms P95, ${p99_response}ms P99"
done

echo "🎯 Response Time Pattern Analysis:"
if grep -q "response-analysis.csv" && [ -f response-analysis.csv ]; then
  # Identify if response time increases linearly, exponentially, or plateaus
  python3 -c "
import csv
with open('response-analysis.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)
    
# Simple trend analysis
first_avg = float(data[0]['avg_response'])
last_avg = float(data[-1]['avg_response'])
ratio = last_avg / first_avg

print(f'Response time scaling ratio: {ratio:.2f}x')
if ratio < 2:
    print('✅ Linear scaling - likely CPU/memory bound')
elif ratio < 5:
    print('⚠️ Moderate scaling degradation - check connection pools')  
else:
    print('🚨 Severe scaling degradation - likely database/external service bottleneck')
"
fi
```

### 2. High Error Rates

**Symptom**: Elevated HTTP error responses (4xx/5xx status codes)

**Diagnostic Commands**:
```bash
# Error pattern analysis with different load levels
error_test_levels=(10 25 50 100 200)

echo "load_level,total_requests,errors,error_rate,primary_error_code" > error-analysis.csv

for level in "${error_test_levels[@]}"; do
  echo "Testing error patterns at ${level} users..."
  
  devstress https://api.example.com/endpoint \
    --users $level --duration 180 \
    --header "X-Error-Analysis: level-${level}" > "errors-${level}.log"
  
  total_requests=$(grep "Total Requests:" "errors-${level}.log" | cut -d: -f2 | tr -d ' ')
  failed_requests=$(grep "Failed:" "errors-${level}.log" | cut -d: -f2 | tr -d ' ')
  error_rate=$(grep "Error Rate:" "errors-${level}.log" | cut -d: -f2 | tr -d '% ')
  
  echo "${level},${total_requests},${failed_requests},${error_rate},TBD" >> error-analysis.csv
  echo "Level ${level}: ${error_rate}% error rate (${failed_requests}/${total_requests})"
done

# Identify error rate threshold
echo "🔍 Error Rate Threshold Analysis:"
awk -F, 'NR>1 && $4>1 {print "Error threshold between", prev_level, "and", $1, "users"} {prev_level=$1}' error-analysis.csv
```

**Error Classification Script**:
```bash
#!/bin/bash
# error-classification.sh

echo "🚨 Error Classification Analysis"

# Test specific error conditions
error_scenarios=(
  "rate-limit:429"
  "auth-failure:401" 
  "server-error:500"
  "timeout:408"
  "not-found:404"
)

for scenario in "${error_scenarios[@]}"; do
  IFS=':' read -r error_type expected_code <<< "$scenario"
  echo "Testing ${error_type} scenario..."
  
  devstress https://api.example.com/test/${error_type} \
    --users 100 --duration 120 \
    --header "X-Error-Test: ${error_type}" > "error-${error_type}.log"
  
  # Check if expected error code appears
  if grep -q "${expected_code}:" "error-${error_type}.log"; then
    echo "✅ ${error_type}: Expected error code ${expected_code} detected"
  else
    echo "❌ ${error_type}: Expected error code ${expected_code} NOT detected"
  fi
done
```

### 3. Connection Issues

**Symptom**: Connection timeouts, refused connections, or connection pool exhaustion

**Diagnostic Commands**:
```bash
# Connection pool analysis
connection_tests=(
  "low-concurrency:25:short"
  "medium-concurrency:100:medium" 
  "high-concurrency:500:long"
  "burst-concurrency:1000:short"
)

echo "🔌 Connection Pool Analysis"

for test in "${connection_tests[@]}"; do
  IFS=':' read -r test_name users duration_type <<< "$test"
  
  case $duration_type in
    "short") duration=60 ;;
    "medium") duration=180 ;;  
    "long") duration=600 ;;
  esac
  
  echo "Testing ${test_name}..."
  devstress https://api.example.com/endpoint \
    --users $users --duration $duration \
    --header "X-Connection-Test: ${test_name}" > "conn-${test_name}.log"
  
  # Check for connection-related errors
  if grep -q "Connection" "conn-${test_name}.log"; then
    echo "⚠️ ${test_name}: Connection issues detected"
    grep "Connection" "conn-${test_name}.log"
  else
    echo "✅ ${test_name}: No connection issues"
  fi
done

# TCP connection analysis
echo "🔍 TCP Connection Analysis"
devstress https://api.example.com/endpoint \
  --users 200 --duration 300 \
  --header "X-TCP-Analysis: connection-lifecycle" \
  --timeout 60 > tcp-analysis.log

# Monitor connection states during test
# (This would typically involve system monitoring tools)
echo "Monitor: ss -tunap | grep :443 | wc -l # Active HTTPS connections"
```

### 4. Memory Leaks

**Symptom**: Degrading performance over time, increasing response times in long-running tests

**Diagnostic Commands**:
```bash
# Long-running memory leak detection
echo "🧠 Memory Leak Detection Test"

# Baseline short test
devstress https://api.example.com/endpoint \
  --users 100 --duration 300 \
  --header "X-Memory-Test: baseline-5min" > memory-baseline.log

# Extended test for leak detection
devstress https://api.example.com/endpoint \
  --users 100 --duration 3600 \
  --header "X-Memory-Test: extended-60min" > memory-extended.log

# Compare performance degradation
baseline_p95=$(grep "95th percentile:" memory-baseline.log | cut -d: -f2 | tr -d ' ms')
extended_p95=$(grep "95th percentile:" memory-extended.log | cut -d: -f2 | tr -d ' ms')

if [ $extended_p95 -gt $((baseline_p95 * 150 / 100)) ]; then
  echo "🚨 Potential memory leak detected:"
  echo "Baseline P95: ${baseline_p95}ms"
  echo "Extended P95: ${extended_p95}ms" 
  echo "Degradation: $(((extended_p95 - baseline_p95) * 100 / baseline_p95))%"
else
  echo "✅ No significant memory leak detected"
fi
```

**Memory Leak Analysis Script**:
```bash
#!/bin/bash
# memory-leak-analysis.sh

echo "🔬 Detailed Memory Leak Analysis"

# Run tests at different intervals to track performance degradation
time_intervals=(300 600 1800 3600 7200) # 5min, 10min, 30min, 1hr, 2hr

echo "duration_mins,avg_response,p95_response,p99_response,error_rate" > memory-leak-analysis.csv

for duration in "${time_intervals[@]}"; do
  duration_mins=$((duration / 60))
  echo "Testing ${duration_mins} minute duration..."
  
  devstress https://api.example.com/endpoint \
    --users 50 --duration $duration \
    --header "X-Memory-Leak-Test: ${duration_mins}min" > "memory-${duration_mins}min.log"
  
  avg_response=$(grep "Average:" "memory-${duration_mins}min.log" | cut -d: -f2 | tr -d ' ms')
  p95_response=$(grep "95th percentile:" "memory-${duration_mins}min.log" | cut -d: -f2 | tr -d ' ms')
  p99_response=$(grep "99th percentile:" "memory-${duration_mins}min.log" | cut -d: -f2 | tr -d ' ms')
  error_rate=$(grep "Error Rate:" "memory-${duration_mins}min.log" | cut -d: -f2 | tr -d '% ')
  
  echo "${duration_mins},${avg_response},${p95_response},${p99_response},${error_rate}" >> memory-leak-analysis.csv
  echo "${duration_mins}min: ${avg_response}ms avg, ${p95_response}ms P95, ${error_rate}% errors"
done

# Analyze trend
echo "📈 Memory Leak Trend Analysis:"
python3 -c "
import csv
import numpy as np

with open('memory-leak-analysis.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Calculate trend in P95 response times
durations = [int(row['duration_mins']) for row in data]
p95_times = [float(row['p95_response']) for row in data]

# Simple linear regression
coefficients = np.polyfit(durations, p95_times, 1)
slope = coefficients[0]

print(f'P95 Response Time Trend: {slope:.2f}ms per minute')
if slope > 0.5:
    print('🚨 MEMORY LEAK DETECTED: Significant performance degradation over time')
elif slope > 0.1:
    print('⚠️ MINOR LEAK SUSPECTED: Slight performance degradation')
else:
    print('✅ NO MEMORY LEAK: Stable performance over time')
"
```

---

## 🌊 Traffic Pattern Analysis

### 1. Seasonal Load Pattern Debugging

**Scenario**: Understanding performance during different traffic patterns

```bash
#!/bin/bash
# seasonal-pattern-analysis.sh

echo "📅 Seasonal Traffic Pattern Analysis"

# Simulate different seasonal patterns
seasonal_patterns=(
  "holiday-rush:2000:spike:300:high"
  "back-to-school:800:ramp:1800:medium"
  "summer-lull:200:steady:3600:low"
  "tax-season:1200:ramp:900:medium-high"
)

for pattern in "${seasonal_patterns[@]}"; do
  IFS=':' read -r season users scenario duration intensity <<< "$pattern"
  echo "Testing ${season} pattern (${intensity} intensity)..."
  
  devstress https://api.example.com/endpoint \
    --users $users --scenario $scenario --duration $duration \
    --header "X-Seasonal-Pattern: ${season}" \
    --header "X-Traffic-Intensity: ${intensity}" > "seasonal-${season}.log"
  
  # Analyze seasonal performance
  rps=$(grep "Requests/Second" "seasonal-${season}.log" | cut -d: -f2 | tr -d ' ')
  error_rate=$(grep "Error Rate" "seasonal-${season}.log" | cut -d: -f2 | tr -d '% ')
  p95_latency=$(grep "95th percentile" "seasonal-${season}.log" | cut -d: -f2 | tr -d ' ms')
  
  echo "${season}: ${rps} RPS, ${error_rate}% errors, ${p95_latency}ms P95"
  
  # Identify problematic patterns
  if (( $(echo "$error_rate > 2.0" | bc -l) )); then
    echo "🚨 ${season}: High error rate detected - scaling needed"
  elif [ $p95_latency -gt 3000 ]; then
    echo "⚠️ ${season}: High latency detected - optimization needed"
  else
    echo "✅ ${season}: Performance acceptable"
  fi
done
```

### 2. User Behavior Pattern Analysis

**Scenario**: Testing different user interaction patterns

```bash
#!/bin/bash
# user-behavior-analysis.sh

echo "👤 User Behavior Pattern Analysis"

behavior_patterns=(
  "power-user:heavy-api-usage:50:300"
  "casual-user:light-browsing:200:60"
  "mobile-user:intermittent-sync:500:30"
  "batch-processor:bulk-operations:20:1800"
)

for pattern in "${behavior_patterns[@]}"; do
  IFS=':' read -r user_type behavior users duration <<< "$pattern"
  echo "Testing ${user_type} behavior (${behavior})..."
  
  case $behavior in
    "heavy-api-usage")
      rps=100
      scenario="steady"
      ;;
    "light-browsing")
      rps=10  
      scenario="steady"
      ;;
    "intermittent-sync")
      rps=5
      scenario="spike"
      ;;
    "bulk-operations")
      rps=200
      scenario="ramp"
      ;;
  esac
  
  devstress https://api.example.com/endpoint \
    --users $users --duration $duration --rps $rps --scenario $scenario \
    --header "X-User-Type: ${user_type}" \
    --header "X-Behavior-Pattern: ${behavior}" > "behavior-${user_type}.log"
  
  # Analyze behavior impact
  actual_rps=$(grep "Requests/Second" "behavior-${user_type}.log" | cut -d: -f2 | tr -d ' ')
  avg_response=$(grep "Average:" "behavior-${user_type}.log" | cut -d: -f2 | tr -d ' ms')
  
  echo "${user_type}: ${actual_rps} RPS achieved, ${avg_response}ms avg response"
done
```

---

## 🔧 System Component Isolation

### 1. Database Performance Isolation

**Scenario**: Identifying database-related performance bottlenecks

```bash
#!/bin/bash
# database-isolation-test.sh

echo "🗄️ Database Performance Isolation"

# Test database-light vs database-heavy endpoints
echo "Testing database-light endpoints..."
devstress https://api.example.com/static/config \
  --users 500 --duration 300 \
  --header "X-Database-Usage: none" > db-light.log

echo "Testing database-read endpoints..." 
devstress https://api.example.com/users/profile \
  --users 200 --duration 300 \
  --header "X-Database-Usage: read-only" > db-read.log

echo "Testing database-write endpoints..."
devstress https://api.example.com/users/update \
  --users 50 --duration 300 \
  --header "X-Database-Usage: write-heavy" > db-write.log

echo "Testing complex query endpoints..."
devstress https://api.example.com/analytics/report \
  --users 10 --duration 300 \
  --header "X-Database-Usage: complex-queries" > db-complex.log

# Analyze database impact
echo "📊 Database Impact Analysis:"
db_light_rps=$(grep "Requests/Second" db-light.log | cut -d: -f2 | tr -d ' ')
db_read_rps=$(grep "Requests/Second" db-read.log | cut -d: -f2 | tr -d ' ')
db_write_rps=$(grep "Requests/Second" db-write.log | cut -d: -f2 | tr -d ' ')
db_complex_rps=$(grep "Requests/Second" db-complex.log | cut -d: -f2 | tr -d ' ')

echo "Database-light: ${db_light_rps} RPS"
echo "Database-read: ${db_read_rps} RPS"  
echo "Database-write: ${db_write_rps} RPS"
echo "Complex queries: ${db_complex_rps} RPS"

# Identify database bottlenecks
echo "🎯 Database Bottleneck Analysis:"
if [ $db_write_rps -lt $((db_read_rps / 5)) ]; then
  echo "🚨 Write performance bottleneck detected"
fi

if [ $db_complex_rps -lt $((db_read_rps / 10)) ]; then
  echo "🚨 Complex query bottleneck detected"
fi
```

### 2. Cache Layer Analysis

**Scenario**: Testing cache effectiveness and performance impact

```bash
#!/bin/bash
# cache-analysis.sh

echo "💾 Cache Layer Performance Analysis"

# Test with cache disabled
echo "Testing with cache disabled..."
devstress https://api.example.com/data \
  --users 100 --duration 300 \
  --header "Cache-Control: no-cache" \
  --header "X-Cache-Test: disabled" > cache-disabled.log

# Test with cold cache  
echo "Testing with cold cache..."
# Clear cache first
curl -X POST https://api.example.com/admin/cache/clear \
  -H "Authorization: Bearer ${ADMIN_TOKEN}"

devstress https://api.example.com/data \
  --users 100 --duration 300 \
  --header "X-Cache-Test: cold-cache" > cache-cold.log

# Test with warm cache
echo "Warming cache..."
devstress https://api.example.com/data \
  --users 10 --duration 60 \
  --header "X-Cache-Test: warmup" > /dev/null

echo "Testing with warm cache..."
devstress https://api.example.com/data \
  --users 100 --duration 300 \
  --header "X-Cache-Test: warm-cache" > cache-warm.log

# Analyze cache impact
echo "📊 Cache Performance Analysis:"
no_cache_rps=$(grep "Requests/Second" cache-disabled.log | cut -d: -f2 | tr -d ' ')
cold_cache_rps=$(grep "Requests/Second" cache-cold.log | cut -d: -f2 | tr -d ' ')
warm_cache_rps=$(grep "Requests/Second" cache-warm.log | cut -d: -f2 | tr -d ' ')

no_cache_latency=$(grep "Average:" cache-disabled.log | cut -d: -f2 | tr -d ' ms')
cold_cache_latency=$(grep "Average:" cache-cold.log | cut -d: -f2 | tr -d ' ms')
warm_cache_latency=$(grep "Average:" cache-warm.log | cut -d: -f2 | tr -d ' ms')

echo "No cache: ${no_cache_rps} RPS, ${no_cache_latency}ms avg"
echo "Cold cache: ${cold_cache_rps} RPS, ${cold_cache_latency}ms avg"
echo "Warm cache: ${warm_cache_rps} RPS, ${warm_cache_latency}ms avg"

cache_improvement=$(echo "scale=1; ($warm_cache_rps - $no_cache_rps) / $no_cache_rps * 100" | bc)
echo "Cache improvement: ${cache_improvement}%"
```

### 3. External Service Dependency Analysis

**Scenario**: Identifying performance impact of external service calls

```bash
#!/bin/bash
# external-service-analysis.sh

echo "🌐 External Service Dependency Analysis"

# Test endpoints with different external service dependencies
external_services=(
  "payment-gateway:critical:30s"
  "email-service:optional:10s"
  "analytics-tracker:fire-and-forget:5s"
  "content-cdn:cached:60s"
)

for service in "${external_services[@]}"; do
  IFS=':' read -r service_name criticality timeout <<< "$service"
  echo "Testing ${service_name} dependency (${criticality})..."
  
  # Convert timeout to numeric value  
  timeout_value=$(echo $timeout | tr -d 's')
  
  devstress https://api.example.com/endpoints/with-${service_name} \
    --users 100 --duration 300 --timeout $timeout_value \
    --header "X-External-Service: ${service_name}" \
    --header "X-Service-Criticality: ${criticality}" > "external-${service_name}.log"
  
  # Analyze external service impact
  rps=$(grep "Requests/Second" "external-${service_name}.log" | cut -d: -f2 | tr -d ' ')
  error_rate=$(grep "Error Rate" "external-${service_name}.log" | cut -d: -f2 | tr -d '% ')
  p95_latency=$(grep "95th percentile" "external-${service_name}.log" | cut -d: -f2 | tr -d ' ms')
  
  echo "${service_name}: ${rps} RPS, ${error_rate}% errors, ${p95_latency}ms P95"
  
  # Check for external service issues
  if (( $(echo "$error_rate > 5.0" | bc -l) )); then
    echo "🚨 ${service_name}: High error rate - external service issue detected"
  fi
  
  if [ $p95_latency -gt $((timeout_value * 800)) ]; then # 80% of timeout
    echo "⚠️ ${service_name}: High latency - approaching timeout threshold"
  fi
done
```

---

## 📈 Performance Regression Detection

### 1. Automated Regression Testing

**Scenario**: Comparing performance between application versions

```bash
#!/bin/bash
# performance-regression-detection.sh

echo "📊 Performance Regression Detection"

# Test baseline version
echo "Testing baseline version (v1.0.0)..."
devstress https://v1.api.example.com/endpoint \
  --users 200 --duration 300 \
  --header "X-Version: v1.0.0" \
  --header "X-Regression-Test: baseline" > baseline-performance.log

# Test new version
echo "Testing new version (v1.1.0)..."  
devstress https://v1-1.api.example.com/endpoint \
  --users 200 --duration 300 \
  --header "X-Version: v1.1.0" \
  --header "X-Regression-Test: candidate" > candidate-performance.log

# Compare performance metrics
echo "🔍 Performance Comparison Analysis:"

baseline_rps=$(grep "Requests/Second" baseline-performance.log | cut -d: -f2 | tr -d ' ')
candidate_rps=$(grep "Requests/Second" candidate-performance.log | cut -d: -f2 | tr -d ' ')

baseline_p95=$(grep "95th percentile:" baseline-performance.log | cut -d: -f2 | tr -d ' ms')
candidate_p95=$(grep "95th percentile:" candidate-performance.log | cut -d: -f2 | tr -d ' ms')

baseline_errors=$(grep "Error Rate:" baseline-performance.log | cut -d: -f2 | tr -d '% ')
candidate_errors=$(grep "Error Rate:" candidate-performance.log | cut -d: -f2 | tr -d '% ')

echo "Baseline (v1.0.0): ${baseline_rps} RPS, ${baseline_p95}ms P95, ${baseline_errors}% errors"
echo "Candidate (v1.1.0): ${candidate_rps} RPS, ${candidate_p95}ms P95, ${candidate_errors}% errors"

# Regression analysis
rps_change=$(echo "scale=1; ($candidate_rps - $baseline_rps) / $baseline_rps * 100" | bc)
p95_change=$(echo "scale=1; ($candidate_p95 - $baseline_p95) / $baseline_p95 * 100" | bc)

echo "📈 Performance Changes:"
echo "RPS Change: ${rps_change}%"
echo "P95 Latency Change: ${p95_change}%"

# Regression detection thresholds
REGRESSION_RPS_THRESHOLD=-10    # 10% RPS decrease
REGRESSION_P95_THRESHOLD=20     # 20% P95 increase

if (( $(echo "$rps_change < $REGRESSION_RPS_THRESHOLD" | bc -l) )); then
  echo "🚨 PERFORMANCE REGRESSION DETECTED: Significant RPS decrease"
  exit 1
fi

if (( $(echo "$p95_change > $REGRESSION_P95_THRESHOLD" | bc -l) )); then
  echo "🚨 PERFORMANCE REGRESSION DETECTED: Significant latency increase"  
  exit 1
fi

echo "✅ No significant performance regression detected"
```

### 2. A/B Testing Performance Comparison

**Scenario**: Comparing performance between different feature implementations

```bash
#!/bin/bash
# ab-performance-testing.sh

echo "⚗️ A/B Testing Performance Comparison"

# Test Version A (control)
echo "Testing Version A (control)..."
devstress https://api.example.com/feature \
  --users 200 --duration 600 \
  --header "X-Feature-Flag: version-a" \
  --header "X-AB-Test: control" > version-a-performance.log

# Test Version B (treatment)
echo "Testing Version B (treatment)..."
devstress https://api.example.com/feature \
  --users 200 --duration 600 \
  --header "X-Feature-Flag: version-b" \
  --header "X-AB-Test: treatment" > version-b-performance.log

# Statistical comparison
echo "📊 A/B Performance Statistical Analysis:"

version_a_rps=$(grep "Requests/Second" version-a-performance.log | cut -d: -f2 | tr -d ' ')
version_b_rps=$(grep "Requests/Second" version-b-performance.log | cut -d: -f2 | tr -d ' ')

version_a_p95=$(grep "95th percentile:" version-a-performance.log | cut -d: -f2 | tr -d ' ms')
version_b_p95=$(grep "95th percentile:" version-b-performance.log | cut -d: -f2 | tr -d ' ms')

version_a_errors=$(grep "Error Rate:" version-a-performance.log | cut -d: -f2 | tr -d '% ')
version_b_errors=$(grep "Error Rate:" version-b-performance.log | cut -d: -f2 | tr -d '% ')

echo "Version A: ${version_a_rps} RPS, ${version_a_p95}ms P95, ${version_a_errors}% errors"
echo "Version B: ${version_b_rps} RPS, ${version_b_p95}ms P95, ${version_b_errors}% errors"

# Performance winner determination
rps_improvement=$(echo "scale=1; ($version_b_rps - $version_a_rps) / $version_a_rps * 100" | bc)
latency_improvement=$(echo "scale=1; ($version_a_p95 - $version_b_p95) / $version_a_p95 * 100" | bc)

echo "🏆 A/B Test Results:"
echo "RPS Improvement (B vs A): ${rps_improvement}%"
echo "Latency Improvement (B vs A): ${latency_improvement}%"

if (( $(echo "$rps_improvement > 5 && $latency_improvement > 5" | bc -l) )); then
  echo "🎉 Version B significantly outperforms Version A"
elif (( $(echo "$rps_improvement < -5 || $latency_improvement < -5" | bc -l) )); then
  echo "⚠️ Version A performs better than Version B"
else
  echo "📊 No significant performance difference between versions"
fi
```

---

## 🛠️ Advanced Debugging Techniques

### 1. Circuit Breaker Testing

**Scenario**: Testing circuit breaker behavior under failure conditions

```bash
#!/bin/bash
# circuit-breaker-testing.sh

echo "🔌 Circuit Breaker Testing"

# Phase 1: Normal operation
echo "Phase 1: Testing normal operation..."
devstress https://api.example.com/endpoint \
  --users 100 --duration 180 \
  --header "X-Circuit-Breaker-Test: normal" > circuit-normal.log

# Phase 2: Simulate downstream failure
echo "Phase 2: Simulating downstream service failure..."
curl -X POST https://api.example.com/admin/simulate-failure \
  -H "Authorization: Bearer ${ADMIN_TOKEN}"

devstress https://api.example.com/endpoint \
  --users 100 --duration 180 \
  --header "X-Circuit-Breaker-Test: failure-mode" > circuit-failure.log

# Phase 3: Recovery testing
echo "Phase 3: Testing circuit breaker recovery..."
curl -X POST https://api.example.com/admin/recover-service \
  -H "Authorization: Bearer ${ADMIN_TOKEN}"

devstress https://api.example.com/endpoint \
  --users 100 --duration 180 \
  --header "X-Circuit-Breaker-Test: recovery" > circuit-recovery.log

# Analyze circuit breaker behavior
echo "🔍 Circuit Breaker Analysis:"
normal_errors=$(grep "Error Rate:" circuit-normal.log | cut -d: -f2 | tr -d '% ')
failure_errors=$(grep "Error Rate:" circuit-failure.log | cut -d: -f2 | tr -d '% ')
recovery_errors=$(grep "Error Rate:" circuit-recovery.log | cut -d: -f2 | tr -d '% ')

echo "Normal operation: ${normal_errors}% errors"
echo "Failure mode: ${failure_errors}% errors"
echo "Recovery mode: ${recovery_errors}% errors"

if (( $(echo "$failure_errors < 50" | bc -l) )); then
  echo "✅ Circuit breaker working correctly - limited error propagation"
else
  echo "🚨 Circuit breaker may not be working - high error propagation"
fi
```

### 2. Rate Limiting Validation

**Scenario**: Testing rate limiting implementation and behavior

```bash
#!/bin/bash
# rate-limiting-validation.sh

echo "🚦 Rate Limiting Validation"

# Test different RPS levels to find rate limit threshold
rate_limits=(10 25 50 100 200 500)

echo "target_rps,actual_rps,error_rate,rate_limited" > rate-limit-validation.csv

for target_rps in "${rate_limits[@]}"; do
  echo "Testing ${target_rps} RPS target..."
  
  devstress https://api.example.com/endpoint \
    --users 100 --duration 180 --rps $target_rps \
    --header "X-Rate-Limit-Test: ${target_rps}rps" > "rate-limit-${target_rps}.log"
  
  actual_rps=$(grep "Requests/Second" "rate-limit-${target_rps}.log" | cut -d: -f2 | tr -d ' ')
  error_rate=$(grep "Error Rate" "rate-limit-${target_rps}.log" | cut -d: -f2 | tr -d '% ')
  
  # Check for rate limiting indicators (429 status codes)
  if grep -q "429:" "rate-limit-${target_rps}.log"; then
    rate_limited="YES"
  else
    rate_limited="NO"
  fi
  
  echo "${target_rps},${actual_rps},${error_rate},${rate_limited}" >> rate-limit-validation.csv
  echo "${target_rps} RPS target: ${actual_rps} actual, ${error_rate}% errors, rate limited: ${rate_limited}"
done

echo "🎯 Rate Limit Analysis:"
# Find the rate limit threshold
awk -F, 'NR>1 && $4=="YES" && prev_limited=="NO" {print "Rate limit threshold between", prev_rps, "and", $1, "RPS"} {prev_rps=$1; prev_limited=$4}' rate-limit-validation.csv
```

### 3. Graceful Degradation Testing

**Scenario**: Testing system behavior under partial component failures

```bash
#!/bin/bash
# graceful-degradation-testing.sh

echo "🛡️ Graceful Degradation Testing"

degradation_scenarios=(
  "redis-cache-down"
  "secondary-database-down"
  "recommendation-service-down"
  "image-processing-down"
)

# Baseline performance
echo "Testing baseline (all services up)..."
devstress https://api.example.com/endpoint \
  --users 200 --duration 300 \
  --header "X-Degradation-Test: baseline" > degradation-baseline.log

baseline_rps=$(grep "Requests/Second" degradation-baseline.log | cut -d: -f2 | tr -d ' ')
baseline_p95=$(grep "95th percentile:" degradation-baseline.log | cut -d: -f2 | tr -d ' ms')

echo "Baseline: ${baseline_rps} RPS, ${baseline_p95}ms P95"

# Test each degradation scenario
for scenario in "${degradation_scenarios[@]}"; do
  echo "Testing degradation scenario: ${scenario}..."
  
  # Simulate service failure
  curl -X POST "https://api.example.com/admin/simulate-failure/${scenario}" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}"
  
  devstress https://api.example.com/endpoint \
    --users 200 --duration 300 \
    --header "X-Degradation-Test: ${scenario}" > "degradation-${scenario}.log"
  
  # Restore service
  curl -X POST "https://api.example.com/admin/restore/${scenario}" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}"
  
  # Analyze degradation impact
  degraded_rps=$(grep "Requests/Second" "degradation-${scenario}.log" | cut -d: -f2 | tr -d ' ')
  degraded_p95=$(grep "95th percentile:" "degradation-${scenario}.log" | cut -d: -f2 | tr -d ' ms')
  degraded_errors=$(grep "Error Rate:" "degradation-${scenario}.log" | cut -d: -f2 | tr -d '% ')
  
  rps_impact=$(echo "scale=1; ($degraded_rps - $baseline_rps) / $baseline_rps * 100" | bc)
  p95_impact=$(echo "scale=1; ($degraded_p95 - $baseline_p95) / $baseline_p95 * 100" | bc)
  
  echo "${scenario}: ${degraded_rps} RPS (${rps_impact}%), ${degraded_p95}ms P95 (${p95_impact}%), ${degraded_errors}% errors"
  
  # Evaluate graceful degradation
  if (( $(echo "$degraded_errors < 1.0" | bc -l) )) && (( $(echo "$rps_impact > -25" | bc -l) )); then
    echo "✅ Graceful degradation working for ${scenario}"
  else
    echo "🚨 Poor degradation handling for ${scenario}"
  fi
done
```

---

## 📋 Troubleshooting Checklist

### Performance Issue Triage Checklist

```bash
# 1. Basic Health Check
devstress https://api.example.com/health --users 1 --duration 30

# 2. Load Scaling Test
for users in 10 25 50 100; do
  devstress https://api.example.com/endpoint --users $users --duration 120
done

# 3. Component Isolation
devstress https://database.api.example.com/query --users 50 --duration 180
devstress https://cache.api.example.com/get --users 50 --duration 180
devstress https://external.api.example.com/call --users 50 --duration 180

# 4. Error Pattern Analysis
devstress https://api.example.com/endpoint --users 100 --duration 300 --timeout 10
devstress https://api.example.com/endpoint --users 200 --duration 300 --timeout 10

# 5. Extended Monitoring
devstress https://api.example.com/endpoint --users 100 --duration 3600 # 1 hour test
```

### Common Performance Anti-Patterns

```bash
# ❌ N+1 Query Problem Detection
devstress https://api.example.com/posts-with-comments --users 100 --duration 300
# Look for: Linear increase in response time with user count

# ❌ Connection Pool Exhaustion
devstress https://api.example.com/database-heavy --users 500 --duration 300
# Look for: Sudden error rate spike at specific user count

# ❌ Memory Leak Detection  
devstress https://api.example.com/endpoint --users 50 --duration 7200
# Look for: Gradually increasing response times over duration

# ❌ Inefficient Caching
devstress https://api.example.com/cached-data --users 200 --duration 300
# Look for: High response times despite caching layer
```

---

**🎯 This comprehensive troubleshooting guide provides systematic approaches to diagnose and resolve performance issues using DevStress. Each technique represents proven debugging patterns used by performance engineers to identify root causes and optimize system behavior.**

**🔧 Ready to debug your performance issues? Start with the diagnostic framework and apply the specific techniques most relevant to your symptoms!**

```bash
pip install devstress
# Begin your performance debugging journey!
```