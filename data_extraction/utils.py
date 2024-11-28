# utils.py

import os

def ensure_output_folder(output_folder):
    """
    Ensure that the output folder exists; create it if it doesn't.

    Args:
        output_folder (str): The path to the output folder.

    Returns:
        None
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
