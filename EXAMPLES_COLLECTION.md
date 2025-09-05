# 📚 DevStress Examples Collection

## 🌟 Real-World Testing Scenarios

This comprehensive collection showcases DevStress in action across diverse real-world scenarios, demonstrating its versatility and power across different industries, use cases, and technical challenges.

---

## 🛒 E-Commerce & Retail Examples

### 1. Flash Sale Load Testing

**Scenario**: Testing a flash sale endpoint that will receive thousands of simultaneous requests when a limited-time offer goes live.

```bash
# Basic flash sale test
devstress https://shop.example.com/flash-sale/limited-edition \
  --users 2000 \
  --scenario spike \
  --duration 120 \
  --header "User-Agent: DevStress-FlashSale-Test" \
  --header "Accept: application/json"

# Expected Results Analysis:
# - Initial spike should handle 2000 concurrent users
# - Response times under 2s for 95th percentile
# - Error rate below 1% even during peak
```

### 2. Shopping Cart Abandonment Testing

**Scenario**: Testing cart operations under load to identify performance bottlenecks that lead to cart abandonment.

```bash
# Cart operations load test
devstress https://api.shop.example.com/cart/add \
  --users 500 \
  --duration 300 \
  --rps 100 \
  --header "Authorization: Bearer ${CART_API_TOKEN}" \
  --header "Content-Type: application/json" \
  --header "X-Session-ID: test-session-$(date +%s)"

# Follow-up checkout flow test
devstress https://api.shop.example.com/checkout/process \
  --users 200 \
  --scenario ramp \
  --duration 180 \
  --header "Authorization: Bearer ${CHECKOUT_API_TOKEN}"
```

### 3. Product Search Performance

**Scenario**: Testing search functionality during peak traffic periods like Black Friday.

```bash
# Search API load testing with realistic query patterns
devstress https://api.shop.example.com/search?q=popular-product \
  --users 800 \
  --duration 240 \
  --rps 150 \
  --header "X-Search-Context: black-friday-sale" \
  --timeout 5
```

### 4. Inventory Management Stress Test

**Scenario**: Testing inventory synchronization across multiple concurrent purchase attempts.

```bash
# High-concurrency inventory test
devstress https://api.shop.example.com/inventory/reserve \
  --users 1000 \
  --scenario spike \
  --duration 60 \
  --header "Authorization: Bearer ${INVENTORY_TOKEN}" \
  --header "X-Test-Mode: high-concurrency"
```

---

## 💰 Financial Services Examples

### 1. High-Frequency Trading API Testing

**Scenario**: Testing market data APIs that need to handle thousands of requests per second with sub-millisecond latency requirements.

```bash
# HFT market data API test
devstress https://api.trading.example.com/market-data/quotes \
  --users 500 \
  --rps 2000 \
  --duration 300 \
  --header "Authorization: Bearer ${HFT_API_KEY}" \
  --header "X-Trading-Session: load-test-$(date +%s)" \
  --timeout 1
```

### 2. Payment Processing Validation

**Scenario**: Testing payment gateway performance under various load conditions.

```bash
# Payment gateway load test
devstress https://payments.example.com/api/process \
  --users 200 \
  --scenario ramp \
  --duration 600 \
  --rps 50 \
  --header "Authorization: Bearer ${PAYMENT_API_KEY}" \
  --header "X-Idempotency-Key: test-$(uuidgen)" \
  --header "Content-Type: application/json"
```

### 3. Banking API Stress Testing

**Scenario**: Testing core banking operations like balance inquiries and transfers.

```bash
# Banking API comprehensive test
devstress https://api.bank.example.com/accounts/balance \
  --users 300 \
  --duration 400 \
  --rps 75 \
  --header "Authorization: Bearer ${BANKING_TOKEN}" \
  --header "X-Customer-ID: test-customer" \
  --header "X-Transaction-Context: load-testing"
```

### 4. Credit Scoring System Testing

**Scenario**: Testing credit scoring APIs that need to handle batch processing loads.

```bash
# Credit scoring batch processing test
devstress https://api.credit.example.com/score/calculate \
  --users 100 \
  --scenario steady \
  --duration 1800 \
  --rps 25 \
  --header "Authorization: Bearer ${CREDIT_API_KEY}" \
  --timeout 30
```

---

## 🏥 Healthcare & Medical Examples

### 1. Electronic Health Records (EHR) Testing

**Scenario**: Testing EHR systems during peak usage periods like shift changes.

```bash
# EHR patient lookup load test
devstress https://ehr.hospital.example.com/api/patients/search \
  --users 50 \
  --duration 900 \
  --rps 20 \
  --header "Authorization: Bearer ${EHR_TOKEN}" \
  --header "X-User-Role: physician" \
  --header "X-Facility-ID: hospital-main" \
  --header "X-HIPAA-Audit: load-test-$(date +%Y%m%d-%H%M%S)"
```

### 2. Telemedicine Platform Testing

**Scenario**: Testing video consultation booking system during high-demand periods.

```bash
# Telemedicine booking API test
devstress https://telehealth.example.com/api/appointments/book \
  --users 80 \
  --scenario ramp \
  --duration 300 \
  --rps 15 \
  --header "Authorization: Bearer ${TELEHEALTH_TOKEN}" \
  --header "X-Patient-Priority: routine" \
  --timeout 15
```

### 3. Medical Imaging System Testing

**Scenario**: Testing PACS (Picture Archiving and Communication System) under load.

```bash
# Medical imaging retrieval test
devstress https://pacs.hospital.example.com/api/images/retrieve \
  --users 25 \
  --duration 1200 \
  --rps 10 \
  --header "Authorization: Bearer ${PACS_TOKEN}" \
  --header "X-Modality: CT-SCAN" \
  --timeout 60
```

### 4. Emergency Alert System Testing

**Scenario**: Testing critical alert systems that must work during emergencies.

```bash
# Emergency alert system stress test
devstress https://alerts.hospital.example.com/api/emergency/broadcast \
  --users 200 \
  --scenario spike \
  --duration 120 \
  --header "Authorization: Bearer ${EMERGENCY_TOKEN}" \
  --header "X-Alert-Priority: critical" \
  --timeout 5
```

---

## 🎮 Gaming & Entertainment Examples

### 1. Multiplayer Game Server Testing

**Scenario**: Testing game matchmaking systems during peak gaming hours.

```bash
# Matchmaking API load test
devstress https://game-api.example.com/matchmaking/find \
  --users 2000 \
  --scenario ramp \
  --duration 600 \
  --rps 200 \
  --header "Authorization: Bearer ${GAME_API_KEY}" \
  --header "X-Game-Mode: battle-royale" \
  --header "X-Region: us-west"
```

### 2. Leaderboard System Testing

**Scenario**: Testing leaderboard APIs during tournament events.

```bash
# Leaderboard API stress test
devstress https://api.game.example.com/leaderboards/global \
  --users 5000 \
  --scenario spike \
  --duration 180 \
  --rps 500 \
  --header "X-Tournament: world-championship" \
  --timeout 3
```

### 3. Game Asset Download Testing

**Scenario**: Testing content delivery for game updates and downloads.

```bash
# Game asset CDN test
devstress https://cdn.game.example.com/assets/latest/manifest.json \
  --users 10000 \
  --scenario spike \
  --duration 300 \
  --header "User-Agent: GameClient/1.2.3" \
  --timeout 30
```

### 4. Real-Time Gaming Analytics

**Scenario**: Testing analytics endpoints that collect real-time gaming data.

```bash
# Gaming analytics ingestion test
devstress https://analytics.game.example.com/api/events/batch \
  --users 1000 \
  --duration 1800 \
  --rps 300 \
  --header "Authorization: Bearer ${ANALYTICS_KEY}" \
  --header "Content-Type: application/json" \
  --header "X-Game-Version: 1.2.3"
```

---

## 🌐 API & Web Services Examples

### 1. RESTful API Comprehensive Testing

**Scenario**: Testing a complete REST API with multiple endpoints and operations.

```bash
# GET endpoint performance
devstress https://api.example.com/v1/users \
  --users 200 \
  --duration 300 \
  --rps 100 \
  --header "Authorization: Bearer ${API_TOKEN}"

# POST endpoint stress test
devstress https://api.example.com/v1/users \
  --users 100 \
  --scenario ramp \
  --duration 240 \
  --rps 50 \
  --header "Authorization: Bearer ${API_TOKEN}" \
  --header "Content-Type: application/json"
```

### 2. Microservices Communication Testing

**Scenario**: Testing inter-service communication in a microservices architecture.

```bash
# User service test
devstress https://user-service.k8s.local/api/profile \
  --users 150 \
  --duration 420 \
  --rps 75 \
  --header "Authorization: Bearer ${SERVICE_TOKEN}" \
  --header "X-Service-Mesh: istio"

# Order service cascade test
devstress https://order-service.k8s.local/api/process \
  --users 100 \
  --scenario spike \
  --duration 180 \
  --header "Authorization: Bearer ${SERVICE_TOKEN}"
```

### 3. GraphQL API Testing

**Scenario**: Testing GraphQL endpoints with complex queries (future capability).

```bash
# GraphQL query performance test (future feature)
# devstress https://api.example.com/graphql \
#   --query-file complex-queries.graphql \
#   --users 200 \
#   --duration 300 \
#   --header "Authorization: Bearer ${GRAPHQL_TOKEN}"
```

### 4. WebSocket Connection Testing

**Scenario**: Testing real-time WebSocket connections (future capability).

```bash
# WebSocket load test (future feature)
# devstress ws://realtime.example.com/chat \
#   --connections 1000 \
#   --message-rate 50 \
#   --duration 600
```

---

## 📱 Mobile & IoT Examples

### 1. Mobile App Backend Testing

**Scenario**: Testing mobile app APIs during app store feature periods.

```bash
# Mobile app API test
devstress https://mobile-api.example.com/v2/sync \
  --users 5000 \
  --scenario ramp \
  --duration 900 \
  --rps 250 \
  --header "Authorization: Bearer ${MOBILE_API_KEY}" \
  --header "User-Agent: MobileApp/2.1.0 (iOS)" \
  --header "X-Device-Type: smartphone"
```

### 2. IoT Device Data Ingestion

**Scenario**: Testing IoT data collection endpoints handling sensor data.

```bash
# IoT data ingestion test
devstress https://iot.example.com/api/telemetry/batch \
  --users 10000 \
  --duration 3600 \
  --rps 1000 \
  --header "Authorization: Bearer ${IOT_API_KEY}" \
  --header "Content-Type: application/json" \
  --header "X-Device-Class: sensor" \
  --timeout 10
```

### 3. Push Notification System Testing

**Scenario**: Testing push notification delivery systems.

```bash
# Push notification service test
devstress https://push.example.com/api/notifications/send \
  --users 1000 \
  --scenario spike \
  --duration 120 \
  --rps 500 \
  --header "Authorization: Bearer ${PUSH_API_KEY}" \
  --header "X-Platform: cross-platform"
```

---

## 🔐 Authentication & Security Examples

### 1. OAuth 2.0 Flow Testing

**Scenario**: Testing OAuth authentication under high load.

```bash
# OAuth token endpoint test
devstress https://auth.example.com/oauth/token \
  --users 200 \
  --duration 300 \
  --rps 100 \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --header "Authorization: Basic $(echo -n 'client_id:client_secret' | base64)"
```

### 2. JWT Token Validation Testing

**Scenario**: Testing JWT validation endpoints under load.

```bash
# JWT validation performance test
devstress https://api.example.com/auth/validate \
  --users 500 \
  --duration 600 \
  --rps 200 \
  --header "Authorization: Bearer ${TEST_JWT_TOKEN}" \
  --header "X-Token-Type: access-token"
```

### 3. Multi-Factor Authentication Testing

**Scenario**: Testing MFA systems during high-traffic periods.

```bash
# MFA verification endpoint test
devstress https://auth.example.com/mfa/verify \
  --users 100 \
  --scenario ramp \
  --duration 480 \
  --rps 25 \
  --header "Authorization: Bearer ${MFA_SESSION_TOKEN}" \
  --timeout 30
```

### 4. API Rate Limiting Testing

**Scenario**: Testing API rate limiting implementation.

```bash
# Rate limit boundary test
devstress https://api.example.com/v1/data \
  --users 50 \
  --rps 120 \
  --duration 300 \
  --header "Authorization: Bearer ${RATE_LIMITED_TOKEN}" \
  --header "X-Rate-Limit-Test: true"
```

---

## 📊 Analytics & Data Processing Examples

### 1. Real-Time Analytics Ingestion

**Scenario**: Testing analytics data ingestion during peak traffic events.

```bash
# Analytics ingestion load test
devstress https://analytics.example.com/api/events/track \
  --users 2000 \
  --duration 1800 \
  --rps 800 \
  --header "Authorization: Bearer ${ANALYTICS_TOKEN}" \
  --header "Content-Type: application/json" \
  --header "X-Event-Type: user-interaction"
```

### 2. Batch Data Processing Testing

**Scenario**: Testing batch data processing APIs.

```bash
# Batch processing API test
devstress https://data.example.com/api/batch/process \
  --users 50 \
  --scenario steady \
  --duration 2400 \
  --rps 10 \
  --header "Authorization: Bearer ${BATCH_API_KEY}" \
  --timeout 120
```

### 3. Report Generation Testing

**Scenario**: Testing report generation systems under concurrent requests.

```bash
# Report generation load test
devstress https://reports.example.com/api/generate \
  --users 100 \
  --duration 900 \
  --rps 20 \
  --header "Authorization: Bearer ${REPORTS_TOKEN}" \
  --header "X-Report-Type: performance-summary" \
  --timeout 180
```

---

## 🌍 Content Delivery & Media Examples

### 1. CDN Performance Testing

**Scenario**: Testing CDN endpoints for static asset delivery.

```bash
# CDN static asset test
devstress https://cdn.example.com/assets/images/hero-image.jpg \
  --users 1000 \
  --scenario spike \
  --duration 180 \
  --header "Accept: image/*" \
  --header "Cache-Control: max-age=3600"
```

### 2. Video Streaming API Testing

**Scenario**: Testing video streaming service APIs.

```bash
# Video streaming API test
devstress https://video.example.com/api/stream/manifest \
  --users 500 \
  --duration 1200 \
  --rps 100 \
  --header "Authorization: Bearer ${VIDEO_API_KEY}" \
  --header "X-Quality: 1080p" \
  --timeout 15
```

### 3. File Upload Service Testing

**Scenario**: Testing file upload endpoints under concurrent load.

```bash
# File upload service test
devstress https://upload.example.com/api/files \
  --users 200 \
  --scenario ramp \
  --duration 600 \
  --rps 40 \
  --header "Authorization: Bearer ${UPLOAD_TOKEN}" \
  --header "Content-Type: multipart/form-data" \
  --timeout 60
```

---

## 🔄 CI/CD Integration Examples

### 1. GitHub Actions Performance Gate

**Scenario**: Implementing performance gates in GitHub Actions workflow.

```yaml
# .github/workflows/performance-gate.yml
name: Performance Gate
on:
  pull_request:
    branches: [main]

jobs:
  performance-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Install DevStress
      run: pip install devstress
    
    - name: API Performance Gate
      run: |
        devstress https://staging-api.example.com/health \
          --users 100 --duration 60 --rps 50
      env:
        API_TOKEN: ${{ secrets.STAGING_API_TOKEN }}
    
    - name: Critical Path Performance Test
      run: |
        devstress https://staging-api.example.com/api/orders \
          --users 200 --scenario ramp --duration 120 \
          --header "Authorization: Bearer ${{ secrets.API_TOKEN }}"
    
    - name: Upload Performance Reports
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: performance-reports
        path: ~/.devstress/*.html
```

### 2. Jenkins Performance Pipeline

**Scenario**: Jenkins pipeline with comprehensive performance testing.

```groovy
pipeline {
    agent any
    
    environment {
        STAGING_URL = 'https://staging-api.example.com'
        PRODUCTION_URL = 'https://api.example.com'
        API_TOKEN = credentials('api-token')
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install devstress'
            }
        }
        
        stage('Performance Testing') {
            parallel {
                stage('Baseline Test') {
                    steps {
                        sh '''
                            devstress ${STAGING_URL}/health \
                              --users 50 --duration 120 \
                              --header "Authorization: Bearer ${API_TOKEN}"
                        '''
                    }
                }
                stage('Load Test') {
                    steps {
                        sh '''
                            devstress ${STAGING_URL}/api/users \
                              --users 200 --scenario ramp --duration 300 \
                              --header "Authorization: Bearer ${API_TOKEN}"
                        '''
                    }
                }
                stage('Stress Test') {
                    steps {
                        sh '''
                            devstress ${STAGING_URL}/api/search \
                              --users 500 --scenario spike --duration 180 \
                              --header "Authorization: Bearer ${API_TOKEN}"
                        '''
                    }
                }
            }
        }
        
        stage('Performance Analysis') {
            steps {
                script {
                    // Custom performance analysis
                    def performanceReport = readFile('~/.devstress/latest-report.html')
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.devstress',
                        reportFiles: '*.html',
                        reportName: 'Performance Report'
                    ])
                }
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: '**/.devstress/*.html'
        }
        failure {
            emailext(
                subject: "Performance Test Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Performance test failed. Check the reports.",
                to: "${env.TEAM_EMAIL}"
            )
        }
    }
}
```

### 3. Docker Container Performance Testing

**Scenario**: Testing containerized applications with DevStress.

```dockerfile
# Dockerfile.devstress
FROM python:3.11-slim

RUN pip install devstress

COPY test-scenarios.json /tests/
COPY run-tests.sh /tests/

WORKDIR /tests

ENTRYPOINT ["./run-tests.sh"]
```

```bash
# run-tests.sh
#!/bin/bash
set -e

echo "🚀 Starting Performance Test Suite"

# Test 1: Health Check
echo "Testing health endpoint..."
devstress ${TARGET_URL}/health --users 50 --duration 60

# Test 2: API Load Test
echo "Testing API load..."
devstress ${TARGET_URL}/api/data \
  --users 200 --scenario ramp --duration 180 \
  --header "Authorization: Bearer ${API_TOKEN}"

# Test 3: Stress Test
echo "Testing stress conditions..."
devstress ${TARGET_URL}/api/search \
  --users 500 --scenario spike --duration 120

echo "✅ Performance Test Suite Complete"
```

### 4. Kubernetes CronJob Performance Monitoring

**Scenario**: Scheduled performance monitoring in Kubernetes.

```yaml
# k8s-performance-monitor.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: performance-monitor
spec:
  schedule: "0 */6 * * *" # Every 6 hours
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: devstress
            image: devstress:latest
            command:
            - /bin/bash
            - -c
            - |
              devstress https://api.example.com/health \
                --users 100 --duration 300 --rps 50 \
                --header "Authorization: Bearer $API_TOKEN" \
                --header "X-Monitor: kubernetes-cronjob"
            env:
            - name: API_TOKEN
              valueFrom:
                secretKeyRef:
                  name: api-credentials
                  key: token
          restartPolicy: OnFailure
```

---

## 🏗️ Infrastructure & DevOps Examples

### 1. Load Balancer Testing

**Scenario**: Testing load balancer distribution and failover.

```bash
# Load balancer distribution test
for endpoint in api1.example.com api2.example.com api3.example.com; do
  devstress https://${endpoint}/health \
    --users 100 --duration 180 \
    --header "X-LoadBalancer-Test: endpoint-${endpoint}" &
done
wait

echo "✅ Load balancer test complete"
```

### 2. Database Connection Pool Testing

**Scenario**: Testing database-backed APIs under high connection load.

```bash
# Database connection pool stress test
devstress https://api.example.com/database/query \
  --users 500 \
  --duration 900 \
  --rps 100 \
  --header "Authorization: Bearer ${DB_API_TOKEN}" \
  --header "X-Query-Type: connection-pool-test" \
  --timeout 30
```

### 3. Cache Performance Testing

**Scenario**: Testing caching layer effectiveness under load.

```bash
# Cache hit/miss performance test
devstress https://api.example.com/cached-data \
  --users 200 \
  --scenario ramp \
  --duration 600 \
  --rps 150 \
  --header "Cache-Control: no-cache" \
  --header "X-Cache-Test: performance-validation"
```

### 4. Auto-Scaling Validation

**Scenario**: Testing auto-scaling triggers and response times.

```bash
# Auto-scaling trigger test
devstress https://api.example.com/compute-intensive \
  --users 1000 \
  --scenario spike \
  --duration 300 \
  --header "X-Scaling-Test: trigger-validation" \
  --timeout 60
```

---

## 🧪 Debugging & Troubleshooting Examples

### 1. Performance Regression Detection

**Scenario**: Comparing performance between different application versions.

```bash
# Version A performance baseline
devstress https://api-v1.example.com/endpoint \
  --users 200 --duration 300 --rps 100 > performance-v1.log

# Version B performance test
devstress https://api-v2.example.com/endpoint \
  --users 200 --duration 300 --rps 100 > performance-v2.log

# Compare results
echo "Analyzing performance regression..."
grep "Requests/Second" performance-v1.log performance-v2.log
```

### 2. Memory Leak Detection Testing

**Scenario**: Long-running tests to identify memory leaks.

```bash
# Extended memory leak detection test
devstress https://api.example.com/endpoint \
  --users 100 \
  --duration 7200 \
  --rps 25 \
  --header "X-Test-Type: memory-leak-detection"
```

### 3. Error Rate Analysis

**Scenario**: Identifying error patterns under different load conditions.

```bash
# Progressive error rate testing
for users in 50 100 200 400 800; do
  echo "Testing with ${users} users..."
  devstress https://api.example.com/endpoint \
    --users ${users} \
    --duration 120 \
    --header "X-User-Load: ${users}" > "results-${users}-users.log"
  
  error_rate=$(grep "Error Rate" "results-${users}-users.log" | cut -d: -f2)
  echo "Error rate with ${users} users: ${error_rate}"
done
```

### 4. Timeout Threshold Testing

**Scenario**: Finding optimal timeout values for different endpoints.

```bash
# Timeout threshold analysis
for timeout in 5 10 15 30 60; do
  echo "Testing with ${timeout}s timeout..."
  devstress https://api.example.com/slow-endpoint \
    --users 100 \
    --duration 180 \
    --timeout ${timeout} \
    --header "X-Timeout-Test: ${timeout}s" > "timeout-${timeout}s.log"
done
```

---

## 📈 Performance Benchmarking Examples

### 1. API Response Time Benchmarking

**Scenario**: Establishing performance baselines for different API endpoints.

```bash
# Comprehensive API benchmarking suite
endpoints=(
  "/api/users"
  "/api/orders" 
  "/api/products"
  "/api/search"
  "/api/analytics"
)

for endpoint in "${endpoints[@]}"; do
  echo "Benchmarking ${endpoint}..."
  devstress https://api.example.com${endpoint} \
    --users 100 --duration 300 --rps 50 \
    --header "Authorization: Bearer ${API_TOKEN}" \
    --header "X-Benchmark: endpoint-${endpoint//\//-}" > "benchmark${endpoint//\//-}.log"
done
```

### 2. Throughput Capacity Testing

**Scenario**: Determining maximum sustainable throughput.

```bash
# Throughput capacity discovery
max_rps=0
for rps in 50 100 200 400 800 1600; do
  echo "Testing ${rps} RPS..."
  devstress https://api.example.com/endpoint \
    --users 200 --duration 180 --rps ${rps} \
    --header "X-RPS-Test: ${rps}" > "throughput-${rps}rps.log"
  
  error_rate=$(grep "Error Rate" "throughput-${rps}rps.log" | cut -d: -f2 | tr -d '% ')
  
  if (( $(echo "$error_rate < 1.0" | bc -l) )); then
    max_rps=$rps
    echo "✅ ${rps} RPS sustainable (${error_rate}% error rate)"
  else
    echo "❌ ${rps} RPS not sustainable (${error_rate}% error rate)"
    break
  fi
done

echo "Maximum sustainable RPS: ${max_rps}"
```

### 3. Scalability Curve Analysis

**Scenario**: Understanding how performance scales with concurrent users.

```bash
# Scalability curve generation
user_counts=(10 25 50 100 200 400 800 1600)

echo "user_count,rps,avg_response_time,error_rate" > scalability-analysis.csv

for users in "${user_counts[@]}"; do
  echo "Testing scalability with ${users} users..."
  
  result=$(devstress https://api.example.com/endpoint \
    --users ${users} --duration 180 \
    --header "X-Scalability-Test: ${users}-users")
  
  rps=$(echo "$result" | grep "Requests/Second" | cut -d: -f2 | tr -d ' ')
  avg_time=$(echo "$result" | grep "Average:" | cut -d: -f2 | tr -d ' ms')
  error_rate=$(echo "$result" | grep "Error Rate" | cut -d: -f2 | tr -d '% ')
  
  echo "${users},${rps},${avg_time},${error_rate}" >> scalability-analysis.csv
done

echo "✅ Scalability analysis complete. Results in scalability-analysis.csv"
```

---

## 🎯 Specialized Testing Scenarios

### 1. Geographic Distribution Testing

**Scenario**: Testing API performance from different geographic regions.

```bash
# Multi-region performance testing
regions=("us-east-1" "eu-west-1" "ap-southeast-1")

for region in "${regions[@]}"; do
  echo "Testing from ${region}..."
  devstress https://api.example.com/endpoint \
    --users 100 --duration 300 \
    --header "X-Origin-Region: ${region}" \
    --header "CloudFront-Viewer-Country: ${region}" > "perf-${region}.log"
done
```

### 2. Browser Simulation Testing

**Scenario**: Simulating different browser behaviors and user agents.

```bash
# Browser simulation load testing
user_agents=(
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15"
  "Mozilla/5.0 (X11; Linux x86_64) Firefox/121.0"
  "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Mobile/15E148"
)

for ua in "${user_agents[@]}"; do
  browser_name=$(echo "$ua" | grep -o -E '(Chrome|Safari|Firefox|Mobile)')
  echo "Testing ${browser_name} simulation..."
  
  devstress https://api.example.com/endpoint \
    --users 200 --duration 240 \
    --header "User-Agent: ${ua}" \
    --header "X-Browser-Test: ${browser_name}" > "browser-${browser_name}.log" &
done
wait
```

### 3. API Version Compatibility Testing

**Scenario**: Testing multiple API versions simultaneously.

```bash
# API version compatibility testing
api_versions=("v1" "v2" "v3" "beta")

for version in "${api_versions[@]}"; do
  echo "Testing API ${version}..."
  devstress https://api.example.com/${version}/endpoint \
    --users 150 --duration 300 \
    --header "Accept: application/vnd.api+json;version=${version}" \
    --header "X-API-Version: ${version}" > "api-${version}.log" &
done
wait
```

### 4. Seasonal Load Pattern Simulation

**Scenario**: Simulating seasonal traffic patterns.

```bash
# Holiday traffic simulation
seasonal_patterns=(
  "black-friday:2000:spike:300"
  "christmas-eve:1500:ramp:600" 
  "new-years:1000:steady:1800"
  "valentines:800:ramp:900"
)

for pattern in "${seasonal_patterns[@]}"; do
  IFS=':' read -r event users scenario duration <<< "$pattern"
  echo "Simulating ${event} traffic pattern..."
  
  devstress https://api.example.com/endpoint \
    --users ${users} \
    --scenario ${scenario} \
    --duration ${duration} \
    --header "X-Seasonal-Event: ${event}" > "seasonal-${event}.log" &
done
wait
```

---

## 🔧 Advanced Configuration Examples

### 1. Custom Environment Configuration

**Scenario**: Setting up DevStress with custom environment variables.

```bash
# Advanced environment configuration
export DEVSTRESS_REPORTS_DIR="/opt/performance-reports"
export DEVSTRESS_MAX_CONNECTIONS=5000
export DEVSTRESS_DEFAULT_TIMEOUT=30
export DEVSTRESS_ENABLE_DEBUG=true
export DEVSTRESS_CUSTOM_USER_AGENT="DevStress-Enterprise/1.0"

# Run with custom configuration
devstress https://api.example.com/endpoint \
  --users 1000 --duration 600 \
  --header "X-Environment: production-testing"
```

### 2. Multi-Stage Testing Pipeline

**Scenario**: Complex multi-stage testing with different configurations.

```bash
#!/bin/bash
# multi-stage-performance-test.sh

set -e

API_BASE="https://api.example.com"
TOKEN="Bearer ${API_TOKEN}"

echo "🚀 Starting Multi-Stage Performance Test"

# Stage 1: Warm-up
echo "Stage 1: System warm-up..."
devstress ${API_BASE}/health \
  --users 10 --duration 60 \
  --header "Authorization: ${TOKEN}" \
  --header "X-Stage: warmup"

# Stage 2: Baseline performance
echo "Stage 2: Baseline performance measurement..."
devstress ${API_BASE}/api/data \
  --users 100 --duration 300 \
  --header "Authorization: ${TOKEN}" \
  --header "X-Stage: baseline"

# Stage 3: Load ramp
echo "Stage 3: Load ramping..."
devstress ${API_BASE}/api/data \
  --users 500 --scenario ramp --duration 600 \
  --header "Authorization: ${TOKEN}" \
  --header "X-Stage: ramp"

# Stage 4: Peak load
echo "Stage 4: Peak load testing..."
devstress ${API_BASE}/api/data \
  --users 1000 --duration 300 \
  --header "Authorization: ${TOKEN}" \
  --header "X-Stage: peak"

# Stage 5: Spike test
echo "Stage 5: Spike testing..."
devstress ${API_BASE}/api/data \
  --users 2000 --scenario spike --duration 180 \
  --header "Authorization: ${TOKEN}" \
  --header "X-Stage: spike"

# Stage 6: Cooldown
echo "Stage 6: System cooldown..."
devstress ${API_BASE}/health \
  --users 10 --duration 120 \
  --header "Authorization: ${TOKEN}" \
  --header "X-Stage: cooldown"

echo "✅ Multi-Stage Performance Test Complete"
```

---

## 📋 Best Practices Summary

### 1. Test Planning Best Practices

```bash
# Always start with health checks
devstress https://api.example.com/health --users 10 --duration 30

# Establish baseline before load testing  
devstress https://api.example.com/endpoint --users 50 --duration 120

# Gradually increase load
devstress https://api.example.com/endpoint --users 100 --scenario ramp --duration 300

# Test edge cases with spike scenarios
devstress https://api.example.com/endpoint --users 500 --scenario spike --duration 180
```

### 2. Monitoring and Analysis Best Practices

```bash
# Use descriptive headers for tracking
devstress https://api.example.com/endpoint \
  --header "X-Test-Purpose: performance-validation" \
  --header "X-Test-Date: $(date +%Y-%m-%d)" \
  --header "X-Test-Engineer: ${USER}"

# Set appropriate timeouts for different endpoint types
devstress https://api.example.com/fast-endpoint --timeout 5
devstress https://api.example.com/slow-endpoint --timeout 30
devstress https://api.example.com/batch-endpoint --timeout 120
```

### 3. Result Interpretation Guidelines

```bash
# Good performance indicators:
# - P95 response time < 2000ms for web APIs
# - Error rate < 0.1% for critical paths  
# - Error rate < 1% for non-critical paths
# - RPS scales linearly with users (until bottleneck)
# - No memory leaks in long-running tests

# Performance red flags:
# - Sudden error rate spikes at specific user counts
# - Exponentially increasing response times
# - High variability in response times (P99 >> P95)
# - Resource exhaustion (CPU > 90%, Memory > 95%)
```

---

**🎉 This comprehensive examples collection demonstrates DevStress's versatility across industries, use cases, and technical scenarios. Each example is production-ready and represents real-world testing patterns used by development teams worldwide.**

**🚀 Ready to implement these patterns? Start with the examples most relevant to your use case and expand from there!**

```bash
pip install devstress
# Choose your example and start testing!
```