import asyncio
import time
import aiohttp

async def download_site(session:aiohttp.ClientSession, url:str):
  async with session.get(url) as response:
    print(f"Read {response.content_length} from {url}")

async def download_all_sites(sites:list[str]):
  async with aiohttp.ClientSession() as session:
    tasks = []
    for url in sites:
      task = asyncio.create_task(download_site(session, url))
      tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
  sites = [
    "https://homepage.sch.ac.kr",
    "https://example.org",
  ] * 80
  start_time = time.time()
  asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  asyncio.run(download_all_sites(sites))
  duration = time.time() - start_time
  print(f"Downloaded {len(sites)} in {duration} seconds")