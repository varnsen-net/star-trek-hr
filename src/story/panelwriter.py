"""Helper class for generating story text using OpenAI API."""

import copy

from openai import OpenAI



class PanelWriter:
    """Generates story text using OpenAI API.
    
    :attr OpenAI client: OpenAI API client.
    """

    TOOLS_TEMPLATE = [
      {
        "type": "function",
        "function": {
          "name": "write_panel",
          "description": "Write the panel text and player options for a text adventure game.",
          "parameters": {
            "type": "object",
            "properties": {
              "body": {
                "type": "string",
                  "description": "The text to display in the panel. Length: 100-200 words.",
              },
            },
            "required": ["body"],
          },
        }
      }
    ]

    def __init__(self, model):
        """Initialize a new PanelWriter object."""
        self.client = OpenAI()
        self.model = model

    def build_tools_param(self, n):
        """Build the tools parameter for the GPT function-calling feature.
        
        :param int n: Number of player choices to generate.
        :param list[dict] tools: List of tools to modify.
        :return: Modified tools list.
        :rtype: list[dict]
        """
        tools = copy.deepcopy(self.TOOLS_TEMPLATE)
        for choice in range(n):
            property = {
                "type": "string",
                "description": f"The text to display for choice number {choice}.",
            }
            tools[0]["function"]["parameters"]["properties"][f"choice_{choice}"] = property
            tools[0]["function"]["parameters"]["required"].append(f"choice_{choice}")
        return tools

    def fetch_chatgpt_response(self, sys_content, usr_content, tools):
        """Fetch a response from the ChatGPT model.
        
        :param str sys_content: System message content.
        :param str usr_content: User message content.
        :param list[dict] tools: List of tools to modify.
        :return: Response from the ChatGPT model.
        :rtype: dict
        """
        messages = [{"role": "system", "content": sys_content},
                    {"role": "user", "content": usr_content}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice="required"
        )
        return response

    def fetch_and_jsonify(self, sys_content, usr_content, tools,
                          max_retries=10):
        """Fetch a response from the ChatGPT model and jsonify it.
        
        Function calling sometimes fails because chatgpt does not return a
        string that can be turned into a dictionary.
        """
        for _ in range(max_retries):
            try:
                response = self.fetch_chatgpt_response(sys_content, usr_content, tools)
                resp_str = response.choices[0].message.tool_calls[0].function.arguments
                resp_dict = eval(resp_str)
                return resp_dict
            except SyntaxError:
                continue
        raise ValueError("Failed to jsonify response after 10 retries.")


if __name__ == "__main__":
    import os

    import dotenv

    import src.config.config as config

    dotenv.load_dotenv()

    sys_content = config.SYS_CONTENT
    usr_content = """The overall story is that Data is trying to file an HR complaint against Riker for cheating during poker. The previous panel text was: 'Data walks into the HR office and asks to see the HR officer in charge.' The previous player choice was: 'Data hands the HR officer a 200 page report on Riker's cheating."""

    writer = PanelWriter(config.MODEL)
    tools = writer.build_tools_param(5)
    response = writer.fetch_chatgpt_response(sys_content, usr_content, tools)
    print(response.choices[0].finish_reason)
    print(response.choices[0].message.tool_calls[0].function.arguments)
