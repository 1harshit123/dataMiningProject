import asyncio
from typing import Dict, List
import asyncpraw
from decouple import config

from rich import print

CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")
USER_AGENT = config("USER_AGENT")


async def _fetchPostsFromSubreddit(
    reddit: asyncpraw.Reddit, subredditName: str, numberOfPosts: int
):
    subredditClass = await reddit.subreddit(subredditName, fetch=True)

    posts: List[Dict[str, str]] = []
    async for post in subredditClass.hot(limit=numberOfPosts):
        posts.append(post.__dict__)
    print(posts)


async def fetchPostsFromSubreddit(subredditName: str, numberOfPosts: int):
    async with asyncpraw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
    ) as reddit:
        await _fetchPostsFromSubreddit(reddit, subredditName, numberOfPosts)


async def main():
    async with asyncpraw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
    ) as reddit:
        await _fetchPostsFromSubreddit(reddit, "delhi", 10)


if __name__ == "__main__":
    asyncio.run(main())
