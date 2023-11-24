from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp


list_num = []
response1 = requests.get('https://asyncio.ru/zadachi/2/problem_pages.txt').text
lst = (list(response1.split('\n')))


async def page(url: str, semaphore):
    global list_num
    async with semaphore:
        async with aiohttp.ClientSession() as session:            # Создание асинхронной сессии
            async with session.get(url, ssl=False) as response:    # Асинхронный запрос GET к URL
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                p_tags = soup.find('p', id='number').text
                list_num.append(int(p_tags))
                return p_tags


async def main():
    semaphore = asyncio.Semaphore(70)
    tasks = []                                    # Список для хранения задач
    global lst
    url2 = 'https://asyncio.ru/zadachi/2/'
    for i in lst:
        link = f'{url2}html/{i}.html'
        task = asyncio.create_task(page(link, semaphore))
        tasks.append(task)
    await asyncio.gather(*tasks)

asyncio.run(main())
print(sum(list_num))
