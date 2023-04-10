
PROMPT = """you are StoryBot, a game master bot that generates thrilling stories for text-based adventure games."""

QUERY = """i'm making a text based rpg called "Star Trek: HR". it's about an HR officer named "Carl" who works on the uss enterprise 1701-D. in this game, the user will be presented with a single paragraph of text and a set of dialogue options to choose from. each dialogue option moves to a new scene.

your job is to write a paragraph of text and dialogue options for each scene.

i will give you a JSON string. you will fill in the MASKS. here is an example. if i gave you:

{{
    "parent": 0,
    "is_leaf": false,
    "previous_paragraph": "This is just filler text."
    "previous_dialogue_option": "This is just filler text."
    "paragraph_text": "[MASK]",
    "dialogue_options": {{
        "2": "[MASK]",
        "1": "[MASK]"
    }}
}}

then you would replace each MASK with text:

{{
    "parent": 0,
    "is_leaf": false,
    "previous_paragraph": "This is just filler text.",
    "previous_dialogue_option": "This is just filler text.",
    "paragraph_text": "<a paragraph of text written by you>",
    "dialogue_options": {{
        "2": "<a dialogue option written by you>",
        "1": "<a dialogue option written by you>"
    }}
}}

you may ONLY replace masks. nothing else. if you replace anything else, i will not accept your submission.
if 'parent' is null, then this is the first scene.
if 'is_leaf' is true, then the paragraph must end the story with the destruction of the enterprise.

this story is a dark psychological thriller with many shocking twists and turns. it begins with Carl noticing that a large number of the crew have begun wearing balenciaga. even the captain. however, not all is what it seems...

here is the JSON string:

{JSON}

"""
