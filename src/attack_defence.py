from dataclasses import dataclass
from enum import Enum


class AttackDefenceLevel(Enum):
    SIMPLE = 'простой'
    ADVANCED = 'сложный'
    TAOIST = 'даосский'


class AttackDefenceType(Enum):
    HIT = 'удар'
    DEFENCE = 'защита'
    ULTRA = 'спецабилка'
    PERSONAL_ULTRA = 'личная спецабилка'


@dataclass
class AttackDefence:
    attacks: dict
    defences: dict
    ultras: list
    personal_ultras: list

    def __init__(self):
        self.attacks = {}
        self.defences = {}
        self.ultras = []
        self.personal_ultras = []

    def from_data(self, data):
        for row in data:
            match row['Тип для скрипта'].lower():
                case AttackDefenceType.HIT.value:
                    self.attacks[row['Название']] = row['Уровень для скрипта'].lower()
                case AttackDefenceType.DEFENCE.value:
                    self.defences[row['Название']] = row['Уровень для скрипта'].lower()
                case AttackDefenceType.ULTRA.value:
                    self.ultras.append(row['Название'])
                case AttackDefenceType.PERSONAL_ULTRA.value:
                    self.personal_ultras.append(row['Название'])
        return self
