from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

data_engineer = AssistantAgent(
    name="Data_Engineer",
    llm_config={"config_list": config_list},
    # the default system message of the AssistantAgent is overwritten here
    system_message="You are a helpful Data Engineer for Clesca LLC. You interact with an sql database",
)
# planner_user = UserProxyAgent(
#     name="planner_user",
#     max_consecutive_auto_reply=0,  # terminate without auto-reply
#     human_input_mode="NEVER",
# )


# def ask_planner(message):
#     planner_user.initiate_chat(planner, message=message)
#     # return the last message received from the planner
#     return planner_user.last_message()["content"]
