import os
import dotenv

import openai

import helpers.constants

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def fetch_gpt_modified_json(panel_json,
                            prompt=helpers.constants.PROMPT,
                            query=helpers.constants.QUERY):
    """Fetch a modified json object from GPT.

    :param dict panel_json: a json object representing a panel
    :param str prompt: the system prompt for the GPT query
    :param str query: the GPT query
    :return: a modified json object
    :rtype: dict
    """
    query = query.format(JSON=panel_json)
    response = openai.ChatCompletion.create(
        model = "gpt-4",
        messages = [{"role": "system", "content": prompt},
                    {"role": "user", "content": query},],
        # max_tokens=50, # lmao
    )
    response = response['choices'][0]['message']['content']
    return response


