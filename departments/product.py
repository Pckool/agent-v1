from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
import lib.constants as constants

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

planner = AssistantAgent(
    name="Planner",
    llm_config={"config_list": config_list},
    # the default system message of the AssistantAgent is overwritten here
    system_message="""You are a product manager for Clesca LLC. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
    The plan may involve an engineer who can write code and a scientist who doesn't write code.
    Explain the plan first. Be clear which step is performed by an data engineer, a memory manager.""",
)
planner_user = UserProxyAgent(
    name="planner_user",
    max_consecutive_auto_reply=0,  # terminate without auto-reply
    human_input_mode="NEVER",
)


def ask_planner(message):
    planner_user.initiate_chat(planner, message=message)
    # return the last message received from the planner
    return planner_user.last_message()["content"]
