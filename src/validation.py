from src.characters import Character
from dataclasses import dataclass
from src.base_units import BaseUnitType


@dataclass
class CombatStatistics:
    wins: int
    draws: int
    fails: int


@dataclass
class CharacterStanging:
    name: str
    unit_type: BaseUnitType
    results: list[dict]

    def to_print(self):
        return {'Атакующий персонаж/Защищающийся персонаж': self.name,
                'Тип': self.unit_type.value}.update(self.results)


class CharactersStandings:
    header: list = None
    data: list = None

    def data_to_print(self):
        return [char_standing.to_print for char_standing in self.data]


class Validation:
    standings: CharactersStandings = None

    def if_draw(self, first_char: Character, second_char: Character):
        return (self.standings[first_char][second_char].contains('|0|'))
