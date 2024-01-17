import random
from decimal import Decimal
import json

from consts import FumoDataKeys, Rarity, FUMO_DATABASE

class Fumo:
    amount: int
    def __init__(self, rarity: str, img: str, sil: str, name: str, recent: int) -> None:
        self.rarity = rarity
        self.img = img
        self.sil = sil
        self.name = name
        self.recent = recent
    
    def __str__(self) -> str:
        return self.name

    def getAmount(self) -> int:
        with open(FUMO_DATABASE, 'r') as f:
            data = json.load(f)

            char: list[dict]
            for char in data['character']:
                if char[FumoDataKeys.nameid] == self.name:
                    self.amount = char[FumoDataKeys.amount]
                    return char[FumoDataKeys.amount]

def generateCharacter() -> Fumo:
    ''' Depending on the chance landed on, grabs a random character of that rarity's data'''

    chance = round(Decimal(random.random()), 2) # Simulates a dice roll of a random float rounded to the 2nd decimal

    if chance <= 0.02: # 2% Chance - super rare
        rarity = Rarity.super_rare

    elif chance <= 0.10: # 8% Chance - rare
        rarity = Rarity.rare

    elif chance <= 0.40: # 30% Chance - uncommon
        rarity = Rarity.uncommon

    elif chance <= 1.00: # 60% Chance - common
        rarity = Rarity.common

    with open(FUMO_DATABASE, 'r') as file:
        data = json.load(file)

        rarityList = tuple(dict_ for dict_ in data['character'] if dict_[FumoDataKeys.rarity] == rarity)

        # Picks a random character based on the rarity chosen
        chosen = random.choice(rarityList)

    return Fumo(chosen[FumoDataKeys.rarity], chosen[FumoDataKeys.img], chosen[FumoDataKeys.silouette], chosen[FumoDataKeys.nameid], chosen[FumoDataKeys.recent])

class saveData:

    def saveData(self, name: str) -> None:
        ''' +1 to the amount value of the character specified in the arguments and then updates the recent value to calculate how recent a character was pulled '''

        with open(FUMO_DATABASE, 'r+') as file:
            data = json.load(file)
            
            # Update recents list
            recentList = self.updateRecents(name)
            
            for char in data['character']:

                # Add amount collected
                if char[FumoDataKeys.nameid] == name:

                    char[FumoDataKeys.amount] += 1
                
                # Sync recent value with save file from memory
                char[FumoDataKeys.recent] = recentList[char[FumoDataKeys.nameid]]

            file.seek(0)
            file.truncate()
            
            json.dump(data, file, indent=4)


    def updateRecents(self, name: str) -> dict[str:int]:
        ''' Finds the most recent character pulled and then calculates the recentcy of each character '''
        recentList = self.recentList()
        mostRecent = recentList[name]

        recentList[name] = 0

        for key, value in recentList.items():

            if value == -1 or key == name:
                continue
            
            elif value == key or value < mostRecent:
                recentList[key] += 1

            elif value > mostRecent and mostRecent == -1:
                recentList[key] += 1

        return recentList


    def charList(self) -> list[Fumo]:
        '''Returns a list of all the characters in the fumo.json'''

        with open(FUMO_DATABASE, 'r') as file:
            data = json.load(file)

        return [
            Fumo(x[FumoDataKeys.rarity], x[FumoDataKeys.img], x[FumoDataKeys.silouette], x[FumoDataKeys.nameid], x[FumoDataKeys.recent])
                for x in data['character']
                ]


    def recentList(self) -> dict[str:int]:
        '''Returns a dictionary {fumo name : recent value}'''

        dict_: dict[str:int] = {}

        with open(FUMO_DATABASE, 'r') as file:
            data = json.load(file)

        char: list[dict]
        for char in data['character']:
            dict_[char[FumoDataKeys.nameid]] = char[FumoDataKeys.recent]

        return dict_


    def deleteData(self) -> None:
        '''
        Resets the amount values to 0
        and recent values to -1 to all characters
        '''

        with open(FUMO_DATABASE, 'r+') as file:
            data = json.load(file)

            for char in data['character']:

                if char[FumoDataKeys.amount] != 0:
                    char[FumoDataKeys.amount] = 0

                if char[FumoDataKeys.recent] != -1:
                    char[FumoDataKeys.recent] = -1
                    
            file.seek(0)
            file.truncate()

            json.dump(data, file, indent=4)
