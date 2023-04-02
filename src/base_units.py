from dataclasses import dataclass
from src.attack_defence import AttackDefenceLevel
from enum import Enum


class BaseUnitType(Enum):
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

    @classmethod
    def from_data(cls, data: dict):
        unit_type = BaseUnitType(data['Тип юнита'])
        hits = int(data['Хиты'] or 0)

        attacks = {}
        attacks[AttackDefenceLevel.SIMPLE] = int(data['Простой удар'] or 0)
        attacks[AttackDefenceLevel.ADVANCED] = int(data['Сложный удар'] or 0)
        attacks[AttackDefenceLevel.TAOIST] = int(data['Даосский удар'] or 0)

        defences = {}
        defences[AttackDefenceLevel.SIMPLE] = int(data['Простая защита'] or 0)
        defences[AttackDefenceLevel.ADVANCED] = int(data['Сложная защита'] or 0)
        defences[AttackDefenceLevel.TAOIST] = int(data['Даосская защита'] or 0)

        ultras = int(data['Случайная спецабилка'] or 0)
        return cls(unit_type=unit_type, hits=hits, attacks=attacks, defences=defences, ultras=ultras)


@dataclass
class BaseUnits:
    units_dict: dict

    @classmethod
    def from_data(cls, data):
        units = [BaseUnit.from_data(row) for row in data]
        units_dict = {}
        for base_unit_type in BaseUnitType:
            units_dict[base_unit_type] = [unit for unit in units if unit.unit_type == base_unit_type]
        return cls(units_dict=units_dict)
