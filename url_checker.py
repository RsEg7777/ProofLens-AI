"""
ProofLens AI - URL Reputation Checker
Uses VirusTotal API to check URLs for malware, phishing, and other threats
"""

import requests
import time
from config import Config
from typing import Dict, Any


class URLReputationChecker:
    """Check URL reputation using VirusTotal API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.VIRUSTOTAL_API_KEY
        self.base_url = "https://www.virustotal.com/api/v3"
        self.headers = {
            "x-apikey": self.api_key,
            "Accept": "application/json"
        }
    
    def check_url(self, url: str) -> Dict[str, Any]:
        """
        Check a URL's reputation using VirusTotal
        
        Args:
            url: The URL to check
            
        Returns:
            Dictionary with reputation analysis
        """
        try:
            # Step 1: Submit URL for scanning
            scan_id = self._submit_url(url)
            
            if not scan_id:
                return self._create_error_response("Failed to submit URL for scanning")
            
            # Step 2: Wait a bit for analysis to complete
            time.sleep(2)
            
            # Step 3: Get analysis results
            analysis = self._get_analysis(scan_id)
            
            if not analysis:
                return self._create_error_response("Failed to retrieve analysis results")
            
            # Step 4: Parse and return results
            return self._parse_results(url, analysis)
            
        except Exception as e:
            return self._create_error_response(f"Error checking URL: {str(e)}")
    
    def _submit_url(self, url: str) -> str:
        """Submit URL to VirusTotal for scanning"""
        try:
            endpoint = f"{self.base_url}/urls"
            data = {"url": url}
            
            response = requests.post(
                endpoint,
                headers=self.headers,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                # Extract the analysis ID
                return result.get('data', {}).get('id')
            else:
                print(f"VirusTotal submit error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error submitting URL: {str(e)}")
            return None
    
    def _get_analysis(self, analysis_id: str) -> Dict[str, Any]:
        """Get analysis results from VirusTotal"""
        try:
            endpoint = f"{self.base_url}/analyses/{analysis_id}"
            
            response = requests.get(
                endpoint,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"VirusTotal analysis error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error getting analysis: {str(e)}")
            return None
    
    def _parse_results(self, url: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Parse VirusTotal analysis results into a standardized format"""
        try:
            data = analysis.get('data', {})
            attributes = data.get('attributes', {})
            stats = attributes.get('stats', {})
            results = attributes.get('results', {})
            
            # Count detections
            malicious = stats.get('malicious', 0)
            suspicious = stats.get('suspicious', 0)
            harmless = stats.get('harmless', 0)
            undetected = stats.get('undetected', 0)
            total_scans = malicious + suspicious + harmless + undetected
            
            # Calculate threat score (0-100)
            if total_scans > 0:
                threat_score = int(((malicious + suspicious * 0.5) / total_scans) * 100)
            else:
                threat_score = 0
            
            # Determine if URL is safe
            is_safe = malicious == 0 and suspicious <= 1
            
            # Extract categories
            categories = self._extract_categories(results)
            
            # Extract threats found
            threats = self._extract_threats(results, malicious, suspicious)
            
            # Create status message
            if is_safe:
                status = "Safe"
                status_message = "No threats detected by security vendors"
            elif malicious > 5:
                status = "Dangerous"
                status_message = f"Flagged as malicious by {malicious} security vendors"
            elif malicious > 0:
                status = "Suspicious"
                status_message = f"Flagged by {malicious} security vendors"
            else:
                status = "Suspicious"
                status_message = f"Flagged as suspicious by {suspicious} security vendors"
            
            return {
                'url': url,
                'is_safe': is_safe,
                'status': status,
                'status_message': status_message,
                'threat_score': threat_score,
                'scan_stats': {
                    'malicious': malicious,
                    'suspicious': suspicious,
                    'harmless': harmless,
                    'undetected': undetected,
                    'total': total_scans
                },
                'categories': categories,
                'threats': threats,
                'scan_date': attributes.get('date', int(time.time()))
            }
            
        except Exception as e:
            print(f"Error parsing results: {str(e)}")
            return self._create_error_response(f"Failed to parse analysis results: {str(e)}")
    
    def _extract_categories(self, results: Dict[str, Any]) -> list:
        """Extract threat categories from scan results"""
        categories = set()
        
        for vendor_name, vendor_result in results.items():
            if isinstance(vendor_result, dict):
                category = vendor_result.get('category', '')
                result = vendor_result.get('result', '')
                
                if category and category != 'harmless' and category != 'undetected':
                    categories.add(category)
                
                # Also extract result types
                if result and result != 'clean':
                    categories.add(result)
        
        return list(categories)[:10]  # Limit to top 10 categories
    
    def _extract_threats(self, results: Dict[str, Any], malicious: int, suspicious: int) -> list:
        """Extract specific threat detections"""
        threats = []
        
        for vendor_name, vendor_result in results.items():
            if isinstance(vendor_result, dict):
                category = vendor_result.get('category', '')
                result = vendor_result.get('result', '')
                
                # Only include malicious or suspicious detections
                if category in ['malicious', 'suspicious']:
                    threats.append({
                        'vendor': vendor_name,
                        'category': category,
                        'result': result or 'Threat detected'
                    })
        
        # Sort by severity (malicious first)
        threats.sort(key=lambda x: 0 if x['category'] == 'malicious' else 1)
        
        return threats[:15]  # Limit to top 15 threats
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create a standardized error response"""
        return {
            'url': '',
            'is_safe': False,
            'status': 'Error',
            'status_message': error_message,
            'threat_score': 0,
            'scan_stats': {
                'malicious': 0,
                'suspicious': 0,
                'harmless': 0,
                'undetected': 0,
                'total': 0
            },
            'categories': [],
            'threats': [],
            'error': error_message
        }
    
    def get_url_report(self, url: str) -> Dict[str, Any]:
        """
        Get existing report for a URL without re-scanning
        Useful for frequently checked URLs
        """
        try:
            # URL-encode the URL
            import urllib.parse
            url_id = urllib.parse.quote_plus(url)
            
            endpoint = f"{self.base_url}/urls/{url_id}"
            
            response = requests.get(
                endpoint,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_results(url, {'data': data.get('data', {})})
            else:
                # If no existing report, do a fresh scan
                return self.check_url(url)
                
        except Exception as e:
            print(f"Error getting URL report: {str(e)}")
            return self.check_url(url)


def check_url_reputation(url: str) -> Dict[str, Any]:
    """
    Convenience function to check URL reputation
    
    Args:
        url: The URL to check
        
    Returns:
        Dictionary with reputation analysis
    """
    checker = URLReputationChecker()
    return checker.check_url(url)


def expand_shortened_url(short_url: str) -> str:
    """
    Expand a shortened URL to its full form
    
    Args:
        short_url: The shortened URL (e.g., bit.ly, tinyurl)
        
    Returns:
        Full expanded URL or original URL if expansion fails
    """
    try:
        response = requests.head(
            short_url,
            allow_redirects=True,
            timeout=10
        )
        return response.url
    except Exception as e:
        print(f"Error expanding URL: {str(e)}")
        return short_url
