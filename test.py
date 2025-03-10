import aiohttp
import asyncio

async def fetch_latest_four_files():
    url = "https://featurebackend.onrender.com/fetchfile"
    headers = {"Content-Type": "application/json"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers) as response:
                if response.status != 200:
                    raise Exception("Failed to fetch files")
                data = await response.json()
                print("Latest Four Files:", data)
                return data
    except Exception as e:
        print("Error fetching latest four files:", e)
        return []

# Run the async function
asyncio.run(fetch_latest_four_files())
