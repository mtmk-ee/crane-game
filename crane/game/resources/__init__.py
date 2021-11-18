import json
import os
import sys
from pathlib import Path
import random
import time

import pygame

try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    _RESOURCE_DIR = Path(sys._MEIPASS) / 'game' / 'resources'
except BaseException as e:
    _RESOURCE_DIR = Path(__file__).parent
_PRIZE_IMAGE_DIR = _RESOURCE_DIR / 'prizes'
_BACKGROUND_DIR = _RESOURCE_DIR / 'backgrounds'

_PRIZE_NAMES = sorted([
    Path(name).stem
    for name in os.listdir(_PRIZE_IMAGE_DIR)
])
_PRIZE_IMAGES = {}
_CONFIG_PATH = _RESOURCE_DIR / 'config'
_SPEND_PRICE = 0.25

_BACKGROUND_PATHS = [
    _BACKGROUND_DIR / path
    for path in os.listdir(_BACKGROUND_DIR)
]
_BACKGROUND_LAST_CHANGE = time.time()
_BACKGROUND_CHANGE_INTERVAL = 10
_BACKGROUND_PATH = random.choice(_BACKGROUND_PATHS)
_BACKGROUNDS = {}


ICON = pygame.image.load(_RESOURCE_DIR / 'icon.ico')


def get_prize_names():
    return _PRIZE_NAMES

def get_prize_path(name: str):
    return _PRIZE_IMAGE_DIR / (name + '.png')

def increment_prize(name: str):
    _CONFIG.setdefault('prizes', {}).setdefault(name, 0)
    _CONFIG['prizes'][name] += 1

def _load_config():
    try:
        with open(_CONFIG_PATH, 'r') as f:
            return json.load(f)
    except:
        print('Could not load config')
        return {
            'prizes': {
                name: 0
                for name in _PRIZE_NAMES
            },
            'spent': 0,
        }


def save_config():
    try:
        with open(_CONFIG_PATH, 'w') as f:
            json.dump(_CONFIG, f)
    except:
        raise

def get_total_prizes():
    count = 0
    for _, n in _CONFIG['prizes'].items():
        count += n
    return count

def get_prize_count(name: str):
    _CONFIG.setdefault('prizes', {}).setdefault(name, 0)
    return _CONFIG['prizes'][name]

def get_unique_prizes():
    return len([
        _ for _, n in _CONFIG['prizes'].items()
        if n > 0
    ])

def get_prize_image(name: str):
    img = _PRIZE_IMAGES.get(name.lower(), None)
    if not img:
        img = pygame.image.load(get_prize_path(name))
        _PRIZE_IMAGES[name.lower()] = img
    return img

def get_prize_price(name: str) -> float:
    return {
        'Kelly': 69,
        'Mitch': 69,
    }.setdefault(name, 1)

def get_total_spent() -> float:
    return _CONFIG.setdefault('spent', 0)

def get_total_won() -> float:
    total = 0
    for name, count in _CONFIG['prizes'].items():
        total += count * get_prize_price(name)
    return total

def use_money():
    _CONFIG.setdefault('spent', 0)
    _CONFIG['spent'] += _SPEND_PRICE


_CONFIG = _load_config()
def get_config():
    return _CONFIG



def get_background():
    global _BACKGROUND_LAST_CHANGE, _BACKGROUND_PATH
    if time.time() - _BACKGROUND_LAST_CHANGE > _BACKGROUND_CHANGE_INTERVAL:
        _BACKGROUND_LAST_CHANGE = time.time()
        new_idx = random.choice(_BACKGROUND_PATHS)
        while new_idx == _BACKGROUND_PATH:
            new_idx = random.choice(_BACKGROUND_PATHS)
        _BACKGROUND_PATH = new_idx

    image = _BACKGROUNDS.get(_BACKGROUND_PATH, None)
    if not image:
        image = pygame.image.load(_BACKGROUND_PATH)
        _BACKGROUNDS[_BACKGROUND_PATH] = image
    return image
