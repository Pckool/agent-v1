import tiktoken


# a function to read the data from a given path and exception checks meant to be interpreted by an llm
# Note that this function is not used in the final product, but is used in the data collection pipeline.
def read_data(path):
    try:
        with open(path, "r") as f:
            data = f.read()
        return data
    except Exception as e:
        print(e)
        return "Oops. I cannot read the file."


# a function to write the data to a given path and exception checks meant to be interpreted by an llm
# Note that this function is not used in the final product, but is used in the data collection pipeline.
def write_data(path, data):
    try:
        with open(path, "w") as f:
            f.write(data)
        return "I successfully wrote the data to the file."
    except Exception as e:
        print(e)
        return "Oops. I cannot write the data to the file."


# a function to execute the code from a given path and exception checks meant to be interpreted by an llm
# Note that this function is not used in the final product, but is used in the data collection pipeline.
def execute_code(path):
    try:
        with open(path, "r") as f:
            code = f.read()
        exec(code)
        return "I successfully executed the code."
    except Exception as e:
        print(e)
        return "Oops. I cannot execute the code."


# a function to inspect the execution result of the code from a given path and exception checks meant to be interpreted by an llm
# Note that this function is not used in the final product, but is used in the data collection pipeline.
def inspect_execution_result(path):
    try:
        with open(path, "r") as f:
            code = f.read()
        exec(code)
        return "I successfully inspected the execution result."
    except Exception as e:
        print(e)
        return "Oops. I cannot inspect the execution result."


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def write_file(text: str, path: str):
    # Open the file for writing
    file = open(path, "w")

    # Write some data to the file
    file.write(text)

    # Close the file
    file.close()
