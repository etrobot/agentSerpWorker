from langchain_community.utilities import BingSearchAPIWrapper
import libsql_experimental as libsql
import re

def clean_title(text):
    # 去除 HTML 标签
    text = re.sub('<.*?>', '', text)
    # 去除特殊符号，只保留字母、数字和空格
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # 去除多余的空格，将多个空格替换为单个空格
    text = re.sub(r'\s+', ' ', text)
    # 去除首尾空格
    text = text.strip()
    return text
def search(keywords: str) -> list:
    result = [
        {
            "title": clean_title(x.get("title")).strip(),
            "snippet": x.get("snippet"),
            "link": x.get("link")
        } for x in BingSearchAPIWrapper().results(keywords, 3)
    ]
    return result

def serpResult2md(results:list) -> str:
    markdown_output = ""
    for result in results:
        title = result.get("title")
        link = result.get("link")
        body = re.sub('<.*?>', '', result.get("snippet"))
        if title and link:
            markdown_output += f"[{title}]({link})\n{body}\n\n"
    return markdown_output


# 连接数据库并进行操作的函数
def handle_search_results(new_data):
    conn = libsql.connect("serpResult.db")
    cursor = conn.cursor()

    # 创建表格 search_results，如果表格不存在
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            snippet TEXT NOT NULL,
            link TEXT NOT NULL
        )
    ''')

    # 准备查询语句，用于检查数据是否已经存在
    query_check = "SELECT title, snippet, link FROM search_results WHERE title = ?"

    # 用来存储新数据中已经在数据库中的条目
    existing_entries = []
    # 用来存储新且不重复的数据，供后续插入
    non_duplicate_data = []

    # 遍历每条新的搜索结果，检查是否已经存在于数据库中
    for entry in new_data:
        cursor.execute(query_check, (entry['title'],))
        result = cursor.fetchone()

        if result:  # 如果结果不为空，表示该条目已存在
            existing_entries.append(result)
        else:
            # 如果不存在，保存到 non_duplicate_data 列表中，准备插入
            non_duplicate_data.append((entry['title'], entry['snippet'], entry['link']))

    # 如果有新的非重复数据，则插入到数据库中
    if non_duplicate_data:
        cursor.executemany('''
            INSERT INTO search_results (title, snippet, link) 
            VALUES (?, ?, ?)
        ''', non_duplicate_data)

        conn.commit()  # 提交更改

    # 关闭数据库连接
    cursor.close()

    # 返回数据库中已存在的条目，如果没有则返回空列表
    return existing_entries