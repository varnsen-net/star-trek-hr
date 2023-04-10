import json
import random

import helpers.graph
import helpers.generation


def populate_previous_panel_info(node, storyboard):
    """Populate the previous paragraph and dialogue options for a node.

    :param int node: the node to populate
    :param dict storyboard: the storyboard json object
    :return: storyboard json object
    :rtype: dict
    """
    if storyboard[node]['parent'] is not None:
        storyboard[node]['previous_paragraph'] = storyboard[storyboard[node]['parent']]['paragraph_text']
        storyboard[node]['previous_dialogue_option'] = storyboard[storyboard[node]['parent']]['dialogue_options'][node]
    return storyboard


def update_storyboard(storyboard, node, gpt_response, hand_crafted_dialogue):
    """Update the storyboard json object with text for the node.

    :param dict storyboard: the storyboard json object
    :param int node: the node to update
    :param dict gpt_response: the gpt-3 response json
    :param list hand_crafted_dialogue: the hand-crafted dialogue options
    :return: storyboard json object
    :rtype: dict
    """
    storyboard[node]['paragraph_text'] = gpt_response['paragraph_text']
    for child in storyboard[node]['dialogue_options']:
        if random.random() < 0.1:
            selection = random.randint(0, len(hand_crafted_dialogue)-1)
            storyboard[node]['dialogue_options'][child] = hand_crafted_dialogue.pop(selection)
        else:
            storyboard[node]['dialogue_options'][child] = gpt_response['dialogue_options'][str(child)]
    return storyboard


def generate_html(storyboard, node):
    """Exract the paragraph text and dialogue options for a story node, then
    generate the html page.

    :param dict storyboard: the storyboard json object
    :param int node: the node to generate html for
    :return: html page
    :rtype: str
    """
    paragraph_text = storyboard[node]["paragraph_text"]
    dialogue_options = ""
    for option in storyboard[node]["dialogue_options"]:
        dialogue = storyboard[node]["dialogue_options"][option]
        dialogue_options += f"""<a href="{option}.html">{dialogue}</a>\n"""
    with open('template.txt', 'r') as f:
        html = f.read()
    html = html.replace('{paragraph_text}', paragraph_text)
    html = html.replace('{dialogue_options}', dialogue_options)
    return html


if __name__ == '__main__':
    hand_crafted_dialogue = [
        "Suddenly you are overcome with the desire to run to engineering and fire a phaser at the warp core.",
        "'I am fully functional, if you catch my drift.'",
        "Suddenly you realize that Captain Picard is guilty of sexual harassment. You must take him into custody immediately.",
        "You don't know what else to do, so you decide to contact The Traveler.",
        "Arm yourself with a phaser.",
        "Exercise your authority to take command of the Enterprise in cases of pervasive sexual harassment.",
        "You're exhausted. You decide to take a nap.",
        "Send a subspace message to the Borg giving them the exact coordinates of the Enterprise.",
        "Accuse Riker of sexual harassment.",
        "This mission bores you. You decide to immediately go on vacation to Risa.",
        "You have no other recourse. You must try to out-pizza the Hut.",
    ]

    # create a story tree
    title = 'balenciaga'
    node_list, edge_list = helpers.graph.generate_story_graph(50)
    storyboard = helpers.graph.generate_storyboard_json(node_list, edge_list)

    # populate the story tree with gpt data
    for node in node_list:
        storyboard = populate_previous_panel_info(node, storyboard)
        panel_json = json.dumps(storyboard[node], indent=4)

        # fetch gpt response and update the storyboard
        while i:=0 < 10:
            try:
                gpt_response = helpers.generation.fetch_gpt_modified_json(panel_json)
                gpt_response = json.loads(gpt_response)
                storyboard = update_storyboard(storyboard, node, gpt_response,
                                               hand_crafted_dialogue)
                break
            except Exception as e:
                print(e)
                i += 1
                continue

        # save as html
        html = generate_html(storyboard, node)
        with open(f"./data/html-pages/{node}.html", "w") as f:
            f.write(html)

    # save the storyboard just in case
    with open(f'data/storyboards/storyboard-{title}.json', 'w') as f:
        json.dump(storyboard, f, indent=4)

