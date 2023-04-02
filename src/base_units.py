from dataclasses import dataclass
from src.attack_defence import AttackDefenceLevel
from enum import Enum


class BaseUnitTypes(Enum):
    WEAK = 'Слабый'
    NORMAL = 'Обычный'
    FIGHTER = 'Воин'
    MASTER = 'Мастер боевых искусств'


@dataclass
class BaseUnit:
    unit_type: BaseUnitTypes | None
    hits: int
    attacks: dict
    defences: dict
    ultras: int

    def __init__(self):
        self.unit_type = None
        self.hits = 0
        self.attacks = {}
        self.defences = {}
        self.ultras = 0

    def from_data(self, data: dict):
        self.unit_type = BaseUnitTypes(data['Тип юнита'])
        self.hits = int(data['Хиты'] or 0)

        self.attacks[AttackDefenceLevel.SIMPLE.value] = int(data['Простой удар'] or 0)
        self.attacks[AttackDefenceLevel.ADVANCED.value] = int(data['Сложный удар'] or 0)
        self.attacks[AttackDefenceLevel.TAOIST.value] = int(data['Даосский удар'] or 0)

        self.defences[AttackDefenceLevel.SIMPLE.value] = int(data['Простая защита'] or 0)
        self.defences[AttackDefenceLevel.ADVANCED.value] = int(data['Сложная защита'] or 0)
        self.defences[AttackDefenceLevel.TAOIST.value] = int(data['Даосская защита'] or 0)

        self.ultras = int(data['Случайная спецабилка'] or 0)
        return self


@dataclass
class BaseUnits:
    units_dict: dict

    @classmethod
    def from_data(cls, data):
        units = [BaseUnit().from_data(row) for row in data]
        units_dict = {}
        for base_unit_type in BaseUnitTypes:
            units_dict[base_unit_type] = [unit for unit in units if unit.unit_type == base_unit_type]
        return cls(units_dict=units_dict)
