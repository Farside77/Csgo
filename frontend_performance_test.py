#!/usr/bin/env python3
"""
CS2 Esports Tracker - Frontend Performance Test Tool

This script tests the performance of the CS2 Esports Tracker frontend, 
measuring load times and component rendering performance.
"""

import requests
import time
import statistics
import os
import json
from datetime import datetime
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Configuration
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
DEFAULT_ITERATIONS = 5

class FrontendPerformanceTester:
    def __init__(self, iterations=DEFAULT_ITERATIONS, verbose=False):
        self.iterations = iterations
        self.verbose = verbose
        self.results = {}
        
        print(f"Testing frontend at {FRONTEND_URL}")
        print(f"Iterations: {iterations}")
    
    def run_test(self, name, url):
        """Test frontend page load performance"""
        print(f"\n🔍 Testing {name}...")
        times = []
        sizes = []
        
        # Create session for connection reuse
        session = requests.Session()
        
        for i in range(self.iterations):
            try:
                start_time = time.time()
                response = session.get(url)
                elapsed = time.time() - start_time
                
                times.append(elapsed)
                sizes.append(len(response.content))
                
                status = "✅" if response.status_code == 200 else "❌"
                
                if self.verbose:
                    print(f"  {status} Iteration {i+1}/{self.iterations}: {elapsed:.4f}s")
                    print(f"    Page Size: {len(response.content)/1024:.2f} KB")
                else:
                    # Print dots to show progress
                    print(".", end="", flush=True)
                
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                times.append(None)
                sizes.append(None)
        
        if not self.verbose:
            print()  # Newline after dots
            
        # Calculate statistics
        valid_times = [t for t in times if t is not None]
        valid_sizes = [s for s in sizes if s is not None]
        
        if valid_times:
            avg_time = statistics.mean(valid_times)
            median_time = statistics.median(valid_times)
            min_time = min(valid_times)
            max_time = max(valid_times)
            
            avg_size = statistics.mean(valid_sizes) / 1024  # KB
            
            result = {
                "name": name,
                "url": url,
                "iterations": self.iterations,
                "success_rate": len(valid_times) / self.iterations * 100,
                "avg_time": avg_time,
                "median_time": median_time,
                "min_time": min_time,
                "max_time": max_time,
                "avg_size": avg_size
            }
            
            self.results[name] = result
            
            print(f"Results for {name}:")
            print(f"  Success Rate: {result['success_rate']:.1f}%")
            print(f"  Avg Load Time: {avg_time:.4f}s")
            print(f"  Median Load Time: {median_time:.4f}s")
            print(f"  Min/Max Load Time: {min_time:.4f}s / {max_time:.4f}s")
            print(f"  Avg Page Size: {avg_size:.2f} KB")
            
            # Performance rating
            if avg_time < 0.5:
                rating = "Excellent"
            elif avg_time < 1.0:
                rating = "Good"
            elif avg_time < 2.0:
                rating = "Acceptable"
            elif avg_time < 3.0:
                rating = "Slow"
            else:
                rating = "Very Slow"
                
            print(f"  Performance Rating: {rating}")
            
            # Analyze HTML content
            try:
                response = session.get(url)
                if response.status_code == 200:
                    self.analyze_html_content(response.text, name)
            except Exception as e:
                print(f"  ❌ Error analyzing HTML: {str(e)}")
            
        else:
            print("❌ All requests failed")
    
    def analyze_html_content(self, html_content, name):
        """Analyze HTML content for optimization opportunities"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Count elements by type
            scripts = soup.find_all('script')
            styles = soup.find_all('link', rel='stylesheet')
            images = soup.find_all('img')
            
            # Count inline styles and scripts
            inline_styles = soup.find_all('style')
            inline_scripts = [s for s in scripts if s.string]
            
            # Identify render-blocking resources
            head_scripts = soup.head.find_all('script') if soup.head else []
            render_blocking = len(head_scripts) + len(styles)
            
            analysis = {
                "external_scripts": len(scripts) - len(inline_scripts),
                "external_styles": len(styles),
                "inline_scripts": len(inline_scripts),
                "inline_styles": len(inline_styles),
                "images": len(images),
                "render_blocking": render_blocking
            }
            
            self.results[name]["analysis"] = analysis
            
            print(f"  Content Analysis:")
            print(f"    External Scripts: {analysis['external_scripts']}")
            print(f"    External Stylesheets: {analysis['external_styles']}")
            print(f"    Inline Scripts: {analysis['inline_scripts']}")
            print(f"    Inline Styles: {analysis['inline_styles']}")
            print(f"    Images: {analysis['images']}")
            print(f"    Render-Blocking Resources: {analysis['render_blocking']}")
            
            # Recommendations
            print(f"  Optimization Suggestions:")
            if analysis['render_blocking'] > 5:
                print(f"    • Reduce render-blocking resources")
            if analysis['external_scripts'] > 10:
                print(f"    • Consider bundling scripts")
            if analysis['external_styles'] > 3:
                print(f"    • Consider bundling stylesheets")
            if analysis['inline_scripts'] > 5:
                print(f"    • Move inline scripts to external files")
            if analysis['inline_styles'] > 3:
                print(f"    • Move inline styles to external stylesheet")
                
        except Exception as e:
            print(f"  ❌ Error in content analysis: {str(e)}")
    
    def print_summary(self):
        """Print a summary of all test results"""
        print("\n" + "="*80)
        print("CS2 ESPORTS TRACKER - FRONTEND PERFORMANCE SUMMARY")
        print("="*80)
        
        if not self.results:
            print("No tests were run successfully")
            return
        
        results_by_time = sorted(self.results.values(), key=lambda x: x.get("avg_time", float("inf")))
        
        print("\nPage Performance (from fastest to slowest):")
        for result in results_by_time:
            name = result["name"]
            avg_time = result.get("avg_time", float("inf"))
            avg_size = result.get("avg_size", 0)
            success_rate = result.get("success_rate", 0)
            
            if avg_time != float("inf"):
                print(f"  {name}: {avg_time:.4f}s ({avg_size:.2f} KB, {success_rate:.1f}% success)")
            else:
                print(f"  {name}: FAILED (0% success)")
        
        # Identify performance issues
        print("\nPotential Performance Issues:")
        slow_pages = [r for r in self.results.values() if r.get("avg_time", 0) > 2.0]
        large_pages = [r for r in self.results.values() if r.get("avg_size", 0) > 1000]  # >1MB
        
        if slow_pages:
            print("  Slow-loading pages:")
            for page in slow_pages:
                print(f"    • {page['name']}: {page.get('avg_time', 'N/A'):.4f}s")
        else:
            print("  • No slow-loading pages identified.")
            
        if large_pages:
            print("  Large pages:")
            for page in large_pages:
                print(f"    • {page['name']}: {page.get('avg_size', 'N/A'):.2f} KB")
        else:
            print("  • No excessively large pages identified.")
        
        # Overall assessment
        avg_times = [r.get("avg_time", float("inf")) for r in self.results.values() 
                    if r.get("avg_time", float("inf")) != float("inf")]
        if avg_times:
            overall_avg = statistics.mean(avg_times)
            
            if overall_avg < 0.5:
                rating = "Excellent"
            elif overall_avg < 1.0:
                rating = "Good"
            elif overall_avg < 2.0:
                rating = "Acceptable"
            elif overall_avg < 3.0:
                rating = "Needs Improvement"
            else:
                rating = "Poor - Significant Optimization Required"
                
            print(f"\nOverall Performance Rating: {rating} (Avg: {overall_avg:.4f}s)")
        else:
            print("\nOverall Performance Rating: Cannot be determined")
        
        # General recommendations
        print("\nGeneral Recommendations:")
        print("  • Ensure proper code splitting to reduce bundle size")
        print("  • Optimize image assets (compression, lazy loading)")
        print("  • Enable server-side caching for static resources")
        print("  • Consider using a CDN for static assets")
        print("  • Use production builds for React applications")
        
        print("\n" + "="*80)
        
    def save_results(self, filename="frontend_performance_results.json"):
        """Save results to a JSON file"""
        try:
            with open(filename, "w") as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "frontend_url": FRONTEND_URL,
                    "results": self.results
                }, f, indent=2)
            print(f"\nResults saved to {filename}")
        except Exception as e:
            print(f"\nError saving results: {str(e)}")
    
    def run_all_tests(self):
        """Run all available frontend tests"""
        # Main page test
        self.run_test("Main Page", FRONTEND_URL)
        
        # Print the test summary
        self.print_summary()
        
        # Save results to file
        self.save_results()

def main():
    parser = argparse.ArgumentParser(description="CS2 Esports Tracker Frontend Performance Test Tool")
    parser.add_argument("--iterations", "-i", type=int, default=DEFAULT_ITERATIONS,
                      help=f"Number of test iterations (default: {DEFAULT_ITERATIONS})")
    parser.add_argument("--verbose", "-v", action="store_true",
                      help="Enable verbose output")
    
    args = parser.parse_args()
    
    tester = FrontendPerformanceTester(
        iterations=args.iterations,
        verbose=args.verbose
    )
    
    tester.run_all_tests()

if __name__ == "__main__":
    main()