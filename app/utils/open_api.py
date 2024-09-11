# utils/openai_api.py
import openai
from openai import AzureOpenAI
import json
from config import AZURE_ENDPOINT, API_KEY, API_VERSION, DEPLOYMENT
from .functions import add, subtract, multiply, divide, is_even_or_odd

client = AzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=API_KEY,
    api_version=API_VERSION
)

tools = [
    {
         "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers together , if not any number given ask for number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
        "name": "subtract",
        "description": "Subtract the second number from the first.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"]
            }
        },

    },
    {
        "type": "function",
        "function": {
        "name": "multiply",
        "description": "Multiply two numbers together.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"]
          },

       },
    },
    {
        "type": "function",
        "function": {
        "name": "divide",
        "description": "Divide the first number by the second.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"]
           },

       },
    },
    {
        "type": "function",
        "function":{
            "name": "is_even_or_odd",
    "description": "Determines if a number is even or odd.",
    "parameters": {
        "type": "object",
        "properties": {
            "number": {
                "type": "integer",
                "description": "To Check wheather the given Number is Odd or Even "
            }
        },
        "required": ["number"]
    }

        }
    }
]


def call_openai_function_calling(messages, tools):
    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0
    )
    return response

def execute_function(function_name, function_args):
    if function_name == "add":
        return add(**function_args)
    elif function_name == "subtract":
        return subtract(**function_args)
    elif function_name == "multiply":
        return multiply(**function_args)
    elif function_name == "divide":
        return divide(**function_args)
    elif function_name == "is_even_or_odd":
        return is_even_or_odd(**function_args)
    else:
        return "Function not recognized."

def get_chat_response(prompt, messages):
    messages.append({"role": "user", "content": prompt})

    response = call_openai_function_calling(messages, tools)
    print("API Response:", response) 
    response_message = response.choices[0].message
    messages.append(response_message)
    print("Response Message:", response_message)

    function_call = response_message.tool_calls
    print("Function Call:", function_call) 

    if function_call:
        function_name = function_call[0].function.name
        function_args = json.loads(function_call[0].function.arguments)
        function_result = execute_function(function_name, function_args)
        messages.append({
            "tool_call_id": function_call[0].id,
            "role": "tool",
            "name": function_name,
            "content": json.dumps(function_result),
        })
    else:
        return response.choices[0].message.content

    final_response = call_openai_function_calling(messages, tools)
    return final_response.choices[0].message.content
