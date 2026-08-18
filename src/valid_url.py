import httpx


async def is_valid(url: str):
    try:
        async with httpx.AsyncClient(timeout= 5) as client:
            response = await client.head(url=url, follow_redirects= False)
            return response.status_code < 400
    except httpx.ConnectError:
        return False
    except httpx.TimeoutException:
        return False