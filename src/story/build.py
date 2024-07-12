"""Builds a full story ready to be consumed by the Flask app."""

import json
import random
import copy

import dotenv

from src.config.config import (SYS_CONTENT,
                               USR_CONTENT,
                               MODEL,
                               NUM_OF_NODES,
                               STORIES_DIR,
                               OVERALL_PLOT_TEXT,
                               TITLE)
from src.story.graphwriter import StoryGraph
from src.story.panelwriter import PanelWriter


def build_current_story_text(storyboard, path_to_node):
    """Builds the story text leading up to the current node.

    :param list[dict] storyboard: The full storyboard.
    :param list[int] path_to_node: The path from the root node to the current
        node.
    :return: The story text leading up to the current node.
    :rtype: str
    """
    current_story_text = ""
    for i in path_to_node[:-1]:
        current_story_text += storyboard[i]["paragraph_text"] + "\n\n"
    return current_story_text


def build_usr_content_params(node, panel, storyboard, path_to_node):
    """Builds the parameters for the USR_CONTENT template.

    The usr_content we send to openai changes depending on the location of the
    current node in the story.
    
    :param int node: The current node.
    :param dict panel: The storyboard panel to build the content for.
    :param list[dict] storyboard: The full storyboard.
    :param list[int] path_to_node: The path from the root node to the current
        node.
    :return: The story text leading up to the current node, and the
        instructions for writing the next panel.
    :rtype: tuple[str, str]
    """
    if len(path_to_node) == 1:
        current_story_text = "There is no story yet because this is the introductory panel."
        instructions = "Please introduce the story with this panel."
    else:
        current_story_text = build_current_story_text(storyboard, path_to_node)
        parent_node = path_to_node[-2]
        previous_decision = storyboard[parent_node]["dialogue_options"][node]
        current_story_text += f"Player decision: {previous_decision}"
        instructions = "Please continue the story with this panel. "
        if panel["is_leaf"] == True:
            instructions += "This is the final panel. There are no more player choices, and the story must end with the total destruction of the Enterprise, caused by the player character's previous action."
    return current_story_text, instructions

if __name__ == "__main__":
    dotenv.load_dotenv()

    # let users regenerate the story graph
    graph = StoryGraph(NUM_OF_NODES)
    graph.print_graph()
    while True:
        regenerate = input("Regenerate the story graph? (y/n): ")
        if regenerate.lower() == "y":
            graph = StoryGraph(30)
            graph.print_graph()
        else:
            break
    storyboard = graph.generate_storyboard_json()
    writer = PanelWriter(MODEL)

    for node, panel in storyboard.items():
        print(f"Node: {node}")
        n = len(panel["dialogue_options"])
        path_to_node = panel["path_to_node"]
        current_story_text, instructions = build_usr_content_params(
            node,
            panel,
            storyboard,
            path_to_node)
        usr_content = USR_CONTENT.format(overall_plot_text=OVERALL_PLOT_TEXT,
                                         current_story_text=current_story_text,
                                         instructions=instructions)
        tools = writer.build_tools_param(n)
        response_args = writer.fetch_and_jsonify(SYS_CONTENT, usr_content, tools)
        # finish_reason = response.choices[0].finish_reason
        body = response_args["body"]
        player_options = copy.deepcopy(response_args)
        del player_options["body"]
        storyboard[node]["paragraph_text"] = body
        keys = storyboard[node]["dialogue_options"].keys()
        vals = player_options.values()
        storyboard[node]["dialogue_options"] = dict(zip(keys, vals))

    with open(STORIES_DIR / f"{TITLE}.json", "w") as f:
        json.dump(storyboard, f, indent=4)
