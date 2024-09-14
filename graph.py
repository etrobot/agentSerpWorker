import time
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START,END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage

from agents import planner,decision_maker
from tools import serp
import dotenv
dotenv.load_dotenv()

def getAgent():
    class State(TypedDict):
        messages: Annotated[list, add_messages]
        plan: list
        next_plan:str
        past_steps: list

    graph_builder = StateGraph(State)

    def planNode(state: State):
        object = state['messages'][0].content
        planlist = planner.plan(object)[:5]
        return {"messages": state['messages'],"plan": planlist,"next_plan":planlist[0],"past_steps":[]}

    def toolNode(state: State):
        serp_response=[]
        if state['next_plan'] in state['plan']:
            idx = state['plan'].index(state['next_plan'])
            for i in range(idx, len(state['plan'])):
                serp_response.extend(serp.search(keywords=state['plan'][i]))
                time.sleep(2)
        else:
            state['plan'].append(state['next_plan'])
            serp_response.extend(serp.search(keywords=state['next_plan']))
        past_steps = list({item['title']: item for item in state['past_steps'] + serp_response}.values())
        return {"past_steps":past_steps}

    def decisionNode(state: State):
        answer,nextPlan = decision_maker.thinkNanswer(
            input=state['messages'][-1].content,
            plan=str(state['plan']),
            past_steps=serp.serpResult2md(state['past_steps']))
        if nextPlan is None:
            if len(state['past_steps']) > 0:
                serpExist = serp.handle_search_results(state['past_steps'])
                if len(serpExist) >= 3:
                    return {"messages": state['messages'] + [AIMessage('No new result')],"next_plan":None}
            state['messages'].append(AIMessage(answer))
        return {"next_plan":nextPlan}


    def should_loop(state: State):
        if state['next_plan'] is not None:
            return 'serpTool'
        else:
            return END

    graph_builder.add_node("planNode", planNode)
    graph_builder.add_node("serpTool", toolNode)
    graph_builder.add_node("decisionNode", decisionNode)

    graph_builder.add_edge(START, "planNode")
    graph_builder.add_edge("planNode", "serpTool")
    graph_builder.add_edge("serpTool", "decisionNode")
    graph_builder.add_conditional_edges("decisionNode", should_loop)

    app = graph_builder.compile()
    return app

if __name__ == "__main__":
    object = "Nomardlist.com introdcution, bussiness mode, tech stack and grow story"
    getAgent().invoke({"messages":[{'role':'user','content':object}]}, {"recursion_limit": 10},debug=True)
    # print(getAgent().get_graph().draw_mermaid())