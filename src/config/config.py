import pathlib

# Paths
PROJECT_WD = pathlib.Path(__file__).parents[2]
"""Absolute path to the project working directory."""
DATA_DIR = PROJECT_WD / "data"
"""Absolute path to the data directory."""
SRC_DIR = PROJECT_WD / "src"
"""Absolute path to the source code directory."""
STORIES_DIR = PROJECT_WD / "webapp" / "static" / "stories"
"""Absolute path to the stories repository directory."""

# GPT
SYS_CONTENT = """You are a story generating bot for a text adventure game based on star trek the next generation.

You are tasked with writing the panel text and player options for the game. You will be given information about the overall plot, as well as the previous panel texts and player choices. Use this information to create the next panel.

In these stories, the player character is the head of the Human Resources department of the USS Enterprise.

The player choices should be absurdly banal and bureaucratic, but the story itself should be fast-paced and thrilling.
"""
"""The system content to use for the GPT API."""
USR_CONTENT = """Overall plot: {overall_plot_text}

tags: dark, thriller, mystery, espionage

This is the story leading to the current panel:

"{current_story_text}"

{instructions}
"""
"""The user content to use for the GPT API."""


# Story Generation
NUM_OF_NODES = 50
"""The number of nodes to generate in the story."""
TITLE = "balenciaga"
"""The title of the story. Will really only be used as the filename."""
OVERALL_PLOT_TEXT = "Data has noticed a disturbing trend among the senior officers on the Enterprise -- many of them have taken to wearing Balenciaga. Data has gone to the office of the player character -- the head of Human Resources on the Enterprise -- to file a complaint. But they soon learn that things are not what they seem..."
"""The overall plot of the story."""


# Misc
HAND_CRAFTED_DIALOGUE = [
    "Suddenly you are overcome with the desire to run to engineering and fire a phaser at the warp core.",
    "'I am fully functional, if you catch my drift.'",
    "You don't know what else to do, so you decide to contact The Traveler.",
    "Arm yourself with a phaser.",
    "Exercise your authority to take command of the Enterprise in cases of pervasive harassment.",
    "You're exhausted. You decide to take a nap.",
    "Send a subspace message to the Borg giving them the exact coordinates of the Enterprise.",
    "Accuse Riker of inappropriate behavior.",
    "You have no other recourse. You must try to out-pizza the Hut.",
]

