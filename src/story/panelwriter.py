"""Helper class for generating story text using OpenAI API."""

import os
import time
from typing import Annotated

from google import genai
from google.genai import types
from pydantic import BaseModel, create_model, Field


def build_response_schema(n):
    """Build a response schema for the LLM response.

    :param int n: The number of options to generate.
    :return: A Pydantic model representing the response schema.
    :rtype: pydantic.BaseModel
    """
    model_params = {
        "body": Annotated[str, Field(
            description="The text to display in the panel. Max length: 400 words.",
            max_length=400,
        )],
    }
    for i in range(n):
        model_params[f"option_{i}"] = Annotated[str, Field(
            description=f"Option {i+1} for the player to choose. Max length: up to 100 words.",
            max_length=100,
        )]
    return create_model("Panel", **model_params)


def fetch_llm_response(sys_content, usr_content, response_schema):
    """Fetch a response from the LLM.

    :param str sys_content: The system content to provide to the LLM.
    :param str usr_content: The user content to provide to the LLM.
    :param pydantic.BaseModel response_schema: The response schema to use for
        the LLM response.
    :return: The LLM response.
    :rtype: google.genai.types.GenerateContentResponse
    """
    client = genai.Client(api_key=os.getenv("LLM_KEY"))
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=usr_content,
        config=types.GenerateContentConfig(
            system_instruction=sys_content,
            response_mime_type='application/json',
            response_schema=list[response_schema]),
    )
    time.sleep(2) # Avoid rate limit on free plan
    return response

def fetch_and_jsonify(sys_content, usr_content, response_schema,
                      max_retries=10):
    """Fetch a response from the LLM and convert it to a JSON object.

    :param str sys_content: The system content to provide to the LLM.
    :param str usr_content: The user content to provide to the LLM.
    :param pydantic.BaseModel response_schema: The response schema to use for
        the LLM response.
    :param int max_retries: The maximum number of retries to attempt if the
        response cannot be converted to JSON.
    :return: The LLM response as a JSON object.
    :rtype: dict
    """
    for _ in range(max_retries):
        try:
            response = fetch_llm_response(sys_content, usr_content,
                                          response_schema)
            resp_dict = eval(response.text)
            return resp_dict
        except SyntaxError:
            continue
    raise ValueError("Failed to jsonify response after 10 retries.")


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv('./.env')

    sys_content = """You are a story generating bot for a text adventure game based on star trek the next generation.

    You are tasked with writing the panel text and player options for the game. You will be given information about the overall plot, as well as the previous panel texts and player choices. Use this information to create the next panel.
    """
    usr_content = """The overall story is that Data is trying to file an HR complaint against Riker for cheating during poker. The previous panel text was: 'Data walks into the HR office and asks to see the HR officer in charge.' The previous player choice was: 'Data hands the HR officer a 200 page report on Riker's cheating."""

    response_schema = build_response_schema(3)
    response = fetch_and_jsonify(sys_content, usr_content, response_schema)
    print(response[0])
