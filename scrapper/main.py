import asyncio
from pathlib import Path

from scrapper.consts import LIST_OF_SUBREDDITS_TO_SCRAP

from .utils import fetchPostsFromSubreddit, save_to_csv


async def subreddit_name_generator():
    for sr in LIST_OF_SUBREDDITS_TO_SCRAP:
        yield sr


async def main():
    # res = await fetchPostsFromSubreddit("delhi", 2000)
    # print(res)
    cwd = Path.cwd()
    data_dir = cwd / "data"

    async for subreddit in subreddit_name_generator():
        posts = await fetchPostsFromSubreddit(subreddit, 1000)
        loop = asyncio.get_running_loop()
        file_name = data_dir / f"{subreddit}.csv"
        await loop.run_in_executor(None, save_to_csv, file_name, posts)
        # save_to_csv(data_dir / f"{subreddit}.csv", posts)


if __name__ == "__main__":
    asyncio.run(main())
