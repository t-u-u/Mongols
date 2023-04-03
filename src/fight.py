from enum import Enum
from random import choice
from src.characters import Character
from src.attack_defence import AttackDefence


class FightResult(Enum):
    PROCEED = 0
    WIN = 1
    FAIL = 2


class Fight:
    attack_queue_length: int
    hits_to_stop_combat: int

    def __init__(self, attack_queue_length: int = None, hits_to_stop_combat: int = None):
        self.attack_queue_length = attack_queue_length or 2
        self.hits_to_stop_combat = hits_to_stop_combat or 1

    def round(self, attacker: Character, defender: Character) -> FightResult:
        # Если у персонажа закончились удары, персонаж проиграл
        if (not attacker.current_attacks):
            if 'Повторение удара' in attacker.current_ultras:
                attacker.current_ultras.remove('Повторение удара')
                attacker.current_attacks.append(choice(attacker.attacks))
            else:
                return FightResult.FAIL

        # Если атакующий знает, что у него есть заведомо успешная атака, он может использовать ее.
        if attacker.first_choice_attack:
            attack = attacker.first_choice_attack
            attacker.first_choice_attack = None
        # Если нет, выбирает случайную
        else:
            attack = choice(attacker.current_attacks)
        attacker.current_attacks.remove(attack)

        required_defence = AttackDefence.get_required_defence(attack)
        # Если защита есть, спокойно применяем
        if required_defence in defender.current_defences:
            defender.current_defences.remove(required_defence)
        # Если защиты нет, но есть Уворот, применяем его
        elif 'Уворот' in defender.current_ultras:
            defender.current_ultras.remove('Уворот')
        # Если есть Повторение защиты, и нужная защита есть в известных, повторяем ее
        elif 'Повторение защиты' in defender.current_ultras:
            if required_defence in defender.defences:
                defender.current_ultras.remove('Повторение защиты')
        # Если ничего не помогло, страдать
        else:
            if ('Двойной урон' in attacker.current_ultras):
                defender.current_hits = defender.current_hits - 2
                attacker.current_ultras.remove('Двойной урон')
            else:
                defender.current_hits = defender.current_hits - 1
            # Если нападающий умеет повторять удары, успешный надо повторить
            if ('Повторение удара' in attacker.current_ultras):
                attacker.first_choice_attack = attack
                attacker.current_attacks.append(attack)
                attacker.current_ultras.remove('Повторение удара')

        # Если у противника закончились хиты, нападающий победил
        if defender.current_hits <= self.hits_to_stop_combat:
            return FightResult.WIN

        return FightResult.PROCEED

    def fight(self, attacker: Character, defender: Character) -> int:
        # Скидываем значения перед боем
        attacker.clear_before_combat()
        defender.clear_before_combat()

        self_is_attacker = True
        fight_result = 0

        while not fight_result:
            if self_is_attacker:
                fight_result = self.round(attacker, defender).value
            else:
                fight_result = self.round(defender, attacker).value
            self_is_attacker = not self_is_attacker

        return fight_result
