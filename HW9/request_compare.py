from aio_requests import download_all_sites as das_aio
from multi_process_requests import download_all_sites as das_mp
from multi_thread_requests import download_all_sites as das_mt
from simple_requests import download_all_sites as das_sr

import time
import asyncio

if __name__ == "__main__":
  sites = [
    "https://www.blank.org",
    # "https://homepage.sch.ac.kr",
    "https://example.org",
  ] * 80
  # 1. aio
  start_time = time.time()
  asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  asyncio.run(das_aio(sites))
  aio_duration = time.time() - start_time
  # 2. multiprocessing
  start_time = time.time()
  das_mp(sites)
  mp_duration = time.time() - start_time
  # 3. multithreading
  start_time = time.time()
  das_mt(sites)
  mt_duration = time.time() - start_time
  # 4. simple
  start_time = time.time()
  das_sr(sites)
  sr_duration = time.time() - start_time

  # Print
  print("=" * 20)
  print(f"* Total time of request {len(sites)} sites")
  print(f"asyncio: {aio_duration}sec")
  print(f"multiprocessing: {mp_duration}sec")
  print(f"multithreading: {mt_duration}sec")
  print(f"simple: {sr_duration}sec")
  print("=" * 20)