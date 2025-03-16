"""Utility functions for the AI Interview Scheduler application."""

import random
import string


def generate_meet_link() -> str:
    """Generate a random Google Meet link.

    Returns:
        str: A randomly generated Google Meet URL in the format 
             'https://meet.google.com/xxx-xxx-xxx' where x are alphanumeric characters.
    """
    chars = string.ascii_letters + string.digits
    code = ''.join(random.choices(chars, k=10))
    return f"https://meet.google.com/{code}-{code[:3]}-{code[3:6]}"
