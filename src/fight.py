import random
from enum import Enum
from random import choice
from src.characters import Character
from src.attack_defence import AttackDefence, AttackDefenceLevel
import logging


class FightResult(Enum):
    DRAW = 0
    WIN = 1
    FAIL = 2


class Fight:
    attack_defence_queue_length: int = 2
    hits_to_stop_combat: int = 1
    rounds_before_draw: int = 20

    attack_defence: AttackDefence
    attacker: Character = None
    defender: Character = None
    current_attack: str = None
    is_attack_successful: bool = False

    def __init__(self, attack_defence: AttackDefence):
        self.attack_defence = attack_defence

    @staticmethod
    def get_random_item_from_intersection(first_list: list, second_list: list):
        first_set = set(first_list)
        second_set = set(second_list)
        res_intersection = list(first_set.intersection(second_set))
        if res_intersection:
            return choice(res_intersection)
        return None

    def add_attack_defence_to_queue(self, original_list, queue, item):
        original_list.remove(item)
        queue.append(item)
        if len(queue) > self.attack_defence_queue_length:
            original_list.append(queue.pop(0))

    def try_to_attack(self):
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
        logging.debug(f'{self.attacker.name}\n'
                      f'Доступные атаки:\n{self.attacker.current_attacks}\n'
                      f'Очередь атак: {self.attacker.attack_queue}'
                      f'Ультры: {self.attacker.current_ultras}')
        # Ищем атаку среди доступных в следующем порядке: сначала даосскую, потом сильную, только потом простую
        for attack_group in [self.attacker.first_choice_attacks,
                             self.attack_defence.attacks[AttackDefenceLevel.TAOIST],
                             self.attack_defence.attacks[AttackDefenceLevel.ADVANCED],
                             self.attack_defence.attacks[AttackDefenceLevel.SIMPLE]]:
            attack = Fight.get_random_item_from_intersection(attack_group, self.attacker.current_attacks)
            if attack:
                self.add_attack_defence_to_queue(self.attacker.current_attacks, self.attacker.attack_queue, attack)
                self.current_attack = attack
                logging.info(f'{self.attacker.name}: {self.current_attack}')

                # Если есть спецабилка "Повтор удара", с 50% вероятностью повторяем сильную или даосскую атаку
                if ('Повторение удара' in self.attacker.current_ultras):
                    if (attack in self.attack_defence.attacks[AttackDefenceLevel.TAOIST]) or \
                            (attack in self.attack_defence.attacks[AttackDefenceLevel.ADVANCED]):
                        if choice([True, False]):
                            self.attacker.current_attacks.append(self.current_attack)
                            self.attacker.attack_queue.remove(self.current_attack)
                            self.attacker.first_choice_attacks.append(self.current_attack)
                            self.attacker.current_ultras.remove('Повторение удара')
                            logging.info(
                                f'{self.attacker.name}: Повторение удара. {self.current_attack} вернулся в доступные\n')

                return self
        raise Exception(f'Не найдены атаки у персонажа {self.attacker.name}, '
                        f'список доступных атак: {self.attacker.current_attacks},'
                        f'список атак: {self.attacker.attacks}')

    def try_to_defend(self):
        """

        :param defender:
        :param attack:
        :return: True если защита прошла успешно, False если нет
        """
        logging.debug(f'{self.defender.name}\n'
                      f'Доступные защиты:\n{self.defender.current_defences}\n'
                      f'Очередь защит: {self.defender.defence_queue}\n'
                      f'Ультры: {self.defender.current_ultras}')
        required_defence = AttackDefence.get_required_defence(self.current_attack)
        # Если защита есть, спокойно применяем
        if required_defence in self.defender.current_defences:
            logging.info(f'{self.defender.name}: {required_defence}\n')
            self.add_attack_defence_to_queue(self.defender.current_defences, self.defender.defence_queue, required_defence)
            # Если от атаки есть штатная защита, убираем ее из атак первого выбора.
            if self.current_attack in self.attacker.first_choice_attacks:
                self.attacker.first_choice_attacks.remove(self.current_attack)
        # Если защиты нет, но есть Уворот, применяем его
        elif 'Уворот' in self.defender.current_ultras:
            logging.info(f'{self.defender.name}: Уворот\n')
            self.defender.current_ultras.remove('Уворот')
            # Удар, от которого применили спецабилку, добавляем в атаки первого выбора
            self.attacker.first_choice_attacks.append(self.current_attack)
        # Если есть Повторение защиты, и нужная защита есть в известных, повторяем ее
        elif ('Повторение защиты' in self.defender.current_ultras) \
                and (required_defence in self.defender.defence_queue):
            logging.info(f'{self.defender.name}: Повторение защиты {required_defence}\n')
            self.defender.current_ultras.remove('Повторение защиты')
            # Добавляем переиспользованную защиту в очередь заново
            self.defender.defence_queue.remove(required_defence)
            self.defender.defence_queue.append(required_defence)
        else:
            logging.info('Атака прошла успешно')
            # Успешный удар добавляем в атаки первого выбора
            self.attacker.first_choice_attacks.append(self.current_attack)
            self.is_attack_successful = True
            return self
        self.is_attack_successful = False
        return self

    def calculate_attack_result(self) -> bool:
        """

        :return: True if attacker wins, and False if still not
        """
        if self.is_attack_successful:
            # Если есть двойной урон, применяем
            if ('Двойной урон' in self.attacker.current_ultras):
                logging.info(f'{self.attacker.name}: Двойной урон\n')
                self.defender.current_hits = self.defender.current_hits - 2
                self.attacker.current_ultras.remove('Двойной урон')
            else:
                self.defender.current_hits = self.defender.current_hits - 1
            logging.info(f'Хиты {self.defender.name}: {self.defender.current_hits}\n')

            # Если нападающий умеет повторять удары, успешный надо вернуть в стэк
            if ('Повторение удара' in self.attacker.current_ultras):
                self.attacker.current_attacks.append(self.current_attack)
                self.attacker.attack_queue.remove(self.current_attack)
                self.attacker.current_ultras.remove('Повторение удара')
                logging.info(f'{self.attacker.name}: Повторение удара. {self.current_attack} вернулся в доступные\n')

            # Если у противника закончились хиты, нападающий победил
            if self.defender.current_hits <= self.hits_to_stop_combat:
                return True
        return False

    def round(self) -> bool:
        """
        :param attacker:
        :param defender:
        :return: True if attacker wins, and False if still not
        """
        logging.debug(f'____________________________\n{self.attacker.name} -> {self.defender.name}.')
        self.try_to_attack()
        self.try_to_defend()
        return self.calculate_attack_result()

    def go_fight(self, attacker: Character, defender: Character) -> FightResult:
        # Скидываем значения перед боем
        self.attacker = attacker
        self.defender = defender
        self.attacker.clear_before_combat()
        self.defender.clear_before_combat()

        logging.info(f'Начат бой между персонажами {self.attacker.name} и {self.defender.name}.\n'
                     f'{self.attacker.name}\n'
                     f'Хиты: {self.attacker.current_hits}\n'
                     f'Атаки: {self.attacker.current_attacks}\n'
                     f'Защиты: {self.attacker.current_defences}\n'
                     f'Ультры: {self.attacker.current_ultras}\n\n'
                     f'{self.defender.name}\n'
                     f'Хиты: {self.defender.current_hits}\n'
                     f'Атаки: {self.defender.current_attacks}\n'
                     f'Защиты: {self.defender.current_defences}\n'
                     f'Ультры: {self.defender.current_ultras}\n\n')

        is_attacker_move = True
        fight_result = FightResult.DRAW
        round_counter = 0

        while (not fight_result.value) and (round_counter < self.rounds_before_draw):
            if is_attacker_move:
                self.attacker = attacker
                self.defender = defender
                if self.round():
                    logging.info(f'{self.attacker.name} победил.')
                    fight_result = FightResult.WIN
            else:
                self.attacker = defender
                self.defender = attacker
                if self.round():
                    logging.info(f'{self.attacker.name} победил.')
                    fight_result = FightResult.FAIL
            is_attacker_move = not is_attacker_move
            round_counter += 1

        if fight_result == FightResult.DRAW:
            logging.info(f'У {self.attacker.name} и {self.defender.name} ничья.')
        return fight_result
