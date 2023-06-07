import aiohttp
import asyncio


async def send_questions_num(num):
    url = f'http://127.0.0.1:8001/questions_num/'
    headers = {'Content_Type': 'application/json'}
    params = {"questions_num": num}
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=params, headers=headers) as response:
            response_json = await response.json()
            print(response_json)


if __name__ == "__main__":
    asyncio.run(send_questions_num(5))
