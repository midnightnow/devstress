#!/usr/bin/env python3
"""
Claude Flow Runner for DevStress
Execute automated load testing workflows
"""

import yaml
import subprocess
import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class ClaudeFlowRunner:
    """Execute Claude Flow workflows for DevStress"""
    
    def __init__(self, config_file: str = "claudeflow.yaml"):
        """Initialize with configuration file"""
        self.config_file = config_file
        self.config = self._load_config()
        self.results = {}
        
    def _load_config(self) -> Dict:
        """Load Claude Flow configuration"""
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def run_workflow(self, workflow_name: str, env_vars: Dict[str, str] = None) -> bool:
        """Run a specific workflow"""
        if workflow_name not in self.config['workflows']:
            print(f"❌ Workflow '{workflow_name}' not found")
            return False
        
        workflow = self.config['workflows'][workflow_name]
        print(f"\n🚀 Running Claude Flow Workflow: {workflow_name}")
        print(f"📝 Description: {workflow.get('description', 'No description')}")
        print("="*60)
        
        # Set environment variables
        env = os.environ.copy()
        if env_vars:
            env.update(env_vars)
        
        success = True
        for step in workflow.get('steps', []):
            if not self._run_step(step, env):
                success = False
                break
        
        return success
    
    def _run_step(self, step: Dict, env: Dict) -> bool:
        """Execute a single workflow step"""
        name = step.get('name', 'Unnamed step')
        print(f"\n📌 Step: {name}")
        print("-"*40)
        
        # Get the command
        command = step.get('run', '')
        
        # Substitute environment variables
        for key, value in env.items():
            command = command.replace(f"${key}", value)
            command = command.replace(f"${{{key}}}", value)
        
        print(f"🔧 Command: {command}")
        
        # Execute command
        result = subprocess.run(command, shell=True, capture_output=True, text=True, env=env)
        
        # Parse results
        metrics = self._parse_output(result.stdout)
        
        # Check expectations
        if 'expect' in step:
            return self._check_expectations(step['expect'], metrics)
        
        # Capture metrics if requested
        if 'capture' in step:
            self._capture_metrics(step['capture'], metrics)
        
        if 'capture_as' in step:
            self.results[step['capture_as']] = metrics
        
        return result.returncode == 0
    
    def _parse_output(self, output: str) -> Dict:
        """Parse DevStress output for metrics"""
        metrics = {}
        
        # Parse key metrics from output
        patterns = {
            'requests_per_second': r'Requests/Second:\s*([\d.]+)',
            'error_rate': r'Error Rate:\s*([\d.]+)%',
            'avg_response_time': r'Average:\s*([\d.]+)ms',
            'p95_response_time': r'95th percentile:\s*([\d.]+)ms',
            'p99_response_time': r'99th percentile:\s*([\d.]+)ms',
            'total_requests': r'Total Requests:\s*([\d,]+)',
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, output)
            if match:
                value = match.group(1).replace(',', '')
                metrics[key] = float(value) if '.' in value else int(value)
        
        return metrics
    
    def _check_expectations(self, expectations: Dict, metrics: Dict) -> bool:
        """Check if metrics meet expectations"""
        all_passed = True
        
        for key, expected in expectations.items():
            if key not in metrics:
                print(f"  ⚠️  Metric '{key}' not found in output")
                continue
            
            actual = metrics[key]
            
            # Parse expectation (e.g., "< 5%", ">= 90")
            if isinstance(expected, str):
                match = re.match(r'([<>=]+)\s*([\d.]+)%?', expected)
                if match:
                    op, value = match.groups()
                    value = float(value)
                    
                    passed = self._evaluate_condition(actual, op, value)
                    status = "✅" if passed else "❌"
                    print(f"  {status} {key}: {actual} (expected {expected})")
                    
                    if not passed:
                        all_passed = False
        
        return all_passed
    
    def _evaluate_condition(self, actual: float, operator: str, expected: float) -> bool:
        """Evaluate a condition"""
        if operator == '<':
            return actual < expected
        elif operator == '<=':
            return actual <= expected
        elif operator == '>':
            return actual > expected
        elif operator == '>=':
            return actual >= expected
        elif operator == '==':
            return actual == expected
        return False
    
    def _capture_metrics(self, metrics_to_capture: List[str], metrics: Dict):
        """Capture specific metrics for later use"""
        print("\n📊 Captured Metrics:")
        for metric in metrics_to_capture:
            if metric in metrics:
                print(f"  • {metric}: {metrics[metric]}")
    
    def run_all_workflows(self, env_vars: Dict[str, str] = None):
        """Run all workflows in sequence"""
        print("🔄 Running All Claude Flow Workflows")
        print("="*60)
        
        results = {}
        for name in self.config['workflows']:
            success = self.run_workflow(name, env_vars)
            results[name] = "✅ PASS" if success else "❌ FAIL"
        
        # Summary
        print("\n" + "="*60)
        print("📋 WORKFLOW SUMMARY")
        print("="*60)
        for name, status in results.items():
            print(f"{status}: {name}")
    
    def generate_ci_config(self, ci_system: str) -> str:
        """Generate CI/CD configuration for various systems"""
        if ci_system not in self.config.get('integrations', {}):
            return f"No configuration found for {ci_system}"
        
        return yaml.dump(self.config['integrations'][ci_system])

def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Claude Flow Runner for DevStress')
    parser.add_argument('workflow', nargs='?', help='Workflow name to run')
    parser.add_argument('--all', action='store_true', help='Run all workflows')
    parser.add_argument('--config', default='claudeflow.yaml', help='Configuration file')
    parser.add_argument('--env', action='append', help='Environment variables (KEY=VALUE)')
    parser.add_argument('--generate-ci', choices=['github-actions', 'jenkins', 'gitlab-ci'],
                       help='Generate CI/CD configuration')
    
    args = parser.parse_args()
    
    # Parse environment variables
    env_vars = {}
    if args.env:
        for env_str in args.env:
            if '=' in env_str:
                key, value = env_str.split('=', 1)
                env_vars[key] = value
    
    # Create runner
    runner = ClaudeFlowRunner(args.config)
    
    # Execute requested action
    if args.generate_ci:
        print(runner.generate_ci_config(args.generate_ci))
    elif args.all:
        runner.run_all_workflows(env_vars)
    elif args.workflow:
        success = runner.run_workflow(args.workflow, env_vars)
        sys.exit(0 if success else 1)
    else:
        print("Available workflows:")
        for name, workflow in runner.config['workflows'].items():
            desc = workflow.get('description', 'No description')
            print(f"  • {name}: {desc}")

if __name__ == "__main__":
    main()