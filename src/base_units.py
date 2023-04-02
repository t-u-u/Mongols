from dataclasses import dataclass
from src.attack_defence import AttackDefenceLevel
from enum import Enum


class BaseUnitType(Enum):
    DEFAULT = ''
    WEAK = 'Слабый'
    NORMAL = 'Обычный'
    FIGHTER = 'Воин'
    MASTER = 'Мастер боевых искусств'


@dataclass
class BaseUnit:
    unit_type: BaseUnitType
    hits: int
    attacks: dict
    defences: dict
    ultras: int

    def __init__(self):
        self.unit_type = BaseUnitType.DEFAULT
        self.hits = 0
        self.attacks = {}
        self.defences = {}
        self.ultras = 0

    def from_data(self, data: dict):
        self.unit_type = BaseUnitType(data['Тип юнита'])
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
    weak_units: list[BaseUnit]
    normal_units: list[BaseUnit]
    fighter_units: list[BaseUnit]
    master_units: list[BaseUnit]

    @classmethod
    def from_data(cls, data):
        units = [BaseUnit().from_data(row) for row in data]
        weak_units = [unit for unit in units if unit.unit_type == BaseUnitType.WEAK]
        normal_units = [unit for unit in units if unit.unit_type == BaseUnitType.NORMAL]
        fighter_units = [unit for unit in units if unit.unit_type == BaseUnitType.FIGHTER]
        master_units = [unit for unit in units if unit.unit_type == BaseUnitType.MASTER]
        return cls(weak_units=weak_units,
                   normal_units=normal_units,
                   fighter_units=fighter_units,
                   master_units=master_units)
