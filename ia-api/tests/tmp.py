import asyncio
import httpx
import time

# url = "http://20.63.107.215:8000/api/v1/analyze/predict"
url = "http://localhost:8000/api/v1/analyze/predict"
image_path = "assets/sample.jpg"

async def send_request(i):
    async with httpx.AsyncClient() as client:
        with open(image_path, "rb") as f:
            files = {"file": (image_path, f, "image/jpeg")}
            response = await client.post(url, files=files, timeout=600.0)
            print(f"[{i}] Response: {response.json()}", flush=True)

async def main():
    t0 = time.time()
    tasks = [send_request(i) for i in range(500)]
    await asyncio.gather(*tasks)
    print(f"Total time: {time.time() - t0:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())