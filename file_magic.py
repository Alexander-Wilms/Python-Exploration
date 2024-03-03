import asyncio

import aiohttp

import magic


async def main():
    url = "https://ftp.gnu.org/gnu/gzip/gzip-1.12.tar.gz"
    HTTP_CHUNK_SIZE = 1024 * 64
    size = 0
    first_chunk = True
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(response.status)
            async for chunk in response.content.iter_chunked(HTTP_CHUNK_SIZE):
                if first_chunk:
                    mimetype = magic.from_buffer(chunk, mime=True)
                    print(mimetype)
                    first_chunk = False
                    break
                size += len(chunk)


asyncio.run(main())
