from enum import Enum
from random import choice
from src.characters import Character


class FightResult(Enum):
    PROCEED = 0
    WIN = 1
    FAIL = 2


def round(attacker: Character, defender: Character) -> FightResult:
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

    required_defence = attack.replace('Удар', 'Защита')
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
    if defender.current_hits <= 0:
        return FightResult.WIN

    return FightResult.PROCEED


def fight(attacker: Character, defender: Character) -> FightResult:
    """
    It's assumed that current character starts this fight
    :param defender: other Character
    :return: True if character win in fight with other character
    """
    # Скидываем значения перед боем
    attacker.current_hits = attacker.hits
    attacker.current_attacks = attacker.attacks
    attacker.current_defences = attacker.defences
    attacker.current_ultras = attacker.full_ultras

    defender.current_hits = defender.hits
    defender.current_attacks = defender.attacks
    defender.current_defences = defender.defences
    defender.current_ultras = defender.full_ultras

    attacker.first_choice_attack = None
    defender.first_choice_attack = None

    self_is_attacker = True
    fight_result = 0

    while not fight_result:
        if self_is_attacker:
            fight_result = round(attacker, defender).value
        else:
            fight_result = round(defender, attacker).value
        self_is_attacker = not self_is_attacker

    return fight_result
