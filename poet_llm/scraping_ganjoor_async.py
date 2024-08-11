import aiohttp
import asyncio
from bs4 import BeautifulSoup as bfs

url = 'https://ganjoor.net/moulavi/shams/ghazalsh'
CONCURRENT_REQUESTS = 150  # Number of parallel requests

async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_poem(session, url, page_number, visited_links, semaphore):
    link = f"{url}/sh{page_number+1}"

    # Check if the link has already been visited
    if link in visited_links:
        return

    # Mark this link as visited
    visited_links.add(link)

    async with semaphore:  # Ensure limited concurrent access
        print(f"Fetching: {link}")
        page_content = await fetch_page(session, link)
        content = bfs(page_content, 'html.parser')

        count = len(content.find_all('div', class_='b'))
        for i in range(count):
            id = 'bn'+str(i+1)
            a = content.find_all('div', class_='b', attrs={'id': id})
            if len(a) != 0:
                mesra_aval = a[0].find('div', class_='m1').text
                mesra_dovom = a[0].find('div', class_='m2').text
                with open('hafez.txt', 'a', encoding='utf-8') as file:
                    file.write('|'+mesra_aval+'         '+mesra_dovom)
                    file.write('\n')

async def main():
    visited_links = set()  # A set to keep track of visited links
    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)  # Limit concurrent requests

    async with aiohttp.ClientSession() as session:
        initial_page_content = await fetch_page(session, url)
        initial_content = bfs(initial_page_content, 'html.parser')
        page_counts = len(initial_content.find_all('p', class_='poem-excerpt'))

        tasks = []
        for page_number in range(page_counts):
            task = asyncio.create_task(fetch_poem(session, url, page_number, visited_links, semaphore))
            tasks.append(task)

        await asyncio.gather(*tasks)

# Run the main function
asyncio.run(main())
