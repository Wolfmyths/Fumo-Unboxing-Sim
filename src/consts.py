from typing import Self
from enum import StrEnum, auto, Enum, IntEnum
import os
import random

from semantic_version import Version

class Rarity(StrEnum):
    common     = auto()
    uncommon   = auto()
    rare       = auto()
    super_rare = 'super rare'

class FumoDataKeys(StrEnum):
    rarity    = auto()
    nameid    = 'name'
    img       = auto()
    silouette = auto()
    amount    = auto()
    recent    = auto()

class InventorySortValues(IntEnum):
    rarity = auto()
    amount = auto()
    recent = auto()
    abc    = auto()

class WindowTitles(Enum):
    main_menu = ('ᗜˬᗜ', 'Becoming Fumo')
    gacha     = ('What will you get?', 'Luckiest fumo collector?', 'ᗜˬᗜ')
    inventory = ('Flexing the Fumos ᗜˬᗜ', 'Your most prized posessions', 'ᗜˬᗜ')

    def getTitle(state: Self) -> str:
        return random.choice(state.value)

ROOT          = os.getcwd()
STYLESHEET    = os.path.abspath(os.path.join(ROOT, 'src', 'style.qss'))
ICON          = os.path.abspath(os.path.join(ROOT, 'icon.png'))
FUMO_DATABASE = os.path.abspath(os.path.join(ROOT, 'src', 'fumo-data.json'))

VERSION       = Version(major=1, minor=0, patch=0)
