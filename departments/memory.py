from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# a function that uses openai to generate an embedding of a text document
import openai
import pinecone
from pinecone import PineconeException
import os
from openai.embeddings_utils import get_embedding, cosine_similarity

from dotenv import load_dotenv


load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]

pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment="us-east4-gcp")
index_name = "cwa-marketing-embeddings"


# Ensure you have set up your OpenAI API key as an environment variable
def generate_embedding(text: str):
    # Using 'strip' to remove newline characters
    text = text.strip()

    # Send the request to OpenAI
    response = openai.Embedding.create(model="text-embedding-ada-002", input=text)
    # embedding = get_embedding(text)

    # The 'choices' field in the response contains the model's output
    embedding: list[float] = response["data"][0]["embedding"]

    return embedding


# remember function takes in text and uses generate_embedding and sends that embedding to pinecone index
def remember(text: str, index_name: str = index_name) -> str:
    # Generate the embedding
    embedding = generate_embedding(text)

    # Upsert the embedding to Pinecone
    index = pinecone.Index(index_name)
    try:
        index.upsert(
            vectors=[
                {
                    "id": "test-data",
                    "values": embedding,
                    "metadata": {"tag": "test_data", "value": text},
                }
            ],
        )
        return "REMEMBERED"
    except Exception as e:
        print(f"Error: {e}")
        return "NOT_REMEMBERED"


def write_file(text: str, path: str):
    # Open the file for writing
    file = open(path, "w")

    # Write some data to the file
    file.write(text)

    # Close the file
    file.close()


#
def fetch_memory(text: str, index_name: str = index_name, top_k: int = 5) -> str:
    """Query the index and return the ids and scores of the nearest neighbors"""
    # Generate the query embedding
    query_embedding = generate_embedding(text)
    index = pinecone.Index(index_name)
    answer = ""
    # Query the Pinecone index
    try:
        result = index.query(index_name=index_name, vector=query_embedding, top_k=top_k)
        top_id: str = result["matches"][0]["id"]

        data = index.fetch([top_id])
        answer = data["vectors"][top_id]["metadata"]["value"]
    except PineconeException as e:
        print(e)
        return 'ERROR"Failed to communicate with vector db"'

    # The result contains the ids and scores of the nearest neighbors
    try:
        # top_score: float = result["matches"][0]["score"]
        # top_values: list[float] = result["matches"][0]["values"]
        # if top_score > 0.59:
        #     return top_value
        # return "NOT CERTAIN ENOUGH"
        return answer

    except IndexError:
        return "ERROR"

    return "ERROR"


memory_manager = AssistantAgent(
    name="Memory_Manager",
    system_message="Manage the retrieval of memories and records for Clesca LLC. Only use the functions you have been provided with.",
    llm_config={
        # "config_list": config_list
        "functions": [
            {
                "name": "generate_embedding",
                "description": "Ask memory_manager generate an embedding (in other words remember) a given document. It can be in many forms like csv, plain text, and even byte data.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "data to generate an embedding from. Make sure it is not over an 8000 davincii-3 token length.",
                        },
                    },
                    "required": ["text"],
                },
            },
            {
                "name": "remember",
                "description": "Remember some information given to you either by a user or by ",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The information (document) to remember. This will upload the information to a vector database and can be referenced again in teh future. It can be in many forms like csv, plain text, and even byte data.",
                        },
                    },
                    "required": ["text"],
                },
            },
            {
                "name": "fetch_memory",
                "description": "Fetch a memory. If it fails, this will return ERROR and may be followed with a failure reason. It's ",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Information to use to help fetch the memory. This is usually a question or key points about embedded documents.",
                        },
                    },
                    "required": ["text"],
                },
            },
        ]
    },
    function_map={
        "generate_embedding": generate_embedding,
        "remember": remember,
        "fetch_memory": fetch_memory,
    },
)

memory_user = UserProxyAgent(
    name="Memory_User",
    max_consecutive_auto_reply=0,  # terminate without auto-reply
    human_input_mode="NEVER",
)

remember("The owner of Clesca LLC (Philippe Clesca) Created Clesca LLC during his time working at Wander. He would receive requests from previous and new clients for development and management of many different things. Clesca LLC. Currently has several clients: Remvidz, Cogwheel Analytics.")
