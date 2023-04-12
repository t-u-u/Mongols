from src.fight import Fight, FightResult
from src.characters import Character
import csv
from src.attack_defence import AttackDefence


class TestFight:
    attack_defence: AttackDefence = None
    fight: Fight = None

    def setup_class(self):
        with open('../data/Боевка - Удары, защиты и спецабилки.csv') as data_f:
            reader = csv.DictReader(data_f)
            attack_def_dict = AttackDefence.from_data(reader)
            attack_def_dict.check()
        self.attack_defence = attack_def_dict
        self.fight = Fight(attack_defence=self.attack_defence)

    def test_simple_fight(self):
        attacker = Character(attacks=['Удар орла'], hits=1)
        defender = Character(defences=['Защита лошади', 'Защита барса', 'Защита медведя', 'Защита чистой воды'], hits=1)

        assert self.fight.fight(attacker, defender) == FightResult.WIN
    def test_draw(self):
        attacker = Character(attacks=['Удар орла', 'Удар барса', 'Удар журавля'],
                             defences=['Защита медведя', 'Защита лошади', 'Защита журавля'],
                             hits=2)
        defender = Character(attacks=['Удар медведя', 'Удар лошади', 'Удар журавля'],
                             defences=['Защита орла', 'Защита барса', 'Защита журавля'],
                             hits=2)
        assert self.fight.fight(attacker, defender) == FightResult.DRAW

    def test_attacker_fails(self):
        attacker = Character(attacks=['Удар орла', 'Удар барса', 'Удар журавля'],
                             defences=['Защита медведя', 'Защита лошади'],
                             hits=2)
        defender = Character(attacks=['Удар медведя', 'Удар лошади', 'Удар журавля'],
                             defences=['Защита орла', 'Защита барса', 'Защита журавля'],
                             hits=2)
        assert self.fight.fight(attacker, defender) == FightResult.FAIL

    def test_ultra(self):
        attacker = Character(attacks=['Удар барса', 'Удар барса', 'Удар барса'],
                             defences=['Защита лошади', 'Защита лошади', 'Защита лошади'],
                             full_ultras=['Двойной урон'],
                             hits=2)
        defender = Character(attacks=['Удар медведя', 'Удар медведя', 'Удар медведя'],
                             defences=['Защита орла', 'Защита журавля', 'Защита лошади'],
                             hits=2)
        assert self.fight.fight(attacker, defender) == FightResult.WIN
