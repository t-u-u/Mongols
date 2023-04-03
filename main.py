import csv
from src.attack_defence import AttackDefence
from src.base_units import BaseUnits
from src.characters import Characters


def main():
    with open('data/Боевка - Удары, защиты и спецабилки.csv') as data_f:
        reader = csv.DictReader(data_f)
        attack_def_dict = AttackDefence.from_data(reader)
        attack_def_dict.check()

    with open('data/Боевка - Легенда.csv') as legend_f:
        reader = csv.DictReader(legend_f)
        base_units = BaseUnits.from_data(reader)

    with open('data/Боевка - Персонажи.csv') as characters_f:
        reader = csv.DictReader(characters_f)
        characters = Characters.from_data(reader, attack_def_dict, base_units)

    with open('data/result.csv', 'w') as res_f:
        fieldnames = characters.HEADER
        writer = csv.DictWriter(res_f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for character in characters.to_list():
            writer.writerow(character)


main()
