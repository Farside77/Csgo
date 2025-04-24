#!/usr/bin/env python3
"""
CS2 Esports Tracker - Backend Performance Test Tool

This script tests the performance of the CS2 Esports Tracker backend API endpoints,
measuring response times and identifying potential bottlenecks.
"""

import requests
import time
import statistics
import os
import uuid
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import argparse

# Configuration
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
DEFAULT_ITERATIONS = 10
DEFAULT_CONCURRENCY = 5

class BackendPerformanceTester:
    def __init__(self, iterations=DEFAULT_ITERATIONS, concurrency=DEFAULT_CONCURRENCY, verbose=False):
        self.iterations = iterations
        self.concurrency = concurrency
        self.verbose = verbose
        self.results = {}
        
        print(f"Testing backend at {BACKEND_URL}")
        print(f"Iterations: {iterations}, Concurrency: {concurrency}")
        
    def run_test(self, name, url, method="GET", data=None, headers=None):
        """Run a test against a specific endpoint"""
        print(f"\n🔍 Testing {name}...")
        times = []
        
        if not headers:
            headers = {"Content-Type": "application/json"}
        
        # Create session for connection reuse
        session = requests.Session()
        
        for i in range(self.iterations):
            try:
                start_time = time.time()
                
                if method == "GET":
                    response = session.get(url, headers=headers)
                elif method == "POST":
                    response = session.post(url, json=data, headers=headers)
                elif method == "PUT":
                    response = session.put(url, json=data, headers=headers)
                else:
                    raise ValueError(f"Unsupported method: {method}")
                
                elapsed = time.time() - start_time
                times.append(elapsed)
                
                status = "✅" if response.status_code == 200 else "❌"
                
                if self.verbose:
                    print(f"  {status} Iteration {i+1}/{self.iterations}: {elapsed:.4f}s")
                else:
                    # Print dots to show progress
                    print(".", end="", flush=True)
                    
                # If GET request, check data size
                if method == "GET" and response.status_code == 200:
                    data_size = len(response.content)
                    if self.verbose:
                        print(f"    Response size: {data_size/1024:.2f} KB")
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                times.append(None)
        
        if not self.verbose:
            print()  # Newline after dots
            
        # Calculate statistics
        valid_times = [t for t in times if t is not None]
        if valid_times:
            avg_time = statistics.mean(valid_times)
            median_time = statistics.median(valid_times)
            min_time = min(valid_times)
            max_time = max(valid_times)
            p95_time = sorted(valid_times)[int(len(valid_times) * 0.95) - 1] if len(valid_times) >= 20 else max_time
            
            result = {
                "name": name,
                "url": url,
                "method": method,
                "iterations": self.iterations,
                "success_rate": len(valid_times) / self.iterations * 100,
                "avg_time": avg_time,
                "median_time": median_time,
                "min_time": min_time,
                "max_time": max_time,
                "p95_time": p95_time
            }
            
            self.results[name] = result
            
            print(f"Results for {name}:")
            print(f"  Success Rate: {result['success_rate']:.1f}%")
            print(f"  Avg Response Time: {avg_time:.4f}s")
            print(f"  Median Response Time: {median_time:.4f}s")
            print(f"  Min/Max Response Time: {min_time:.4f}s / {max_time:.4f}s")
            print(f"  P95 Response Time: {p95_time:.4f}s")
            
            # Performance rating
            if avg_time < 0.1:
                rating = "Excellent"
            elif avg_time < 0.3:
                rating = "Good"
            elif avg_time < 0.5:
                rating = "Acceptable"
            elif avg_time < 1.0:
                rating = "Slow"
            else:
                rating = "Very Slow"
                
            print(f"  Performance Rating: {rating}")
            
        else:
            print("❌ All requests failed")
    
    def run_concurrent_test(self, name, url, method="GET", data_generator=None, headers=None):
        """Run a concurrent test against a specific endpoint"""
        print(f"\n🔍 Testing {name} with {self.concurrency} concurrent users...")
        start_time = time.time()
        
        if not headers:
            headers = {"Content-Type": "application/json"}
            
        # Create session for connection reuse
        session = requests.Session()
        
        def make_request(i):
            try:
                req_start = time.time()
                
                # Generate unique data for each request if needed
                if data_generator:
                    data = data_generator(i)
                else:
                    data = None
                
                if method == "GET":
                    response = session.get(url, headers=headers)
                elif method == "POST":
                    response = session.post(url, json=data, headers=headers)
                elif method == "PUT":
                    response = session.put(url, json=data, headers=headers)
                else:
                    raise ValueError(f"Unsupported method: {method}")
                
                elapsed = time.time() - req_start
                
                return {
                    "iteration": i,
                    "status_code": response.status_code,
                    "time": elapsed,
                    "success": response.status_code == 200
                }
            except Exception as e:
                return {
                    "iteration": i, 
                    "error": str(e),
                    "time": None,
                    "success": False
                }
        
        with ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            results = list(executor.map(make_request, range(self.iterations)))
        
        total_time = time.time() - start_time
        success_count = sum(1 for r in results if r["success"])
        success_rate = success_count / self.iterations * 100
        
        # Calculate statistics from successful requests
        times = [r["time"] for r in results if r["time"] is not None]
        if times:
            avg_time = statistics.mean(times)
            median_time = statistics.median(times)
            min_time = min(times)
            max_time = max(times)
            p95_time = sorted(times)[int(len(times) * 0.95) - 1] if len(times) >= 20 else max_time
            
            throughput = self.iterations / total_time
            
            result = {
                "name": name,
                "url": url,
                "method": method,
                "iterations": self.iterations,
                "concurrency": self.concurrency,
                "success_rate": success_rate,
                "total_time": total_time,
                "throughput": throughput,
                "avg_time": avg_time,
                "median_time": median_time,
                "min_time": min_time,
                "max_time": max_time,
                "p95_time": p95_time
            }
            
            self.results[f"{name}_concurrent"] = result
            
            print(f"Results for {name} (Concurrent):")
            print(f"  Success Rate: {success_rate:.1f}%")
            print(f"  Total Time: {total_time:.2f}s")
            print(f"  Throughput: {throughput:.2f} requests/second")
            print(f"  Avg Response Time: {avg_time:.4f}s")
            print(f"  Median Response Time: {median_time:.4f}s")
            print(f"  Min/Max Response Time: {min_time:.4f}s / {max_time:.4f}s")
            print(f"  P95 Response Time: {p95_time:.4f}s")
            
            # Throughput rating
            if throughput > 50:
                rating = "Excellent"
            elif throughput > 20:
                rating = "Good"
            elif throughput > 10:
                rating = "Acceptable"
            elif throughput > 5:
                rating = "Poor"
            else:
                rating = "Very Poor"
                
            print(f"  Throughput Rating: {rating}")
            
        else:
            print("❌ All concurrent requests failed")
    
    def print_summary(self):
        """Print a summary of all test results"""
        print("\n" + "="*80)
        print("CS2 ESPORTS TRACKER - BACKEND PERFORMANCE SUMMARY")
        print("="*80)
        
        if not self.results:
            print("No tests were run successfully")
            return
        
        results_by_time = sorted(self.results.values(), key=lambda x: x.get("avg_time", float("inf")))
        
        print("\nEndpoint Performance (from fastest to slowest):")
        for result in results_by_time:
            name = result["name"]
            method = result["method"]
            avg_time = result.get("avg_time", float("inf"))
            success_rate = result.get("success_rate", 0)
            
            if avg_time != float("inf"):
                print(f"  {method} {name}: {avg_time:.4f}s ({success_rate:.1f}% success)")
            else:
                print(f"  {method} {name}: FAILED (0% success)")
        
        # Identify bottlenecks
        print("\nPotential Bottlenecks:")
        bottlenecks = [r for r in self.results.values() if r.get("avg_time", 0) > 0.5]
        if bottlenecks:
            for bottleneck in bottlenecks:
                print(f"  • {bottleneck['method']} {bottleneck['name']}: {bottleneck.get('avg_time', 'N/A'):.4f}s")
        else:
            print("  No significant bottlenecks identified.")
        
        # Throughput summary
        concurrent_results = [r for r in self.results.values() if "concurrency" in r]
        if concurrent_results:
            print("\nThroughput Summary:")
            for result in concurrent_results:
                name = result["name"]
                method = result["method"]
                throughput = result.get("throughput", 0)
                print(f"  {method} {name}: {throughput:.2f} requests/second")
        
        # Overall assessment
        avg_times = [r.get("avg_time", float("inf")) for r in self.results.values() 
                    if r.get("avg_time", float("inf")) != float("inf")]
        if avg_times:
            overall_avg = statistics.mean(avg_times)
            
            if overall_avg < 0.1:
                rating = "Excellent"
            elif overall_avg < 0.3:
                rating = "Good"
            elif overall_avg < 0.5:
                rating = "Acceptable"
            elif overall_avg < 1.0:
                rating = "Needs Improvement"
            else:
                rating = "Poor - Significant Optimization Required"
                
            print(f"\nOverall Performance Rating: {rating} (Avg: {overall_avg:.4f}s)")
        else:
            print("\nOverall Performance Rating: Cannot be determined")
        
        print("\nRecommendations:")
        if bottlenecks:
            print("  • Optimize the identified bottleneck endpoints")
            print("  • Consider adding caching for expensive calculations")
            print("  • Check database query performance for slow endpoints")
        else:
            print("  • The backend performance is satisfactory")
            print("  • Consider adding response compression for larger responses")
            print("  • Set up monitoring to track performance over time")
        
        print("\n" + "="*80)
        
    def save_results(self, filename="performance_results.json"):
        """Save results to a JSON file"""
        try:
            with open(filename, "w") as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "backend_url": BACKEND_URL,
                    "results": self.results
                }, f, indent=2)
            print(f"\nResults saved to {filename}")
        except Exception as e:
            print(f"\nError saving results: {str(e)}")
    
    def run_all_tests(self):
        """Run all available tests"""
        # Test API root
        self.run_test("API Root", f"{BACKEND_URL}/api")
        
        # Test getting matches
        self.run_test("Get Matches", f"{BACKEND_URL}/api/matches")
        self.run_test("Get Matches - Filtered", f"{BACKEND_URL}/api/matches?status=upcoming")
        
        # Test getting bets
        self.run_test("Get Bets", f"{BACKEND_URL}/api/bets")
        
        # Refresh matches
        self.run_test("Refresh Matches", f"{BACKEND_URL}/api/refresh-matches", method="POST")
        
        # Concurrent match fetching
        self.run_concurrent_test("Get Matches", f"{BACKEND_URL}/api/matches")
        
        # Bet creation performance
        def generate_bet_data(i):
            # Generate a unique match ID for each bet
            match_id = str(uuid.uuid4())
            return {
                "match_id": match_id,
                "team_bet_on": f"Team {i % 2 + 1}",
                "odds": 1.5 + (i % 5) / 10,
                "stake": 100 + i
            }
            
        self.run_concurrent_test("Create Bet", f"{BACKEND_URL}/api/bets", 
                                method="POST", data_generator=generate_bet_data)
        
        # Print the test summary
        self.print_summary()
        
        # Save results to file
        self.save_results()

def main():
    parser = argparse.ArgumentParser(description="CS2 Esports Tracker Backend Performance Test Tool")
    parser.add_argument("--iterations", "-i", type=int, default=DEFAULT_ITERATIONS,
                        help=f"Number of test iterations (default: {DEFAULT_ITERATIONS})")
    parser.add_argument("--concurrency", "-c", type=int, default=DEFAULT_CONCURRENCY,
                        help=f"Number of concurrent users for load testing (default: {DEFAULT_CONCURRENCY})")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable verbose output")
    
    args = parser.parse_args()
    
    tester = BackendPerformanceTester(
        iterations=args.iterations,
        concurrency=args.concurrency,
        verbose=args.verbose
    )
    
    tester.run_all_tests()

if __name__ == "__main__":
    main()