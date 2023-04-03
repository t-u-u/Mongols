from dataclasses import dataclass
from enum import Enum
from src.fight import get_required_defence


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

    full_attacks: list
    full_defences: list

    @classmethod
    def from_data(cls, data):
        attacks = {attack_defence_level: [] for attack_defence_level in AttackDefenceLevel}
        defences = {attack_defence_level: [] for attack_defence_level in AttackDefenceLevel}
        ultras = []
        personal_ultras = []

        for row in data:
            match row['Тип для скрипта'].lower():
                case AttackDefenceType.HIT.value:
                    attacks[AttackDefenceLevel(row['Уровень для скрипта'].lower())].append(row['Название'])
                case AttackDefenceType.DEFENCE.value:
                    defences[AttackDefenceLevel(row['Уровень для скрипта'].lower())].append(row['Название'])
                case AttackDefenceType.ULTRA.value:
                    ultras.append(row['Название'])
                case AttackDefenceType.PERSONAL_ULTRA.value:
                    personal_ultras.append(row['Название'])
        return cls(attacks=attacks, defences=defences, ultras=ultras, personal_ultras=personal_ultras)

    def get_full_defences(self):
        full_defences = []
        for attack_defence_level in AttackDefenceLevel:
            full_defences.extend(self.attacks[attack_defence_level])

    def get_full_attacks(self):
        full_attacks = []
        for attack_defence_level in AttackDefenceLevel:
            full_attacks.extend(self.attacks[attack_defence_level])

    def check(self):
        for attack in self.get_full_attacks():
            get_required_defence(attack)
