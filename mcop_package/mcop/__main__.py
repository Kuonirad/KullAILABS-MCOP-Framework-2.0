"""
M-COP v3.1 Module Entry Point

Allows running M-COP as a module:
    python -m mcop solve "problem"
    python -m mcop interactive
"""

from .cli import main

if __name__ == '__main__':
    main()