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
        self.hits = int(data['Хиты'])

        self.attacks[AttackDefenceLevel.SIMPLE.value] = int(data['Простой удар']) if data['Простой удар'] else 0
        self.attacks[AttackDefenceLevel.ADVANCED.value] = int(data['Сложный удар']) if data['Сложный удар'] else 0
        self.attacks[AttackDefenceLevel.TAOIST.value] = int(data['Даосский удар']) if data['Даосский удар'] else 0

        self.defences[AttackDefenceLevel.SIMPLE.value] = int(data['Простая защита']) if data['Простая защита'] else 0
        self.defences[AttackDefenceLevel.ADVANCED.value] = int(data['Сложная защита']) if data['Сложная защита'] else 0
        self.defences[AttackDefenceLevel.TAOIST.value] = int(data['Даосская защита']) if data['Даосская защита'] else 0

        self.ultras = int(data['Случайная спецабилка']) if data['Случайная спецабилка'] else 0
        return self


@dataclass
class BaseUnits:
    units: list[BaseUnit]
    weak_units: list[BaseUnit]
    normal_units: list[BaseUnit]
    fighter_units: list[BaseUnit]
    master_units: list[BaseUnit]

    def __init__(self, units = None):
        self.units = units if units else []
        self.weak_units = []
        self.normal_units = []
        self.fighter_units = []
        self.master_units = []

    def __post_init__(self):
        self.weak_unit = [unit for unit in self.units if unit.unit_type == BaseUnitType.WEAK.value]
        self.normal_unit = [unit for unit in self.units if unit.unit_type == BaseUnitType.NORMAL.value]
        self.fighter_units = [unit for unit in self.units if unit.unit_type == BaseUnitType.FIGHTER.value]
        self.master_units = [unit for unit in self.units if unit.unit_type == BaseUnitType.MASTER.value]

    @classmethod
    def from_data(cls, data):
        return cls(units=[BaseUnit().from_data(row) for row in data])
