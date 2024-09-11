import re,os,ast
from langchain_openai import ChatOpenAI

#prompt
plannerPrompt:str = """
For the given object, Take a deep breath and think step by step, what's the related concept is needed to finish the search? make a group of keywords for the search engine. \
for example, the object is "write a wiki for google.com",and the keywors group should be in array format: \
["search engine","search engine bussiness mode","alphabet investment value","google.com tech stack","google.com founder"]

Here's the object: 

{object}

Finish it well and I will tip you $100.

"""

#output parser
def planParsed2list(output:str)->list:
    keywords_match = re.search(r'\[(.*?)\]', output.replace('\n',''))
    if keywords_match:
        keywords_str = keywords_match.group(0)  # 获取完整的方括号内容
        keywords_list = ast.literal_eval(keywords_str)
        return keywords_list
    return []

#llm
def plan(input:str) -> list:
    llm = ChatOpenAI(model=os.getenv("MODEL"), api_key=os.getenv("LLM_KEY"), base_url=os.getenv("LLM_BASE"))
    prompt = plannerPrompt.format(object=input)
    result = llm.invoke(prompt).content
    print(result)
    return planParsed2list(result)
