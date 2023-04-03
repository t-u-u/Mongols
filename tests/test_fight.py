from src.fight import Fight, FightResult
from src.characters import Character


class TestFight:
    def test_simple_fight(self):
        attacker = Character(attacks=['Удар орла'], hits=1)
        defender = Character(defences=['Защита лошади', 'Защита барса', 'Защита медведя', 'Защита чистой воды'], hits=1)
        assert Fight().fight(attacker, defender) == FightResult.WIN.value
