from src.fight import fight, FightResult
from src.characters import Character

class TestFight:
    def simple_fight(self):
        attacker = Character(attacks='Удар орла')
        defender = Character(defence='Защита лошади, Защита барса, Защита медведя, Защита чистой воды')
        assert fight(attacker, defender) == FightResult.WIN