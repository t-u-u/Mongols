import csv
from src.attack_defence import AttackDefence
from src.base_units import BaseUnits
from src.characters import Characters
from src.fight import Fight

def generate_characters():
    with open('data/Боевка - Удары, защиты и спецабилки.csv') as data_f:
        reader = csv.DictReader(data_f)
        attack_def_dict = AttackDefence.from_data(reader)
        attack_def_dict.check()

    with open('data/Боевка - Легенда.csv') as legend_f:
        reader = csv.DictReader(legend_f)
        base_units = BaseUnits.from_data(reader)

    with open('data/Боевка - Ничьи.csv') as draws_f:
        reader = csv.reader(draws_f)
        next(reader)
        draws = [row for row in reader]

    with open('data/Боевка - Персонажи.csv') as characters_f:
        reader = csv.DictReader(characters_f)
        characters = Characters.from_data(reader, attack_def_dict, base_units)
        characters.generate_draws(draws)

    with open('data/result.csv', 'w') as res_f:
        fieldnames = characters.HEADER
        writer = csv.DictWriter(res_f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for character in characters.to_list():
            writer.writerow(character)

    with open('data/result_for_print.csv', 'w') as res_f:
        fieldnames = characters.HEADER
        writer = csv.DictWriter(res_f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for character in characters.to_list(for_print=True):
            writer.writerow(character)

    with open('data/fight_result.csv', 'w') as fight_res_f:
        fieldnames = ['']
        fieldnames.extend([character.name for character in characters.characters])
        writer = csv.DictWriter(fight_res_f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        fight = Fight(attack_defence=attack_def_dict)
        for first_character in characters.characters:
            cur_row = {'': first_character.name}
            for second_character in characters.characters:
                if first_character != second_character:
                    cur_row[second_character.name] = fight.go_fight(first_character, second_character).name
                else:
                    cur_row[second_character.name] = ''
            writer.writerow(cur_row)


generate_characters()
