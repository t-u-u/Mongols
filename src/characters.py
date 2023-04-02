from dataclasses import dataclass
from src.attack_defence import AttackDefence, AttackDefenceLevel
from src.base_units import BaseUnit, BaseUnits, BaseUnitType
from random import sample, choice


@dataclass
class Character:
    name: str
    unit_type: BaseUnitType | None
    hits: int
    attacks: list
    defences: list
    ultras: list
    personal_ultras: str

    def __init__(self):
        self.name = ''
        self.unit_type = None
        self.hits = 0
        self.attacks = []
        self.defences = []
        self.ultras = []
        self.personal_ultras = ''

    def to_dict(self):
        full_ultras = list(self.ultras)
        if self.personal_ultras:
            full_ultras.append(self.personal_ultras)
        return {'Имя': self.name,
                'Тип': self.unit_type.value,
                'Хиты': self.hits,
                'Атаки': ', '.join(self.attacks),
                'Защиты': ', '.join(self.defences),
                'Спецабилки': ', '.join(full_ultras)}

    def fill_skills(self, attack_defence: AttackDefence, base_units: BaseUnits):
        schema: BaseUnit = choice(base_units.units_dict[self.unit_type])
        self.hits = self.hits or schema.hits

        self.attacks = []
        for attack_defence_level in AttackDefenceLevel:
            self.attacks.extend(sample(attack_defence.attacks[attack_defence_level],
                                       k=schema.attacks[attack_defence_level]))

        self.defences = []
        for attack_defence_level in AttackDefenceLevel:
            self.defences.extend(sample(attack_defence.defences[attack_defence_level],
                                        k=schema.defences[attack_defence_level]))

        self.ultras = sample(attack_defence.ultras, k=schema.ultras)

    def from_data(self, data: dict, attack_defence: AttackDefence, base_units: BaseUnits):
        self.unit_type = BaseUnitType(data['Тип'])
        self.name = data['Персонаж']
        self.hits = int(data['Хиты'] or 0)
        self.personal_ultras = data['спецабилка']
        self.fill_skills(attack_defence, base_units)

        match data['Доп.удары/защиты']:
            case 'даосская атака':
                self.attacks.append(attack_defence.attacks[AttackDefenceLevel.TAOIST][0])
            case 'даосская защита':
                self.defences.append(attack_defence.defences[AttackDefenceLevel.TAOIST][0])

        return self


@dataclass
class Characters:
    HEADER = ['Имя', 'Тип', 'Хиты', 'Атаки', 'Защиты', 'Спецабилки']
    characters: list

    @classmethod
    def from_data(cls, data, attack_defence: AttackDefence, base_units: BaseUnits):
        return cls(characters=[Character().from_data(row, attack_defence, base_units) for row in data])

    def to_list(self):
        return [character.to_dict() for character in self.characters]
