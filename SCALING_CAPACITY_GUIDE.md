# 📈 DevStress Scaling & Capacity Planning Guide

## 🎯 Strategic Capacity Planning with DevStress

This comprehensive guide demonstrates how to use DevStress for strategic capacity planning, scaling analysis, and infrastructure optimization across different growth scenarios and business requirements.

---

## 🏗️ Infrastructure Scaling Strategies

### 1. Horizontal Scaling Analysis

**Scenario**: Determining when and how to scale horizontally across multiple instances.

```bash
#!/bin/bash
# horizontal-scaling-analysis.sh

echo "🏗️ Horizontal Scaling Analysis"

# Test single instance capacity
echo "Testing single instance baseline..."
devstress https://single.api.example.com/endpoint \
  --users 500 --duration 300 --rps 200 \
  --header "X-Instance-Count: 1" > single-instance.log

# Test dual instance setup  
echo "Testing dual instance configuration..."
devstress https://dual.api.example.com/endpoint \
  --users 1000 --duration 300 --rps 400 \
  --header "X-Instance-Count: 2" > dual-instance.log

# Test quad instance setup
echo "Testing quad instance configuration..."
devstress https://quad.api.example.com/endpoint \
  --users 2000 --duration 300 --rps 800 \
  --header "X-Instance-Count: 4" > quad-instance.log

# Analyze scaling efficiency
echo "📊 Scaling Efficiency Analysis:"
single_rps=$(grep "Requests/Second" single-instance.log | cut -d: -f2 | tr -d ' ')
dual_rps=$(grep "Requests/Second" dual-instance.log | cut -d: -f2 | tr -d ' ')
quad_rps=$(grep "Requests/Second" quad-instance.log | cut -d: -f2 | tr -d ' ')

echo "Single instance: ${single_rps} RPS"
echo "Dual instance: ${dual_rps} RPS (efficiency: $(echo "scale=2; $dual_rps / $single_rps / 2 * 100" | bc)%)"
echo "Quad instance: ${quad_rps} RPS (efficiency: $(echo "scale=2; $quad_rps / $single_rps / 4 * 100" | bc)%)"
```

### 2. Vertical Scaling Optimization

**Scenario**: Testing performance improvements with increased server resources.

```bash
#!/bin/bash  
# vertical-scaling-test.sh

server_configs=(
  "small:2cpu-4gb"
  "medium:4cpu-8gb" 
  "large:8cpu-16gb"
  "xlarge:16cpu-32gb"
)

for config in "${server_configs[@]}"; do
  IFS=':' read -r size spec <<< "$config"
  echo "Testing ${size} server (${spec})..."
  
  devstress https://${size}.api.example.com/endpoint \
    --users 1000 --duration 300 \
    --header "X-Server-Config: ${spec}" \
    --header "X-Test-Type: vertical-scaling" > "vertical-${size}.log"
  
  # Extract performance metrics
  rps=$(grep "Requests/Second" "vertical-${size}.log" | cut -d: -f2 | tr -d ' ')
  avg_response=$(grep "Average:" "vertical-${size}.log" | cut -d: -f2 | tr -d ' ms')
  p95_response=$(grep "95th percentile:" "vertical-${size}.log" | cut -d: -f2 | tr -d ' ms')
  
  echo "${size}: ${rps} RPS, ${avg_response}ms avg, ${p95_response}ms P95"
done
```

### 3. Auto-Scaling Trigger Testing

**Scenario**: Testing auto-scaling policies and response times.

```bash
#!/bin/bash
# auto-scaling-validation.sh

echo "🚀 Auto-Scaling Trigger Validation"

# Test gradual load increase to trigger scaling
echo "Phase 1: Gradual load increase..."
devstress https://autoscale.api.example.com/endpoint \
  --users 100 --scenario ramp --duration 600 \
  --header "X-Scaling-Test: gradual-trigger" &

GRADUAL_PID=$!

# Test sudden spike to trigger rapid scaling
sleep 120
echo "Phase 2: Sudden spike trigger..."
devstress https://autoscale.api.example.com/endpoint \
  --users 1000 --scenario spike --duration 300 \
  --header "X-Scaling-Test: spike-trigger" &

SPIKE_PID=$!

# Monitor scaling events during tests
echo "Phase 3: Monitoring scaling response..."
for i in {1..10}; do
  current_time=$(date '+%Y-%m-%d %H:%M:%S')
  instance_count=$(curl -s https://autoscale.api.example.com/admin/instances | jq '.count')
  echo "${current_time}: ${instance_count} instances running"
  sleep 30
done

wait $GRADUAL_PID $SPIKE_PID
echo "✅ Auto-scaling validation complete"
```

### 4. Database Scaling Impact Analysis

**Scenario**: Testing how database scaling affects application performance.

```bash
#!/bin/bash
# database-scaling-impact.sh

database_tiers=(
  "micro:1cpu-1gb-10iops"
  "small:2cpu-4gb-100iops"
  "medium:4cpu-8gb-1000iops"
  "large:8cpu-16gb-10000iops"
)

for tier in "${database_tiers[@]}"; do
  IFS=':' read -r size spec <<< "$tier"
  echo "Testing with ${size} database tier..."
  
  # Test database-heavy endpoint
  devstress https://api.example.com/database-intensive \
    --users 200 --duration 300 --rps 100 \
    --header "X-DB-Tier: ${size}" \
    --header "X-DB-Spec: ${spec}" \
    --timeout 30 > "db-scaling-${size}.log"
  
  # Analyze database impact on performance
  avg_response=$(grep "Average:" "db-scaling-${size}.log" | cut -d: -f2)
  p95_response=$(grep "95th percentile:" "db-scaling-${size}.log" | cut -d: -f2)
  error_rate=$(grep "Error Rate:" "db-scaling-${size}.log" | cut -d: -f2)
  
  echo "DB ${size}: ${avg_response} avg, ${p95_response} P95, ${error_rate} errors"
done
```

---

## 📊 Capacity Planning Models

### 1. Growth Projection Testing

**Scenario**: Testing system capacity against projected user growth.

```bash
#!/bin/bash
# growth-projection-testing.sh

echo "📈 Growth Projection Capacity Testing"

# Current user base simulation
current_users=1000
growth_rate=1.5 # 50% growth per quarter

quarters=("Q1" "Q2" "Q3" "Q4")
projected_users=$current_users

for quarter in "${quarters[@]}"; do
  projected_users=$(echo "scale=0; $projected_users * $growth_rate" | bc)
  concurrent_users=$(echo "scale=0; $projected_users / 100" | bc) # 1% concurrent usage assumption
  
  echo "Testing ${quarter} projection: ${projected_users} total users (${concurrent_users} concurrent)..."
  
  devstress https://api.example.com/endpoint \
    --users $concurrent_users --duration 300 \
    --header "X-Growth-Projection: ${quarter}" \
    --header "X-Total-Users: ${projected_users}" \
    --header "X-Concurrent-Users: ${concurrent_users}" > "growth-${quarter}.log"
  
  # Analyze capacity requirements
  rps=$(grep "Requests/Second" "growth-${quarter}.log" | cut -d: -f2 | tr -d ' ')
  error_rate=$(grep "Error Rate" "growth-${quarter}.log" | cut -d: -f2 | tr -d '% ')
  
  if (( $(echo "$error_rate > 1.0" | bc -l) )); then
    echo "⚠️  ${quarter}: Scaling required (${error_rate}% error rate)"
  else
    echo "✅ ${quarter}: Current capacity sufficient (${error_rate}% error rate)"
  fi
done
```

### 2. Peak Traffic Modeling

**Scenario**: Modeling system behavior during predictable peak events.

```bash
#!/bin/bash
# peak-traffic-modeling.sh

echo "🏔️ Peak Traffic Modeling"

# Define peak traffic scenarios
peak_events=(
  "flash-sale:5000:spike:300"
  "product-launch:3000:ramp:600"
  "black-friday:8000:spike:1800"
  "cyber-monday:6000:steady:3600"
  "holiday-shopping:4000:ramp:7200"
)

for event in "${peak_events[@]}"; do
  IFS=':' read -r name users pattern duration <<< "$event"
  echo "Modeling ${name} peak traffic..."
  
  devstress https://api.example.com/endpoint \
    --users $users --scenario $pattern --duration $duration \
    --header "X-Peak-Event: ${name}" \
    --header "X-Expected-Users: ${users}" > "peak-${name}.log"
  
  # Analyze peak capacity results
  max_rps=$(grep "Requests/Second" "peak-${name}.log" | cut -d: -f2 | tr -d ' ')
  error_rate=$(grep "Error Rate" "peak-${name}.log" | cut -d: -f2 | tr -d '% ')
  p99_latency=$(grep "99th percentile" "peak-${name}.log" | cut -d: -f2 | tr -d ' ms')
  
  echo "${name}: ${max_rps} RPS, ${error_rate}% errors, ${p99_latency}ms P99"
  
  # Capacity recommendation
  if (( $(echo "$error_rate > 0.5" | bc -l) )); then
    recommended_instances=$(echo "scale=0; $users / 500" | bc) # 500 users per instance assumption
    echo "💡 Recommendation: Scale to ${recommended_instances} instances for ${name}"
  fi
done
```

### 3. Resource Utilization Analysis

**Scenario**: Correlating load test results with system resource usage.

```bash
#!/bin/bash
# resource-utilization-analysis.sh

echo "💻 Resource Utilization Analysis"

load_levels=(100 200 400 800 1600)

echo "load_level,rps,cpu_usage,memory_usage,disk_io,network_io" > resource-analysis.csv

for load in "${load_levels[@]}"; do
  echo "Testing load level: ${load} users..."
  
  # Start system monitoring
  (
    while true; do
      timestamp=$(date '+%Y-%m-%d %H:%M:%S')
      cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
      memory_usage=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')
      echo "${timestamp},${cpu_usage},${memory_usage}" >> "system-metrics-${load}.log"
      sleep 5
    done
  ) &
  
  MONITOR_PID=$!
  
  # Run load test
  devstress https://api.example.com/endpoint \
    --users $load --duration 300 \
    --header "X-Load-Level: ${load}" > "load-${load}.log"
  
  # Stop monitoring
  kill $MONITOR_PID
  
  # Extract performance metrics
  rps=$(grep "Requests/Second" "load-${load}.log" | cut -d: -f2 | tr -d ' ')
  avg_cpu=$(awk -F, '{sum+=$2; count++} END {printf "%.1f", sum/count}' "system-metrics-${load}.log")
  avg_memory=$(awk -F, '{sum+=$3; count++} END {printf "%.1f", sum/count}' "system-metrics-${load}.log")
  
  echo "${load},${rps},${avg_cpu},${avg_memory},TBD,TBD" >> resource-analysis.csv
  echo "Load ${load}: ${rps} RPS, ${avg_cpu}% CPU, ${avg_memory}% Memory"
done

echo "✅ Resource utilization analysis complete. Results in resource-analysis.csv"
```

### 4. Cost-Performance Optimization

**Scenario**: Finding the optimal balance between performance and infrastructure cost.

```bash
#!/bin/bash
# cost-performance-optimization.sh

echo "💰 Cost-Performance Optimization Analysis"

# Define instance types with hourly costs (example AWS pricing)
instance_types=(
  "t3.small:0.0208:1cpu-2gb"
  "t3.medium:0.0416:2cpu-4gb"
  "t3.large:0.0832:2cpu-8gb"
  "c5.large:0.085:2cpu-4gb"
  "c5.xlarge:0.17:4cpu-8gb"
  "c5.2xlarge:0.34:8cpu-16gb"
)

echo "instance_type,hourly_cost,rps,cost_per_1000_requests" > cost-performance.csv

for instance in "${instance_types[@]}"; do
  IFS=':' read -r type cost spec <<< "$instance"
  echo "Testing ${type} (${spec}) at \$${cost}/hour..."
  
  devstress https://${type}.api.example.com/endpoint \
    --users 500 --duration 300 \
    --header "X-Instance-Type: ${type}" \
    --header "X-Instance-Spec: ${spec}" > "cost-${type}.log"
  
  # Calculate cost per performance metrics
  rps=$(grep "Requests/Second" "cost-${type}.log" | cut -d: -f2 | tr -d ' ')
  cost_per_1000_requests=$(echo "scale=4; $cost / $rps * 1000 / 3600" | bc)
  
  echo "${type},${cost},${rps},${cost_per_1000_requests}" >> cost-performance.csv
  echo "${type}: ${rps} RPS at \$${cost_per_1000_requests} per 1000 requests"
done

# Find optimal cost-performance ratio
echo "🎯 Finding optimal cost-performance ratio..."
sort -t, -k4 -n cost-performance.csv | head -n 3 | while IFS=, read -r type cost rps cost_per_req; do
  echo "Top performer: ${type} - ${rps} RPS at \$${cost_per_req} per 1000 requests"
done
```

---

## 🌍 Geographic Scaling Analysis

### 1. Multi-Region Performance Testing

**Scenario**: Testing performance across different geographic regions.

```bash
#!/bin/bash
# multi-region-performance.sh

echo "🌍 Multi-Region Performance Analysis"

regions=(
  "us-east-1:N. Virginia"
  "us-west-2:Oregon"
  "eu-west-1:Ireland" 
  "ap-southeast-1:Singapore"
  "ap-northeast-1:Tokyo"
)

echo "region,location,rps,avg_latency,p95_latency" > regional-performance.csv

for region_info in "${regions[@]}"; do
  IFS=':' read -r region location <<< "$region_info"
  echo "Testing ${location} (${region})..."
  
  devstress https://${region}.api.example.com/endpoint \
    --users 200 --duration 300 \
    --header "X-Origin-Region: ${region}" \
    --header "CloudFront-Viewer-Country: ${region}" > "region-${region}.log"
  
  # Extract regional performance metrics
  rps=$(grep "Requests/Second" "region-${region}.log" | cut -d: -f2 | tr -d ' ')
  avg_latency=$(grep "Average:" "region-${region}.log" | cut -d: -f2 | tr -d ' ms')
  p95_latency=$(grep "95th percentile:" "region-${region}.log" | cut -d: -f2 | tr -d ' ms')
  
  echo "${region},${location},${rps},${avg_latency},${p95_latency}" >> regional-performance.csv
  echo "${location}: ${rps} RPS, ${avg_latency}ms avg, ${p95_latency}ms P95"
done

echo "✅ Multi-region analysis complete. Consider regions with <200ms P95 latency for optimal UX."
```

### 2. CDN Performance Impact Analysis

**Scenario**: Measuring CDN impact on application performance.

```bash
#!/bin/bash
# cdn-performance-analysis.sh

echo "🚀 CDN Performance Impact Analysis"

# Test without CDN
echo "Testing direct origin performance..."
devstress https://origin.api.example.com/static/data.json \
  --users 500 --duration 300 \
  --header "Cache-Control: no-cache" \
  --header "X-CDN-Test: origin-direct" > cdn-origin.log

# Test with CDN (cold cache)
echo "Testing CDN performance (cold cache)..."
devstress https://cdn.api.example.com/static/data.json \
  --users 500 --duration 300 \
  --header "Cache-Control: no-cache" \
  --header "X-CDN-Test: cold-cache" > cdn-cold.log

# Wait for cache warm-up
echo "Warming CDN cache..."
sleep 60

# Test with CDN (warm cache)  
echo "Testing CDN performance (warm cache)..."
devstress https://cdn.api.example.com/static/data.json \
  --users 500 --duration 300 \
  --header "X-CDN-Test: warm-cache" > cdn-warm.log

# Analyze CDN impact
echo "📊 CDN Impact Analysis:"
origin_rps=$(grep "Requests/Second" cdn-origin.log | cut -d: -f2 | tr -d ' ')
cold_rps=$(grep "Requests/Second" cdn-cold.log | cut -d: -f2 | tr -d ' ')
warm_rps=$(grep "Requests/Second" cdn-warm.log | cut -d: -f2 | tr -d ' ')

origin_latency=$(grep "Average:" cdn-origin.log | cut -d: -f2 | tr -d ' ms')
cold_latency=$(grep "Average:" cdn-cold.log | cut -d: -f2 | tr -d ' ms')
warm_latency=$(grep "Average:" cdn-warm.log | cut -d: -f2 | tr -d ' ms')

echo "Origin: ${origin_rps} RPS, ${origin_latency}ms avg"
echo "CDN Cold: ${cold_rps} RPS, ${cold_latency}ms avg"
echo "CDN Warm: ${warm_rps} RPS, ${warm_latency}ms avg"

improvement=$(echo "scale=1; ($warm_rps - $origin_rps) / $origin_rps * 100" | bc)
echo "CDN Performance Improvement: ${improvement}%"
```

---

## 🔄 Load Balancer Optimization

### 1. Load Balancing Strategy Testing

**Scenario**: Testing different load balancing algorithms and their impact.

```bash
#!/bin/bash
# load-balancer-strategy-test.sh

echo "⚖️ Load Balancer Strategy Testing"

strategies=("round-robin" "least-connections" "weighted-round-robin" "ip-hash")

for strategy in "${strategies[@]}"; do
  echo "Testing ${strategy} strategy..."
  
  devstress https://lb.api.example.com/endpoint \
    --users 400 --duration 300 \
    --header "X-LB-Strategy: ${strategy}" \
    --header "X-LB-Test: strategy-comparison" > "lb-${strategy}.log"
  
  # Analyze distribution effectiveness
  rps=$(grep "Requests/Second" "lb-${strategy}.log" | cut -d: -f2 | tr -d ' ')
  error_rate=$(grep "Error Rate" "lb-${strategy}.log" | cut -d: -f2 | tr -d '% ')
  p95_latency=$(grep "95th percentile" "lb-${strategy}.log" | cut -d: -f2 | tr -d ' ms')
  
  echo "${strategy}: ${rps} RPS, ${error_rate}% errors, ${p95_latency}ms P95"
done

echo "💡 Recommendation: Choose strategy with lowest error rate and P95 latency"
```

### 2. Health Check Impact Analysis

**Scenario**: Testing the impact of health check frequency on performance.

```bash
#!/bin/bash
# health-check-impact.sh

echo "💓 Health Check Impact Analysis"

health_check_intervals=(5 15 30 60)

for interval in "${health_check_intervals[@]}"; do
  echo "Testing health check interval: ${interval}s..."
  
  devstress https://api.example.com/endpoint \
    --users 300 --duration 600 \
    --header "X-Health-Check-Interval: ${interval}s" \
    --header "X-Test-Type: health-check-impact" > "health-${interval}s.log"
  
  # Analyze impact of health check frequency
  rps=$(grep "Requests/Second" "health-${interval}s.log" | cut -d: -f2 | tr -d ' ')
  avg_latency=$(grep "Average:" "health-${interval}s.log" | cut -d: -f2 | tr -d ' ms')
  
  echo "${interval}s interval: ${rps} RPS, ${avg_latency}ms avg latency"
done
```

### 3. Failover Testing

**Scenario**: Testing load balancer failover behavior and recovery time.

```bash
#!/bin/bash
# failover-testing.sh

echo "🔄 Load Balancer Failover Testing"

# Start continuous load testing
devstress https://lb.api.example.com/endpoint \
  --users 200 --duration 1800 \
  --header "X-Failover-Test: continuous-load" &

LOAD_TEST_PID=$!

# Monitor performance during failover simulation
echo "Monitoring baseline performance..."
sleep 300

echo "Simulating server failure..."
# Trigger failover (this would typically involve stopping a server)
curl -X POST https://lb-admin.api.example.com/simulate-failure \
  -H "Authorization: Bearer ${ADMIN_TOKEN}"

echo "Monitoring failover response..."
sleep 300

echo "Simulating server recovery..."
curl -X POST https://lb-admin.api.example.com/simulate-recovery \
  -H "Authorization: Bearer ${ADMIN_TOKEN}"

echo "Monitoring recovery performance..."
sleep 300

# Stop load test
kill $LOAD_TEST_PID

echo "✅ Failover testing complete. Check logs for performance impact."
```

---

## 🧮 Capacity Planning Calculations

### 1. Peak Capacity Planning

**Scenario**: Calculating required capacity for expected peak loads.

```bash
#!/bin/bash
# peak-capacity-calculator.sh

echo "🧮 Peak Capacity Planning Calculator"

# Business requirements
EXPECTED_DAILY_USERS=100000
PEAK_HOUR_PERCENTAGE=20  # 20% of daily users in peak hour
CONCURRENT_PERCENTAGE=5  # 5% of peak hour users are concurrent
SAFETY_MARGIN=50        # 50% safety margin

# Calculate peak concurrent users
peak_hour_users=$((EXPECTED_DAILY_USERS * PEAK_HOUR_PERCENTAGE / 100))
peak_concurrent_users=$((peak_hour_users * CONCURRENT_PERCENTAGE / 100))
required_capacity=$((peak_concurrent_users * (100 + SAFETY_MARGIN) / 100))

echo "📊 Capacity Planning Results:"
echo "Expected daily users: ${EXPECTED_DAILY_USERS}"
echo "Peak hour users: ${peak_hour_users}"
echo "Peak concurrent users: ${peak_concurrent_users}"
echo "Required capacity (with ${SAFETY_MARGIN}% margin): ${required_capacity}"

# Test calculated capacity
echo "🧪 Testing calculated capacity..."
devstress https://api.example.com/endpoint \
  --users $required_capacity --duration 300 \
  --header "X-Capacity-Test: peak-planning" \
  --header "X-Required-Capacity: ${required_capacity}" > capacity-test.log

# Validate capacity planning
actual_rps=$(grep "Requests/Second" capacity-test.log | cut -d: -f2 | tr -d ' ')
error_rate=$(grep "Error Rate" capacity-test.log | cut -d: -f2 | tr -d '% ')

if (( $(echo "$error_rate < 1.0" | bc -l) )); then
  echo "✅ Capacity planning validated: ${actual_rps} RPS with ${error_rate}% error rate"
else
  echo "⚠️  Capacity planning needs adjustment: ${error_rate}% error rate exceeds threshold"
  recommended_capacity=$((required_capacity * 130 / 100)) # 30% increase
  echo "💡 Recommended capacity: ${recommended_capacity} concurrent users"
fi
```

### 2. Storage Scaling Analysis

**Scenario**: Testing database and storage performance under different scaling scenarios.

```bash
#!/bin/bash
# storage-scaling-analysis.sh

echo "💾 Storage Scaling Analysis"

storage_configs=(
  "standard-ssd:100iops:1000gb"
  "premium-ssd:1000iops:1000gb" 
  "ultra-ssd:10000iops:1000gb"
  "standard-ssd:100iops:5000gb"
  "premium-ssd:1000iops:5000gb"
)

echo "storage_type,iops,size_gb,rps,avg_response,p95_response,error_rate" > storage-analysis.csv

for config in "${storage_configs[@]}"; do
  IFS=':' read -r storage_type iops size <<< "$config"
  echo "Testing ${storage_type} (${iops} IOPS, ${size}GB)..."
  
  devstress https://api.example.com/database/heavy \
    --users 200 --duration 300 \
    --header "X-Storage-Type: ${storage_type}" \
    --header "X-Storage-IOPS: ${iops}" \
    --header "X-Storage-Size: ${size}" \
    --timeout 30 > "storage-${storage_type}-${iops}.log"
  
  # Extract storage performance metrics
  rps=$(grep "Requests/Second" "storage-${storage_type}-${iops}.log" | cut -d: -f2 | tr -d ' ')
  avg_response=$(grep "Average:" "storage-${storage_type}-${iops}.log" | cut -d: -f2 | tr -d ' ms')
  p95_response=$(grep "95th percentile:" "storage-${storage_type}-${iops}.log" | cut -d: -f2 | tr -d ' ms')
  error_rate=$(grep "Error Rate:" "storage-${storage_type}-${iops}.log" | cut -d: -f2 | tr -d '% ')
  
  echo "${storage_type},${iops},${size},${rps},${avg_response},${p95_response},${error_rate}" >> storage-analysis.csv
  echo "${storage_type}: ${rps} RPS, ${avg_response}ms avg, ${p95_response}ms P95"
done

echo "✅ Storage scaling analysis complete. Results in storage-analysis.csv"
```

### 3. Network Bandwidth Planning

**Scenario**: Testing network bandwidth requirements for different load levels.

```bash
#!/bin/bash
# network-bandwidth-planning.sh

echo "🌐 Network Bandwidth Planning"

# Test different payload sizes to understand bandwidth requirements
payload_sizes=(1 10 100 1000 10000) # KB

echo "payload_size_kb,users,rps,bandwidth_mbps_per_user,total_bandwidth_mbps" > bandwidth-analysis.csv

for size in "${payload_sizes[@]}"; do
  echo "Testing ${size}KB payload size..."
  
  devstress https://api.example.com/data/payload/${size}kb \
    --users 100 --duration 300 \
    --header "X-Payload-Size: ${size}KB" \
    --header "X-Bandwidth-Test: true" > "bandwidth-${size}kb.log"
  
  # Calculate bandwidth requirements
  rps=$(grep "Requests/Second" "bandwidth-${size}kb.log" | cut -d: -f2 | tr -d ' ')
  bandwidth_per_user=$(echo "scale=2; $rps * $size * 8 / 1024" | bc) # Mbps per user
  total_bandwidth_100_users=$(echo "scale=2; $bandwidth_per_user * 100" | bc)
  
  echo "${size},100,${rps},${bandwidth_per_user},${total_bandwidth_100_users}" >> bandwidth-analysis.csv
  echo "${size}KB: ${rps} RPS, ${bandwidth_per_user} Mbps/user, ${total_bandwidth_100_users} Mbps total"
done

echo "💡 Bandwidth Planning Recommendations:"
echo "- Small payloads (<10KB): ~1 Mbps per 100 concurrent users"  
echo "- Medium payloads (100KB): ~10-50 Mbps per 100 concurrent users"
echo "- Large payloads (1MB+): >100 Mbps per 100 concurrent users"
```

---

## 🎯 Performance SLA Definition

### 1. SLA Baseline Establishment

**Scenario**: Establishing performance baselines for SLA definition.

```bash
#!/bin/bash
# sla-baseline-establishment.sh

echo "📋 SLA Baseline Establishment"

# Test different SLA scenarios
sla_scenarios=(
  "bronze:100:5000:2000" # tier:users:p95_target_ms:p99_target_ms
  "silver:200:3000:5000"
  "gold:500:2000:3000"
  "platinum:1000:1000:2000"
)

echo "sla_tier,users,actual_p95,actual_p99,p95_target,p99_target,p95_sla_met,p99_sla_met" > sla-baseline.csv

for scenario in "${sla_scenarios[@]}"; do
  IFS=':' read -r tier users p95_target p99_target <<< "$scenario"
  echo "Testing ${tier} SLA tier (${users} users)..."
  
  devstress https://api.example.com/endpoint \
    --users $users --duration 600 \
    --header "X-SLA-Tier: ${tier}" \
    --header "X-SLA-Test: baseline" > "sla-${tier}.log"
  
  # Extract performance metrics
  actual_p95=$(grep "95th percentile:" "sla-${tier}.log" | cut -d: -f2 | tr -d ' ms')
  actual_p99=$(grep "99th percentile:" "sla-${tier}.log" | cut -d: -f2 | tr -d ' ms')
  
  # Check SLA compliance
  p95_met=$([ $actual_p95 -le $p95_target ] && echo "YES" || echo "NO")
  p99_met=$([ $actual_p99 -le $p99_target ] && echo "YES" || echo "NO")
  
  echo "${tier},${users},${actual_p95},${actual_p99},${p95_target},${p99_target},${p95_met},${p99_met}" >> sla-baseline.csv
  echo "${tier}: P95=${actual_p95}ms (target: ${p95_target}ms) P99=${actual_p99}ms (target: ${p99_target}ms)"
done

echo "✅ SLA baseline establishment complete. Review sla-baseline.csv for compliance."
```

### 2. SLA Monitoring and Alerting

**Scenario**: Continuous SLA monitoring with alerting thresholds.

```bash
#!/bin/bash
# sla-monitoring.sh

echo "📊 Continuous SLA Monitoring"

SLA_P95_THRESHOLD=2000 # ms
SLA_P99_THRESHOLD=5000 # ms
SLA_ERROR_THRESHOLD=1  # %

while true; do
  current_time=$(date '+%Y-%m-%d %H:%M:%S')
  echo "🔍 SLA Check at ${current_time}"
  
  # Run quick SLA validation test
  devstress https://api.example.com/endpoint \
    --users 100 --duration 60 \
    --header "X-SLA-Monitor: continuous" > sla-check.log
  
  # Extract metrics
  p95_latency=$(grep "95th percentile:" sla-check.log | cut -d: -f2 | tr -d ' ms')
  p99_latency=$(grep "99th percentile:" sla-check.log | cut -d: -f2 | tr -d ' ms')
  error_rate=$(grep "Error Rate:" sla-check.log | cut -d: -f2 | tr -d '% ')
  
  # Check SLA violations
  sla_violations=""
  if [ $p95_latency -gt $SLA_P95_THRESHOLD ]; then
    sla_violations="${sla_violations}P95: ${p95_latency}ms > ${SLA_P95_THRESHOLD}ms; "
  fi
  
  if [ $p99_latency -gt $SLA_P99_THRESHOLD ]; then
    sla_violations="${sla_violations}P99: ${p99_latency}ms > ${SLA_P99_THRESHOLD}ms; "
  fi
  
  if (( $(echo "$error_rate > $SLA_ERROR_THRESHOLD" | bc -l) )); then
    sla_violations="${sla_violations}Error Rate: ${error_rate}% > ${SLA_ERROR_THRESHOLD}%; "
  fi
  
  # Alert if SLA violations detected
  if [ -n "$sla_violations" ]; then
    echo "🚨 SLA VIOLATION DETECTED: ${sla_violations}"
    # Send alert (email, Slack, PagerDuty, etc.)
    # curl -X POST https://hooks.slack.com/webhook \
    #   -d "{'text': 'SLA Violation: ${sla_violations}'}"
  else
    echo "✅ SLA compliance OK: P95=${p95_latency}ms, P99=${p99_latency}ms, Errors=${error_rate}%"
  fi
  
  # Wait before next check
  sleep 300 # Check every 5 minutes
done
```

---

## 🎉 Capacity Planning Best Practices Summary

### 1. Planning Methodology

```bash
# 1. Establish current baseline
devstress https://api.example.com/endpoint --users 100 --duration 300

# 2. Test incremental scaling
for users in 200 400 800 1600; do
  devstress https://api.example.com/endpoint --users $users --duration 300
done

# 3. Identify breaking point
devstress https://api.example.com/endpoint --users 3200 --scenario spike --duration 180

# 4. Plan safety margin (typically 50-100% above expected peak)
devstress https://api.example.com/endpoint --users $((expected_peak * 150 / 100)) --duration 300
```

### 2. Key Metrics to Monitor

- **Response Time Percentiles**: P50, P95, P99
- **Error Rates**: Overall and by error type
- **Throughput**: Requests per second sustainability
- **Resource Utilization**: CPU, Memory, Disk, Network
- **Scaling Efficiency**: Performance per additional resource unit

### 3. Common Scaling Patterns

```bash
# Linear scaling (ideal)
# Performance doubles when resources double

# Sub-linear scaling (common)
# Performance increases less than resource increase due to coordination overhead

# Negative scaling (problematic)  
# Performance decreases when resources increase due to contention
```

### 4. Infrastructure Recommendations

- **Start small**: Begin with minimal viable capacity
- **Scale horizontally**: Distribute load across multiple instances
- **Monitor continuously**: Implement real-time performance monitoring
- **Plan for peaks**: Design for 150-200% of expected peak capacity
- **Test failure scenarios**: Validate performance during partial outages

---

**🎯 This comprehensive scaling guide provides the frameworks and examples needed to plan, test, and optimize infrastructure capacity using DevStress. Each scenario represents proven patterns used by engineering teams to ensure their systems can handle growth and peak loads effectively.**

**🚀 Ready to plan your scaling strategy? Start with the examples most relevant to your growth projections and infrastructure architecture!**

```bash
pip install devstress
# Begin your capacity planning journey!
```