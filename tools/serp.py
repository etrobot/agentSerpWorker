import os
from langchain_community.utilities import BingSearchAPIWrapper

def search(keywords: str) -> list:
    result =  BingSearchAPIWrapper().results(keywords, 3)
    return result

def serpResult2md(results:list) -> str:
    markdown_output = ""
    for result in results:
        title = result.get("title")
        link = result.get("link")
        body = result.get("snippet")
        if title and link:
            markdown_output += f"[{title}]({link})\n{body}\n\n"
    return markdown_output