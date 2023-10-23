from autogen import (
    AssistantAgent,
    UserProxyAgent,
    config_list_from_json,
    config_list_openai_aoai,
    GroupChat,
    GroupChatManager,
)

from departments.memory import (
    generate_embedding,
    remember,
    fetch_memory,
    memory_manager,
    memory_user,
)
from departments.product import ask_planner, planner
from departments.data import data_engineer

from dotenv import load_dotenv

load_dotenv()

# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
# and OAI_CONFIG_LIST_sample
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")
# You can also set config_list directly as a list, for example, config_list = [{'model': 'gpt-4', 'api_key': '<your OpenAI API key here>'},]
assistant = AssistantAgent(
    "Assistant",
    # system_message="You are the assistant of the system admin of Clesca LLC. You conduct work for the admin. You should check with other "
    llm_config={
        "model": "gpt-4",
        "config_list": config_list_openai_aoai(exclude="aoai"),
        "functions": [
            {
                "name": "ask_planner",
                "description": "ask planner to: 1. get a plan for finishing a task, 2. verify the execution result of the plan and potentially suggest new plan.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Question to ask planner. Make sure the question include enough context, such as the code and the execution result. The planner does not know the conversation between you and the user, unless you share the conversation with the planner.",
                        },
                    },
                    "required": ["message"],
                },
            },
        ],
    },
)
user_proxy = UserProxyAgent(
    "Admin",
    system_message="You are the system admin of Clesca LLC. You conduct work for the owner of the company. If you receive any questions about Clesca LLC or any known clients or associates (you should check with Memory_Manager).",
    code_execution_config={"work_dir": "working"},
    # human_input_mode="NEVER",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    # is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    is_termination_msg=lambda x: "content" in x
    and x["content"] is not None
    and x["content"].rstrip().endswith("TERMINATE"),
    function_map={
        "ask_planner": ask_planner,
    },
)

groupchat = GroupChat(
    agents=[
        user_proxy,
        data_engineer,
        planner,
        memory_manager,
        memory_user,
        # critic,
    ],
    messages=[],
    max_round=50,
)
manager = GroupChatManager(groupchat=groupchat, llm_config=config_list)

# This initiates an automated chat between the two agents to solve the task
user_proxy.initiate_chat(
    manager,
    message="""What's the name of the owner of Clesca LLC?""",
)
