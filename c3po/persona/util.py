"""Utility functions for personas"""


def should_mention(should_add_mention):
    """Decorator to add a should_mention return value to contents."""
    def dec(func):
        """Returning the function object."""
        def wrapper(*args, **kwargs):
            """Returning the function value and the should_add_mention var."""
            return func(*args, **kwargs), should_add_mention

        return wrapper

    return dec
