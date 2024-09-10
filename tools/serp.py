import os
from langchain_community.tools import BraveSearch

def search(keywords: str) -> list:
    tool = BraveSearch.from_api_key(api_key=os.getenv('BRAVE_KEY'), search_kwargs={"count": 3})
    return tool.run(keywords)



def serpResult2md(results:list) -> str:
    markdown_output = ""
    for result in results:
        title = result.get("title")
        link = result.get("link")
        body = result.get("snippet")
        if title and link:
            markdown_output += f"- [{title}]({link})\n{body}\n\n"
    return markdown_output
