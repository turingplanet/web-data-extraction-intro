import asyncio
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from util import load_config

config = load_config('config.yml')
OPENAI_KEY = config['open_ai']['key']

async def run_playwright(site):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) # if True, may get the error: This browser is no longer supported. Please switch to a supported browser to continue using twitter.com. You can see a list of supported browsers in our He....
        # browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        # Set a timeout for navigating to the page
        try:
            # await page.goto(site, wait_until='load', timeout=20000) # 10 secs
            # await page.goto(site, wait_until='load')
            await page.goto(site, wait_until='networkidle')
        except TimeoutError:
            print("Timeout reached during page load, proceeding with available content.")
        page_source = await page.content()
        soup = BeautifulSoup(page_source, "html.parser")
        for script in soup(["script", "style"]): # Remove all javascript and stylesheet code
            script.extract()
        text = soup.get_text()
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines()) 
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) 
        data = '\n'.join(chunk for chunk in chunks if chunk) # Drop blank lines
        await browser.close()
    return data

GPT_4 = 'gpt-4'
llm = ChatOpenAI(temperature=0, model=GPT_4, openai_api_key=OPENAI_KEY)

async def main():
    stock_website_info = {
        "url": "https://stockanalysis.com/stocks/googl/",
        "schema": {
            "properties": {
                "market_cap": {"type": "string"},
                "open": {"type": "string"},
                "eps": {"type": "string"},
                "finantial perfomanc": {"type": "string"},
            },
        }
    }
    youtube_website_info = {
        "url": "https://www.youtube.com/@turingplanet4052/videos",
        "schema": {
            "properties": {
                "title": {"type": "string"},
                "view": {"type": "string"},
                "date": {"type": "string"},
            },
        }
    }
    twitter_website_info = {
        "url": "https://twitter.com/elonmusk/status/1777659389568045424",
        "schema": {
            "properties": {
                "post_author": {"type": "string"},
                "post_content": {"type": "string"},
            },
        }
    }
    techcruch_website_info = {
        "url": "https://techcrunch.com/2024/04/12/meta-is-testing-an-ai-powered-search-bar-in-instagram/",
        "schema": {
            "properties": {
                "article_title": {"type": "string"},
                "article_content": {"type": "string"},
            },
        }
    }

    parsing_target = stock_website_info
    parsing_target = youtube_website_info
    parsing_target = twitter_website_info
    # parsing_target = techcruch_website_info

    output = await run_playwright(parsing_target['url'])
    json_result = create_extraction_chain(parsing_target['schema'], llm).invoke(output)
    print(json_result['text'])


if __name__ == "__main__":
    asyncio.run(main())
