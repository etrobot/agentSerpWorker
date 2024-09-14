import os
from langchain_openai import ChatOpenAI

searchOrAnswer:str ="""\
For the given objective, search the keywords group by group and then make the final answer.  

Your objective was this:
{input}

You have currently finish the search with "{plan}", the search results are here:
{past_steps}

If the search results are enough to answer the objective or the search results ends with duplicate contents, please summarize the data and make a final answer beginned with a # title, finally end with {finishWord}. \
Otherwise, output the next keyword group in the last line with this format:
{shouldLoopWord} next keywords group here" \
"""

finishWord = "Misson Complete!"
shouldLoopWord = "Further Search:"

def thinkNanswer(input:str,plan:str,past_steps:str) -> (str,str):
    llm = ChatOpenAI(model=os.getenv("MODEL"), api_key=os.getenv("LLM_KEY"), base_url=os.getenv("LLM_BASE"))
    prompt = searchOrAnswer.format(input=input,plan=plan,past_steps=past_steps,finishWord=finishWord,shouldLoopWord=shouldLoopWord)
    print('prompt',prompt)
    result = llm.invoke([{'role':'user','content':prompt}]).content
    nextPlan = None
    resultDealed =result.split(shouldLoopWord)
    answer = resultDealed[0]
    if len(resultDealed)>1 and finishWord not in result:
        nextPlan = resultDealed[1].strip()
    return answer,nextPlan


