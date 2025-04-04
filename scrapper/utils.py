import asyncio
import csv
from pathlib import Path
from typing import Any, Dict, List

import asyncpraw

from .consts import CLIENT_ID, CLIENT_SECRET, USER_AGENT


async def _fetchPostsFromSubreddit(
    reddit: asyncpraw.Reddit, subredditName: str, numberOfPosts: int
) -> List[Dict[str, Any]]:
    # fetch=False so that it avoids fetch unecessary utill specifically requested
    subredditClass = await reddit.subreddit(subredditName, fetch=True)

    posts: List[Dict[str, str]] = []

    post_gen = subredditClass.hot(limit=numberOfPosts)

    tasks = [
        encode_post_detail(post, posts)
        async for post in post_gen
        if getattr(post, "selftext") not in ("[removed]", "[deleted]")
    ]

    asyncio.gather(*tasks)

    # async for post in post_gen:
    #     postInst = {}
    #
    #     # extract only necessary info
    #
    #     postInst["author_username"] = post.author_fullname
    #     postInst["title"] = post.title
    #     postInst["downs"] = post.downs
    #     postInst["ups"] = post.ups
    #     postInst["upvote_ratio"] = post.upvote_ratio
    #     postInst["total_awards_recieved"] = post.total_awards_received
    #     postInst["created_utc"] = post.created_utc
    #     postInst["over_18"] = post.over_18
    #     postInst["subreddit_id"] = post.subreddit_id
    #     postInst["selftext"] = post.selftext
    #
    #     posts.append(postInst)
    return posts


async def encode_post_detail(post, posts):
    postInst = {}

    # extract only necessary info

    postInst["author_username"] = (
        post.author.name if getattr(post, "author", None) is not None else None
    )
    postInst["title"] = post.title if getattr(post, "title", None) is not None else None
    postInst["downs"] = post.downs if getattr(post, "downs", None) is not None else None
    postInst["ups"] = post.ups if getattr(post, "ups", None) is not None else None
    postInst["upvote_ratio"] = (
        post.upvote_ratio if getattr(post, "upvote_ratio", None) is not None else None
    )
    postInst["total_awards_recieved"] = (
        post.total_awards_received
        if getattr(post, "total_awards_received", None) is not None
        else None
    )
    postInst["created_utc"] = (
        post.created_utc if getattr(post, "created_utc", None) is not None else None
    )
    postInst["over_18"] = (
        post.over_18 if getattr(post, "over_18", None) is not None else None
    )
    postInst["subreddit_id"] = (
        post.subreddit_id if getattr(post, "subreddit_id", None) is not None else None
    )
    postInst["selftext"] = (
        post.selftext if getattr(post, "selftext", None) is not None else None
    )

    posts.append(postInst)


async def fetchPostsFromSubreddit(subredditName: str, numberOfPosts: int):
    async with asyncpraw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
    ) as reddit:
        res = await _fetchPostsFromSubreddit(reddit, subredditName, numberOfPosts)
        # if output_lenght := len(res) != numberOfPosts:
        #     await asyncio.sleep(70)
        return res


# async def get_top_subreddit_by_country_and_posts(
#     reddit: asyncpraw.Reddit, country: str, limit=10, post_limit=1000
# ):
#     subreddit_post_count: Dict[str, int] = {}
#
#     async for subreddit in reddit.subreddits.search(country, limit=1000):
#         subreddit_name = subreddit.display_name
#         post_count = 0
#
#         async for _ in subreddit.hot(limit=post_limit):
#             post_count += 1
#             await asyncio.sleep(0.2)
#
#         subreddit_post_count[subreddit_name] = post_count
#
#     sorted_subreddits = sorted(
#         subreddit_post_count.items(), key=lambda x: x[1], reverse=True
#     )
#
#     return sorted_subreddits[:limit]


def save_to_csv(file_name: Path, posts: List[Dict[str, Any]]):
    filed_names = [
        "author_username",
        "title",
        "downs",
        "ups",
        "upvote_ratio",
        "total_awards_recieved",
        "created_utc",
        "over_18",
        "subreddit_id",
        "selftext",
    ]

    with file_name.open("+w") as file:
        writter = csv.DictWriter(file, fieldnames=filed_names)
        writter.writeheader()
        writter.writerows(rowdicts=posts)
