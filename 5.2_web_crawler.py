# https://books.toscrape.com/index.html
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_page_content(url):
    """Fetch the HTML content of a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response is an error response
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_book_urls(html_content, base_url):
    """Extract book URLs from the given HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    return [urljoin(base_url, article.find('h3').find('a')['href']) for article in soup.find_all('article', class_='product_pod')]

def find_next_page(html_content, base_url):
    """Find the URL of the next page from the given HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    next_button = soup.find('li', class_='next')
    if next_button:
        return urljoin(base_url, next_button.find('a')['href'])
    return None

def crawl_all_book_urls(start_url):
    """Crawl all pages to collect book URLs."""
    book_urls = []
    current_page_url = start_url
    while current_page_url:
        print(f"Fetching {current_page_url}")
        html_content = fetch_page_content(current_page_url)
        if html_content:
            book_urls.extend(extract_book_urls(html_content, current_page_url))
            current_page_url = find_next_page(html_content, current_page_url)
        else:
            break
    return book_urls

def save_urls_to_file(urls, file_path):
    with open(file_path, 'w') as file:
        for url in urls:
            file.write(url + '\n')

# Starting URL of the site
base_url = 'https://books.toscrape.com/index.html'
# Crawl the website and collect book URLs
all_book_urls = crawl_all_book_urls(base_url)
# Output the collected book URLs
for url in all_book_urls:
    print(url)

print(f"Total book URLs found: {len(all_book_urls)}")

file_path = 'all_book_urls.txt'
save_urls_to_file(all_book_urls, file_path)

