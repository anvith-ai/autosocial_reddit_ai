import requests
from bs4 import BeautifulSoup

class ContentScraper:
    def scrape_url_content(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text()
            content = content.strip()
            content = ' '.join(content.split())
            return content
        except requests.exceptions.RequestException as e:
            print(f"Error scraping URL: {url} - {str(e)}")
            return ""