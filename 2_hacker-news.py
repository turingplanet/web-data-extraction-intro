import requests
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com/"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')
titlelines = soup.find_all('span', class_='titleline')
# Iterate through each article and extract title and link
for titleline in titlelines:
    hyperlink_tag = titleline.find('a')
    title = hyperlink_tag.text
    link = hyperlink_tag['href']
    print(f"Title: {title}\nLink: {link}\n")
