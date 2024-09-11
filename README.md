# agentSerpWorker
A Plan-and-excute(search) agent build with Langgraph and FastHTML.

- <strong>No function-call feature required.</strong>
- Use any LLM api that follows the OpenAI format.
- Raad missions from notion by Status "Mission" and write the result back to notion

```mermaid
graph TD;
	__start__([__start__]):::first
	planNode(planNode)
	serpTool(serpTool)
	decisionNode(decisionNode)
	__end__([__end__]):::last
	__start__ --> planNode;
	planNode --> serpTool;
	serpTool --> decisionNode;
	decisionNode -.-> planNode;
	decisionNode -.-> serpTool;
	decisionNode -.-> __end__;	
```
## Usage

1. Copy .env_example to .env and fill out the necessary information.
2. Run ```poetry install```
3. Run ```poetry run python app.py```
