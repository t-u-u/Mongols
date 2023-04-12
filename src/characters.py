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
    personal_ultras: list

    current_hits: int
    current_attacks: list
    current_defences: list
    current_ultras: list
    first_choice_attacks: list[str]
    attack_queue: list[str]
    defence_queue: list[str]

    def __init__(self, hits=None, attacks=None, defences=None, full_ultras=None):
        # Базовые характеристики
        self.name = ''
        self.unit_type = None
        self.hits = hits or 0
        self.attacks = attacks or []
        self.defences = defences or []
        self.ultras = []
        self.personal_ultras = []

        # Характеристики для конкретного боя
        self.current_hits = 0
        self.current_attacks = []
        self.current_defences = []
        self.current_ultras = []
        self.first_choice_attacks = []
        self.attack_queue = []
        self.defence_queue = []

    def to_dict(self, for_print: bool = False):
        if for_print:
            delimiter = '\n'
        else:
            delimiter = ', '
        return {'Имя': self.name,
                'Тип': self.unit_type.value,
                'Хиты': self.hits,
                'Атаки': (delimiter.join(self.attacks)).strip(delimiter),
                'Защиты': (delimiter.join(self.defences)).strip(delimiter),
                'Спецабилки': (delimiter.join(self.ultras)).strip(delimiter)}

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
        self.ultras.extend(self.personal_ultras)

    def from_data(self, data: dict, attack_defence: AttackDefence, base_units: BaseUnits):
        self.unit_type = BaseUnitType(data['Тип'])
        self.name = data['Персонаж']
        self.hits = int(data['Хиты'] or 0)
        self.personal_ultras = [personal_ultra.capitalize() for personal_ultra in data['спецабилка'].split(', ')]
        self.fill_skills(attack_defence, base_units)

        match data['Доп.удары/защиты']:
            case 'даосская атака':
                self.attacks.append(attack_defence.attacks[AttackDefenceLevel.TAOIST][0])
            case 'даосская защита':
                self.defences.append(attack_defence.defences[AttackDefenceLevel.TAOIST][0])
        return self

    def from_other_character_to_draw(self, other):
        """
        Для персонажей одинакового типа, у которых должна быть ничья, задаем атаки и защиты друг от друга.
        :param other:
        :return:
        """
        if not other.unit_type:
            raise ValueError(f'Не задан тип персонажа {other.name}')
        elif self.unit_type != other.unit_type:
            raise ValueError(f'У персонажа {self.name} тип юнита {self.unit_type}, а у персонажа {other.name} '
                             f'тип юнита {other.unit_type}. Нельзя сделать автоматическую ничью.')
        else:
            self.attacks = []
            self.defences = []
            for attack in other.attacks:
                self.defences.append(AttackDefence.get_required_defence(attack))
            for defence in other.defences:
                self.attacks.append(AttackDefence.get_required_attack(defence))
        return self

    def clear_before_combat(self):
        self.current_hits = self.hits
        self.current_attacks = self.attacks
        self.current_defences = self.defences
        self.current_ultras = self.ultras
        self.first_choice_attacks = []
        self.attack_queue = []
        self.defence_queue = []


@dataclass
class Characters:
    HEADER = ['Имя', 'Тип', 'Хиты', 'Атаки', 'Защиты', 'Спецабилки']
    characters: list = None

    @classmethod
    def from_data(cls, data, attack_defence: AttackDefence, base_units: BaseUnits):
        return cls(characters=[Character().from_data(row, attack_defence, base_units) for row in data])

    def get_character_by_name(self, name: str) -> Character:
        for character in self.characters:
            if character.name == name:
                return character

    def generate_draws(self, draws: list):
        # self.from_data(data, attack_defence, base_units)
        for character_name1, character_name2 in draws:
            character1 = self.get_character_by_name(character_name1)
            character2 = self.get_character_by_name(character_name2)
            character1.from_other_character_to_draw(character2)
        return self

    def to_list(self, for_print: bool = False):
        return [character.to_dict(for_print) for character in self.characters]