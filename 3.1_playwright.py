from playwright.async_api import async_playwright
import asyncio

async def get_article_details(url):
    async with async_playwright() as p:
        # browser = await p.chromium.launch(headless=False)
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        # Wait until network is idle after going to the page
        # await page.goto(url, wait_until='networkidle') # It considers the network to be idle when there are no more than 0 network connections for at least 500 ms (by default).
        # load is fired when the page and its resources (images, scripts, stylesheets, etc.) have finished loading. 
        await page.goto(url, wait_until='load')
        title = await page.title()
        print(f"The page title is: {title}")
        title = await page.inner_text('h1')
        print(f"The article title is: {title}")
        await asyncio.sleep(5)
        await browser.close()

async def main():
    # url = 'https://twitter.com/OldRowSwig/status/1732112446943269347?s=20'
    url = 'https://techcrunch.com/2024/04/20/boston-dynamics-unveils-a-new-robot-controversy-over-mkbhd-and-layoffs-at-tesla/'
    await get_article_details(url)

if __name__ == "__main__":
    asyncio.run(main())
