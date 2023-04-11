from enum import Enum
from random import choice
from src.characters import Character
from src.attack_defence import AttackDefence, AttackDefenceLevel


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

    @staticmethod
    def get_random_item_from_intersection(first_list: list, second_list: list):
        first_set = set(first_list)
        second_set = set(second_list)
        return choice(first_set.intersection(second_set))

    def get_best_attack(self, attacker: Character, attack_defence: AttackDefence):
        """
        Ищем доступную атаку в следующем порядке:
        - среди заведомо проходящих ударов
        - среди даосских ударов
        - среди сложных ударов
        - среди простых ударов
        Если ничего не найдено, поднимаем эксепшн.
        :param attacker:
        :param attack_defence:
        :return:
        """
        for attack_group in [attacker.first_choice_attacks,
                             attack_defence.attacks[AttackDefenceLevel.TAOIST],
                             attack_defence.attacks[AttackDefenceLevel.ADVANCED],
                             attack_defence.attacks[AttackDefenceLevel.SIMPLE]]:
            attack = self.get_random_item_from_intersection(attack_group, attacker.current_attacks)
            if attack:
                return attack
        raise Exception(f'Не найдены атаки у персонажа {attacker.name}, '
                        f'список доступных атак: {attacker.current_attacks}')

    def round(self, attacker: Character, defender: Character, attack_defence: AttackDefence) -> FightResult:
        """

        :param attacker:
        :param defender:
        :return:
        """
        attack = self.get_best_attack()


    def round_old(self, attacker: Character, defender: Character) -> FightResult:
        """
        Если есть даосский удар - начинаем с него
        Если есть сложный - начинаем с него
        С ударом стервятника нельзя двойной урон
        Первый прошедший урон удвой
        :param attacker:
        :param defender:
        :return:
        """
        # Если у персонажа закончились удары, персонаж проиграл
        if (not attacker.current_attacks):
            if 'Повторение удара' in attacker.current_ultras:
                attacker.current_ultras.remove('Повторение удара')
                attacker.current_attacks.append(choice(attacker.attacks))
            else:
                return FightResult.FAIL

        # Если атакующий знает, что у него есть заведомо успешная атака, он может использовать ее.
        if attacker.first_choice_attacks:
            attack = attacker.first_choice_attacks
            attacker.first_choice_attacks = None
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
                attacker.first_choice_attacks = attack
                attacker.current_attacks.append(attack)
                attacker.current_ultras.remove('Повторение удара')

        # Если у противника закончились хиты, нападающий победил
        if defender.current_hits <= self.hits_to_stop_combat:
            return FightResult.WIN

        return FightResult.PROCEED

    def fight(self, attacker: Character, defender: Character, attack_defence: AttackDefence) -> int:
        # Скидываем значения перед боем
        attacker.clear_before_combat()
        defender.clear_before_combat()

        is_attacker_move = True
        fight_result = 0

        while not fight_result:
            if is_attacker_move:
                fight_result = self.round(attacker, defender).value
            else:
                fight_result = self.round(defender, attacker).value
            is_attacker_move = not is_attacker_move

        return fight_result
