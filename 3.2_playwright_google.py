import asyncio
from playwright.async_api import async_playwright

async def search_google(query):
    async with async_playwright() as p:
        # Launch the browser in headless mode (change headless=False if you want to see it)
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        # Go to Google's homepage
        await page.goto("https://www.google.com", wait_until='networkidle')
        # Wait for the search input to load, type the search query, and press Enter
        await page.fill("textarea[name='q']", query)
        await page.press("textarea[name='q']", "Enter")
        # Wait for the results to load
        await page.wait_for_selector("#search")
        # Fetch all titles and URLs of the search results
        titles = await page.evaluate('''() => {
            const titles = [];
            const items = document.querySelectorAll('h3');
            items.forEach(item => titles.push(item.innerText));
            return titles;
        }''')
        urls = await page.evaluate('''() => {
            const urls = [];
            const links = document.querySelectorAll('.tF2Cxc .yuRUbf a');
            links.forEach(link => urls.push(link.href));
            return urls;
        }''')
        await browser.close()
        return list(zip(titles, urls))

async def main():
    query = "TuringPlanet"
    results = await search_google(query)
    
    print(f"Search results for '{query}':")
    for title, url in results:
        print(f"Title: {title}\nURL: {url}\n")

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from playwright.async_api import async_playwright
