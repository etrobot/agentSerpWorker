import requests,logging,json,os,time as t
from langchain_openai import ChatOpenAI
from tools.noiton  import NotionMarkdownManager
from dotenv import load_dotenv, find_dotenv
from tools import browser
from graph import getAgent
load_dotenv(find_dotenv())
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s')

manager = NotionMarkdownManager(os.getenv("NOTION_TOKEN"), os.getenv("NOTION_DB_ID_SW"))
llm = ChatOpenAI(model=os.getenv("MODEL"), api_key=os.getenv("LLM_KEY"), base_url=os.getenv("LLM_BASE"))

# while True:
#     try:
mission_articles = manager.list_mission_articles()
if len(mission_articles) == 0:
    logging.info("No mission articles found")
    t.sleep(60)
    # continue
for article in mission_articles:
    mission =  {"name": article["properties"]["Name"]["title"][0]["text"]["content"], "value": article["id"]}
    articleContent = manager.get_article_content(article["id"])
    links = browser.extract_and_replace_links(articleContent)
    prompt = ''
    if len(links)>0:
        linkread = browser.linkReader(links[0])
        prompt= linkread+'accroding the data above,summarize keypoints about: '+mission["name"]
        prompt = llm.invoke([{'role':'user','content':prompt}]).content
    past_steps = [{'title':articleContent,'link':links[0],'snippet':prompt}]
    msg=[{'role':'user','content':articleContent}]
    print(msg,past_steps)
    lgraph = getAgent().invoke({"messages": msg, "past_steps": past_steps},{"recursion_limit": 10},debug=True)
    print(lgraph['messages'][-1]['content'])
            # if len(answer)>300:
            #     newId = manager.update_markdown_to_notion(article["id"],answer,title=mission["name"])
            #     logging.critical(f"Inserted:{newId}{mission['name']} ")
            # break
    # except Exception as e:
    #     logging.error(f"Error: {e}")
    #     t.sleep(3600)
