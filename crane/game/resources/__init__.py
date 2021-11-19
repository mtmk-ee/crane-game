"""A gross module with tons of global variables.

Stuff related to game configuration and resources
goes in here. Some helpers too.
"""
import json
import os
from pathlib import Path
import random
import sys
import time
from typing import List

import pygame


# PyInstaller creates a temp folder and stores path in _MEIPASS
try:
    _RESOURCE_DIR = Path(sys._MEIPASS) / 'game' / 'resources'
except BaseException as e:
    _RESOURCE_DIR = Path(__file__).parent

_CONFIG_PATH = _RESOURCE_DIR / 'config'
ICON = pygame.image.load(_RESOURCE_DIR / 'icon.ico')


# Prize resources
_PRIZE_IMAGE_DIR = _RESOURCE_DIR / 'prizes'
_PRIZE_NAMES = sorted([
    Path(name).stem
    for name in os.listdir(_PRIZE_IMAGE_DIR)
])
_PRIZE_IMAGES = {}
_SPEND_PRICE = 0.25 # back in my day...


# Background image resources
_BACKGROUND_DIR = _RESOURCE_DIR / 'backgrounds'
_BACKGROUND_PATHS = [
    _BACKGROUND_DIR / path
    for path in os.listdir(_BACKGROUND_DIR)
]
_BACKGROUND_LAST_CHANGE = time.time()
_BACKGROUND_CHANGE_INTERVAL = 15
_BACKGROUND_PATH = random.choice(_BACKGROUND_PATHS)
_BACKGROUNDS = {}


def get_prize_names() -> List[str]:
    """Returns a list of prize names.
    """
    return _PRIZE_NAMES


def get_prize_path(name: str) -> Path:
    """Returns the path to a prize image.

    Args:
        name (str): the name of the prize.

    Returns:
        A `Path` object pointing to the image.
    """
    return _PRIZE_IMAGE_DIR / (name + '.png')


def increment_prize(name: str):
    """Increments the win count for a particular type
    of prize. This value gets stored in the config.

    Args:
        name (str): the name of the prize
    """
    _CONFIG.setdefault('prizes', {}).setdefault(name, 0)
    _CONFIG['prizes'][name] += 1


def _load_config() -> dict:
    """Loads the configuration file as a dictionary, or
    returns a default dict if it doesn't exist/can't be
    parsed.

    Returns:
        The configuration dictionary
    """
    try:
        # config file stored as JSON
        with open(_CONFIG_PATH, 'r') as f:
            return json.load(f)
    except:
        return {
            'prizes': {
                name: 0
                for name in _PRIZE_NAMES
            },
            'spent': 0,
        }


def save_config():
    """Saves the configuration to disk.
    """
    try:
        # config file stored as JSON
        with open(_CONFIG_PATH, 'w') as f:
            json.dump(_CONFIG, f)
    except:
        raise


def get_total_prizes() -> int:
    """Gets the total number of prizes won across
    all types.

    Returns:
        The total number of prizes won.
    """
    count = 0
    for _, n in _CONFIG['prizes'].items():
        count += n
    return count


def get_prize_count(name: str) -> int:
    """Gets the number of prizes won of a given
    type.

    Args:
        name (str): the prize name.

    Returns:
        The number of prizes won.
    """
    _CONFIG.setdefault('prizes', {}).setdefault(name, 0)
    return _CONFIG['prizes'][name]


def get_unique_prizes() -> int:
    """Gets the number of unique prizes that have been
    won so far.

    Returns:
        The number of unique prizes won.
    """
    # Kind of a dumb way of doing it
    return len([
        _ for _, n in _CONFIG['prizes'].items()
        if n > 0
    ])


def get_prize_image(name: str) -> pygame.surface.Surface:
    """Gets the image for a particular prize.

    Args:
        name (str): the name of the prize.

    Returns:
        The prize image as a pygame Surface.
    """
    # Images are cached to avoid reading from disk a bunch
    img = _PRIZE_IMAGES.get(name.lower(), None)
    if not img:
        img = pygame.image.load(get_prize_path(name))
        _PRIZE_IMAGES[name.lower()] = img

    return img


def get_prize_price(name: str) -> float:
    """Gets the "dollar equivalent" of a prize.

    Args:
        name (str): the name of the prize.

    Returns:
        The "dollar equivalent" of the prize.
    """
    # Dumb way of doing it, but I'm too lazy to write if-else statements :)
    return {
        'Kelly': 69,
        'Mitch': 69,
    }.setdefault(name, 1)


def get_total_spent() -> float:
    """Gets the total amount spent playing the game.

    Returns:
        The total amount spent.
    """
    return _CONFIG.setdefault('spent', 0)


def get_total_won() -> float:
    """Gets the total price of prizes won.

    Returns:
        The total price of prizes won.
    """
    total = 0
    for name, count in _CONFIG['prizes'].items():
        total += count * get_prize_price(name)

    return total

def use_money():
    """Increments the amount spent in the config
    by the cost to play the game.
    """
    _CONFIG.setdefault('spent', 0)
    _CONFIG['spent'] += _SPEND_PRICE


_CONFIG = _load_config()
def get_config() -> dict:
    """Gets the configuration dictionary.

    Returns:
        The config dict.
    """
    return _CONFIG

def get_background() -> pygame.surface.Surface:
    """Gets the current background. The image returned
    changes over time.

    Returns:
        The background image as a pygame Surface.
    """
    global _BACKGROUND_LAST_CHANGE, _BACKGROUND_PATH

    # Check if it's time to change the background
    if time.time() - _BACKGROUND_LAST_CHANGE > _BACKGROUND_CHANGE_INTERVAL:
        _BACKGROUND_LAST_CHANGE = time.time()

        # Avoid getting the same image twice in a row
        new_idx = random.choice(_BACKGROUND_PATHS)
        while new_idx == _BACKGROUND_PATH:
            new_idx = random.choice(_BACKGROUND_PATHS)
        _BACKGROUND_PATH = new_idx

    # Cache the images to avoid reading them from disk every time
    image = _BACKGROUNDS.get(_BACKGROUND_PATH, None)
    if not image:
        image = pygame.image.load(_BACKGROUND_PATH)
        _BACKGROUNDS[_BACKGROUND_PATH] = image

    return image
