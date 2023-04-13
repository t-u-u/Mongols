import csv
import logging

from src.attack_defence import AttackDefence
from src.characters import Character
from src.fight import Fight, FightResult


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
        defender = Character(defences=['Защита лошади', 'Защита барса', 'Защита медведя', 'Защита чистой воды'], hits=2)

        assert self.fight.go_fight(attacker, defender) == FightResult.WIN

    def test_draw(self):
        attacker = Character(attacks=['Удар орла', 'Удар барса', 'Удар журавля'],
                             defences=['Защита медведя', 'Защита лошади', 'Защита журавля'],
                             hits=2)
        defender = Character(attacks=['Удар медведя', 'Удар лошади', 'Удар журавля'],
                             defences=['Защита орла', 'Защита барса', 'Защита журавля'],
                             hits=2)
        assert self.fight.go_fight(attacker, defender) == FightResult.DRAW

    def test_attacker_fails(self):
        attacker = Character(attacks=['Удар орла', 'Удар барса', 'Удар журавля'],
                             defences=['Защита медведя', 'Защита лошади'],
                             hits=5)
        defender = Character(attacks=['Удар медведя', 'Удар лошади', 'Удар журавля'],
                             defences=['Защита орла', 'Защита барса', 'Защита журавля'],
                             hits=5)
        assert self.fight.go_fight(attacker, defender) == FightResult.FAIL

    def test_ultra_double_damage(self):
        attacker = Character(name='Атакующий Вася',
                             attacks=['Удар барса', 'Удар барса', 'Удар барса'],
                             defences=['Защита лошади', 'Защита лошади', 'Защита лошади'],
                             hits=3)
        defender = Character(name='Защищающийся Петя',
                             attacks=['Удар медведя', 'Удар медведя', 'Удар медведя'],
                             defences=['Защита орла', 'Защита журавля', 'Защита лошади'],
                             ultras=['Двойной урон'],
                             hits=3)
        assert self.fight.go_fight(attacker, defender) == FightResult.FAIL

    def test_ultra_retry_defence(self):
        attacker = Character(name='Вася',
                             attacks=['Удар лошади', 'Удар лошади', 'Удар орла'],
                             defences=['Защита орла', 'Защита журавля', 'Защита барса'],
                             hits=4)
        defender = Character(name='Петя',
                             attacks=['Удар лошади', 'Удар стервятника', 'Удар медведя'],
                             defences=['Защита лошади', 'Защита орла', 'Защита стервятника'],
                             ultras=['Повторение защиты'],
                             hits=2)
        assert self.fight.go_fight(attacker, defender) == FightResult.FAIL

    def test_ultra_specific_characters(self):
        attacker = Character(name='Хайюнь',
                             attacks=['Удар лошади', 'Удар журавля', 'Удар медведя', 'Удар орла',
                                      'Удар стервятника', 'Удар водяного вихря'],
                             defences=['Защита медведя', 'Защита журавля', 'Защита барса', 'Защита орла',
                                       'Защита скорпиона', 'Защита водяного вихря'],
                             ultras=['Повторение атаки'],
                             hits=5)
        defender = Character(name='Ходжа Насреддин',
                             attacks=['Удар лошади', 'Удар барса', 'Удар медведя'],
                             defences=['"Защита лошади', 'Защита орла', 'Защита стервятника'],
                             ultras=['Повторение защиты'],
                             hits=5)
        assert self.fight.go_fight(attacker, defender) == FightResult.WIN