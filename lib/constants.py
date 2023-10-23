prompts = {
  "writing_or_code": """For any action beyond writing code or reasoning, convert it to a step which can be implemented by writing code. For example, the action of browsing the web can be implemented by writing code which reads and prints the content of a web page. Finally, inspect the execution result. If the plan is not good, suggest a better plan. If the execution is wrong, analyze the error and suggest a fix.""",
  "action": """You suggest coding and reasoning steps for another AI assistant to accomplish a task. Do not suggest concrete code.""",
  "planner": """You are a helpful AI assistant. {action}""",
  "planner_user": """You are a user who is working with the Planner to accomplish a task. {action}""",
  "ask_planner": """You ask the Planner to {action}""",
  "ask_planner_code": """You ask the Planner to {action}. Here is the code you want the Planner to reason about:\n\n```python\n{code}\n```""",
}