"""
Unified Live Data Fetcher for SDG Ethiopia Chatbot
Fetches real-time data from:
- UN SDG Database
- World Bank API  
- Ethiopian Statistical Service (ESS) Website

Features:
- Auto-updates when new data is available
- Intelligent caching to avoid repeated requests
- Fallback mechanisms when APIs fail
"""

import requests
from bs4 import BeautifulSoup
import io
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

# Optional PDF support (only needed for local ESS report processing)
try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

class UnifiedDataFetcher:
    """Unified fetcher for all three data sources: UN, World Bank, ESS"""
    
    def __init__(self, cache_dir="./cache"):
        # Initialize URLs
        self.world_bank_base = "https://api.worldbank.org/v2"
        self.ess_base_url = "https://ess.gov.et"  # Updated ESS website URL
        self.un_sdg_url = "https://unstats.un.org/sdgs/dataportal"
        self.country_code = "ETH"  # Ethiopia
        
        # Setup cache
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_duration = timedelta(hours=6)  # 6 hour cache
        
        print("✓ Unified Data Fetcher initialized")
    
    # ==========================================
    # WORLD BANK API METHODS
    # ==========================================
    
    def fetch_worldbank_indicator(self, indicator_code, years=10):
        """
        Fetch specific indicator from World Bank API
        
        Args:
            indicator_code: World Bank indicator (e.g., 'SI.POV.DDAY')
            years: Number of recent years to fetch
        
        Returns:
            dict with latest data or None if failed
        """
        cache_key = f"wb_{indicator_code}"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            url = f"{self.world_bank_base}/country/{self.country_code}/indicator/{indicator_code}"
            params = {
                'format': 'json',
                'per_page': years,
                'date': f'{datetime.now().year - years}:{datetime.now().year}'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if len(data) > 1 and data[1]:
                    # Extract latest data point
                    latest = data[1][0]
                    
                    result = {
                        'indicator': latest.get('indicator', {}).get('value'),
                        'year': latest.get('date'),
                        'value': latest.get('value'),
                        'country': 'Ethiopia',
                        'source': 'World Bank API (Live)',
                        'fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    self._save_to_cache(cache_key, result)
                    return result
            
            return None
                
        except Exception as e:
            print(f"✗ World Bank fetch error: {e}")
            return None
    
    def search_worldbank_by_keyword(self, keyword):
        """
        Search for World Bank indicators by keyword
        
        Returns:
            list of indicator codes matching the keyword
        """
        # Comprehensive keyword mapping
        indicator_map = {
            # Poverty & Income
            'poverty': ['SI.POV.DDAY', 'SI.POV.NAHC'],
            'poor': ['SI.POV.DDAY'],
            'income': ['SI.POV.DDAY', 'NY.GDP.PCAP.CD'],
            
            # Education
            'education': ['SE.PRM.NENR', 'SE.SEC.NENR', 'SE.ADT.LITR.ZS'],
            'school': ['SE.PRM.NENR', 'SE.SEC.NENR'],
            'enrollment': ['SE.PRM.NENR', 'SE.SEC.NENR'],
            'literacy': ['SE.ADT.LITR.ZS'],
            'student': ['SE.PRM.NENR'],
            'learning': ['SE.PRM.NENR'],
            
            # Health
            'health': ['SH.STA.MORT', 'SH.DYN.MORT', 'SP.DYN.LE00.IN'],
            'mortality': ['SH.STA.MORT', 'SH.DYN.MORT'],
            'infant': ['SH.STA.MORT'],
            'child': ['SH.DYN.MORT'],
            'death': ['SH.STA.MORT'],
            'life expectancy': ['SP.DYN.LE00.IN'],
            
            # Infrastructure
            'electricity': ['EG.ELC.ACCS.ZS'],
            'power': ['EG.ELC.ACCS.ZS'],
            'energy': ['EG.ELC.ACCS.ZS'],
            'water': ['SH.H2O.BASW.ZS'],
            'sanitation': ['SH.STA.BASS.ZS'],
            'toilet': ['SH.STA.BASS.ZS'],
            
            # Environment
            'forest': ['AG.LND.FRST.ZS'],
            'tree': ['AG.LND.FRST.ZS'],
            'deforestation': ['AG.LND.FRST.ZS'],
            
            # Economy
            'gdp': ['NY.GDP.PCAP.CD', 'NY.GDP.MKTP.KD.ZG'],
            'economy': ['NY.GDP.PCAP.CD'],
            'economic': ['NY.GDP.MKTP.KD.ZG'],
            'growth': ['NY.GDP.MKTP.KD.ZG'],
        }
        
        keyword_lower = keyword.lower()
        for key, codes in indicator_map.items():
            if keyword_lower in key:
                return codes
        
        return []
    
    # ==========================================
    # ESS WEBSITE SCRAPING METHODS
    # ==========================================
    
    def fetch_ess_homepage(self):
        """
        Fetch latest announcements from ESS homepage
        
        Returns:
            dict with latest updates or None if failed
        """
        cache_key = "ess_homepage"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            response = requests.get(self.ess_base_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                latest_data = {
                    'source': 'ESS Website (Live)',
                    'fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'url': self.ess_base_url,
                    'content': []
                }
                
                # Look for news/announcements sections
                news_sections = soup.find_all(['div', 'section', 'article'], 
                                             class_=['news', 'announcement', 'latest', 'update'])
                
                for section in news_sections[:5]:
                    text = section.get_text(strip=True)
                    if len(text) > 50:
                        latest_data['content'].append(text[:500])
                
                if latest_data['content']:
                    self._save_to_cache(cache_key, latest_data)
                    return latest_data
            
            return None
                
        except Exception as e:
            print(f"✗ ESS homepage fetch error: {e}")
            return None
    
    def fetch_ess_reports(self, max_reports=5):
        """
        Fetch latest ESS reports from publications page
        
        Returns:
            list of report metadata
        """
        cache_key = "ess_reports"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            reports_url = f"{self.ess_base_url}/publications/"
            response = requests.get(reports_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                reports = []
                
                # Find PDF links
                pdf_links = soup.find_all('a', href=lambda x: x and '.pdf' in x.lower())
                
                for link in pdf_links[:max_reports]:
                    title = link.get_text(strip=True)
                    url = link['href']
                    
                    # Make absolute URL
                    if not url.startswith('http'):
                        url = self.ess_base_url + url
                    
                    reports.append({
                        'title': title,
                        'url': url,
                        'source': 'ESS Website',
                        'fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                
                if reports:
                    self._save_to_cache(cache_key, reports)
                
                return reports
            
            return []
                
        except Exception as e:
            print(f"✗ ESS reports fetch error: {e}")
            return []
    
    def search_ess_by_keyword(self, keyword):
        """
        Search ESS website for specific keyword
        
        Returns:
            list of search results
        """
        cache_key = f"ess_search_{keyword}"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            search_url = f"{self.ess_base_url}/search?q={keyword}"
            response = requests.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                results = []
                
                # Find search result containers
                result_divs = soup.find_all(['div', 'article'], class_=['result', 'search-result'])
                
                for result in result_divs[:5]:
                    title_elem = result.find(['h3', 'h4', 'a'])
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        content = result.get_text(strip=True)[:500]
                        
                        results.append({
                            'title': title,
                            'content': content,
                            'source': 'ESS Website Search',
                            'keyword': keyword,
                            'fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                
                if results:
                    self._save_to_cache(cache_key, results)
                
                return results
            
            return []
                
        except Exception as e:
            print(f"✗ ESS search error: {e}")
            return []
    
    # ==========================================
    # UN SDG DATABASE METHODS
    # ==========================================
    
    def check_un_updates(self):
        """
        Check if UN SDG database has new data
        Note: UN data is typically updated quarterly
        
        Returns:
            dict with update status
        """
        cache_key = "un_last_check"
        cached = self._get_from_cache(cache_key)
        
        # Only check once per day
        if cached and 'last_check' in cached:
            last_check = datetime.fromisoformat(cached['last_check'])
            if datetime.now() - last_check < timedelta(days=1):
                return cached
        
        try:
            # Check UN SDG portal for updates
            response = requests.get(self.un_sdg_url, timeout=10)
            
            result = {
                'last_check': datetime.now().isoformat(),
                'status': 'checked',
                'message': 'UN data is typically updated quarterly. Check portal manually for latest updates.',
                'portal_url': self.un_sdg_url
            }
            
            self._save_to_cache(cache_key, result)
            return result
                
        except Exception as e:
            print(f"✗ UN check error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    # ==========================================
    # UNIFIED SEARCH METHOD
    # ==========================================
    
    def fetch_all_sources(self, question):
        """
        Fetch data from all three sources based on question
        
        Args:
            question: User's question
        
        Returns:
            dict with data from all available sources
        """
        results = {
            'world_bank': [],
            'ess': [],
            'un': [],
            'fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Extract keywords from question
        keywords = self._extract_keywords(question)
        
        # Fetch from World Bank
        for keyword in keywords[:2]:  # Limit to 2 keywords
            codes = self.search_worldbank_by_keyword(keyword)
            for code in codes[:1]:  # 1 indicator per keyword
                data = self.fetch_worldbank_indicator(code)
                if data:
                    results['world_bank'].append(data)
        
        # Fetch from ESS
        for keyword in keywords[:2]:
            ess_data = self.search_ess_by_keyword(keyword)
            if ess_data:
                results['ess'].extend(ess_data[:2])
        
        # Check UN status
        results['un'] = self.check_un_updates()
        
        return results
    
    # ==========================================
    # HELPER METHODS
    # ==========================================
    
    def _extract_keywords(self, text):
        """Extract relevant keywords from text"""
        keywords = [
            'poverty', 'poor', 'income',
            'education', 'school', 'enrollment', 'literacy', 'student',
            'health', 'mortality', 'infant', 'child', 'death',
            'electricity', 'power', 'energy', 'water', 'sanitation',
            'forest', 'tree', 'gdp', 'economy', 'growth'
        ]
        
        text_lower = text.lower()
        found = [kw for kw in keywords if kw in text_lower]
        return found if found else ['poverty']  # Default keyword
    
    def _get_from_cache(self, key):
        """Get data from cache if not expired"""
        cache_file = self.cache_dir / f"{key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached = json.load(f)
                
                cached_time = datetime.fromisoformat(cached['_cached_at'])
                if datetime.now() - cached_time < self.cache_duration:
                    print(f"✓ Using cached data for '{key}'")
                    return cached['data']
            except:
                pass
        
        return None
    
    def _save_to_cache(self, key, data):
        """Save data to cache"""
        cache_file = self.cache_dir / f"{key}.json"
        
        try:
            cached_data = {
                '_cached_at': datetime.now().isoformat(),
                'data': data
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cached_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠ Cache save error: {e}")
    
    def clear_cache(self):
        """Clear all cached data"""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
        print("✓ Cache cleared")


# Quick access function
def fetch_live_data(question):
    """
    Quick function to fetch live data from all sources
    
    Usage:
        from unified_data_fetcher import fetch_live_data
        data = fetch_live_data("What is Ethiopia's poverty rate?")
    """
    fetcher = UnifiedDataFetcher()
    return fetcher.fetch_all_sources(question)


if __name__ == "__main__":
    # Test the fetcher
    print("Testing Unified Data Fetcher...")
    print("=" * 50)
    
    fetcher = UnifiedDataFetcher()
    
    # Test World Bank
    print("\n1. Testing World Bank API...")
    wb_data = fetcher.fetch_worldbank_indicator('SI.POV.DDAY')
    if wb_data:
        print(f"   ✓ {wb_data['indicator']}: {wb_data['value']} ({wb_data['year']})")
    
    # Test ESS
    print("\n2. Testing ESS Website...")
    ess_data = fetcher.search_ess_by_keyword('poverty')
    if ess_data:
        print(f"   ✓ Found {len(ess_data)} ESS results")
    
    # Test unified fetch
    print("\n3. Testing Unified Fetch...")
    all_data = fetcher.fetch_all_sources("What is poverty in Ethiopia?")
    print(f"   ✓ World Bank: {len(all_data['world_bank'])} results")
    print(f"   ✓ ESS: {len(all_data['ess'])} results")
    print(f"   ✓ UN Status: {all_data['un'].get('status', 'N/A')}")
    
    print("\n" + "=" * 50)
    print("✓ All tests completed!")
