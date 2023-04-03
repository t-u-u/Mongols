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

    def get_all_defences(self):
        all_defences = []
        for attack_defence_level in AttackDefenceLevel:
            all_defences.extend(self.attacks[attack_defence_level])

    def get_all_attacks(self):
        all_attacks = []
        for attack_defence_level in AttackDefenceLevel:
            all_attacks.extend(self.attacks[attack_defence_level])

    @classmethod
    def get_required_defence(cls, attack: str):
        return attack.replace('Удар', 'Защита')

    @classmethod
    def get_required_attack(cls, defence: str):
        return defence.replace('Защита', 'Удар')

    def check(self):
        for attack in self.get_all_attacks():
            defence = self.get_required_defence(attack)
            if defence not in self.get_all_defences():
                raise ValueError(f'Не найдена защита "{defence}" для удара "{attack}".')
        for defence in self.get_all_defences():
            attack = self.get_required_attack()
            if attack not in self.get_all_attacks():
                raise ValueError(f'Не найден удар "{attack}" для защиты "{defence}".')
