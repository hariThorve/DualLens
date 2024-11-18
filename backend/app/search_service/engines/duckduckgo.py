from .base import SearchEngine
from ..models.search import SearchResult
from typing import List
import aiohttp
from bs4 import BeautifulSoup
import logging
from urllib.parse import quote

class DuckDuckGoEngine(SearchEngine):
    BASE_URL = "https://html.duckduckgo.com/html/"
    
    def format_url(self, url: str) -> str:
        """Ensure URL has proper format with http/https"""
        if url and not url.startswith(('http://', 'https://')):
            return f'https://{url}'
        return url

    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        try:
            encoded_query = quote(query)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.BASE_URL,
                    data={"q": encoded_query},
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                ) as response:
                    if response.status != 200:
                        logging.error(f"Search failed with status {response.status}")
                        return []
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    for result in soup.select('.result'):
                        if len(results) >= max_results:
                            break
                            
                        title_elem = result.select_one('.result__title')
                        link_elem = result.select_one('.result__url')
                        snippet_elem = result.select_one('.result__snippet')
                        
                        if title_elem and link_elem:
                            url = self.format_url(link_elem.get_text(strip=True))
                            
                            try:
                                results.append(
                                    SearchResult(
                                        title=title_elem.get_text(strip=True),
                                        url=url,
                                        description=snippet_elem.get_text(strip=True) if snippet_elem else None,
                                        content=None
                                    )
                                )
                            except Exception as e:
                                logging.error(f"Failed to create SearchResult: {str(e)}")
                                continue
                    
                    return results
                    
        except Exception as e:
            logging.error(f"Search error: {str(e)}")
            return []

    async def extract_content(self, url: str) -> str:
        """Extract main content from a webpage"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    },
                    timeout=10
                ) as response:
                    if response.status != 200:
                        logging.error(f"Failed to fetch content: Status {response.status}")
                        return ""

                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    # Remove unwanted elements
                    for element in soup.select('script, style, nav, header, footer, iframe, ads'):
                        element.decompose()

                    # Try to find main content
                    main_content = soup.select_one('main, article, #content, .content')
                    if main_content:
                        content = main_content.get_text(separator=' ', strip=True)
                    else:
                        # Fallback to body content
                        content = soup.get_text(separator=' ', strip=True)

                    # Clean up the text
                    content = ' '.join(content.split())
                    return content[:5000]  # Limit content length

        except Exception as e:
            logging.error(f"Content extraction error for {url}: {str(e)}")
            return ""