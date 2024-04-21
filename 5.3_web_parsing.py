import requests
from bs4 import BeautifulSoup

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls

def extract_details(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Title
        product_main_div = soup.find('div', class_='product_main')
        title = product_main_div.find('h1').text.strip()
        # UPC
        upc_th = soup.find('th', string='UPC')
        upc = upc_th.find_next_sibling('td').string.strip()
        # Availability
        availability_th = soup.find('th', string='Availability')
        availability = availability_th.find_next_sibling('td').string.strip()

        return {
            'Title': title,
            'UPC': upc,
            'Availability': availability
        }

def extract_book_information(file_path):
    urls = read_urls_from_file(file_path)
    product_details = []
    
    for url in urls:
        details = extract_details(url)
        if details:
            product_details.append(details)
            print(details)

if __name__ == "__main__":
    file_path = 'all_book_urls.txt' 
    extract_book_information(file_path)
