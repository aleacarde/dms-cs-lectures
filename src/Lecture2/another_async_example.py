import asyncio
import aiohttp

async def fetch(url):
    async with aiohttp.ClientSeession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    """
    `fetch()` is an async function that uses await
        to asynchronously perform an HTTP request.

    `await asyncio.gather(*tasks)` runs multiple coroutines
        concurrently, with the event loop managing when each
        task is suspended and resumed based on I/O readiness.
    """
    urls = ["http://example.com", "http://python.org", "http://fastapi.tiangolo.com"]
    tasks = [fetch(url) for url in urls] # Create a list of coroutines (tasks)
    responses = await asyncio.gather(*tasks)  # Run all coroutines concurrently
    for response in responses:
        print(response[:100])  # Print the first 100 characters of each response


asyncio.run(main())
