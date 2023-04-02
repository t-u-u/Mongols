import csv
from src.attack_defence import AttackDefence
from src.base_units import BaseUnits

def main():
    with open('data/Боевка - Удары, защиты и спецабилки.csv') as data_f:
        reader = csv.DictReader(data_f)
        attack_def_dict = AttackDefence().from_data(reader)

    with open('data/Боевка - Легенда.csv') as legend_f:
        reader = csv.DictReader(legend_f)
        base_units = BaseUnits().from_data(reader)

    print(base_units)


    #     res = []
    #     for row in reader:
    #         unit_hits = []
    #         unit_defenses = []
    #         ultra = ''
    #         if row['Простой удар']:
    #             unit_hits.extend(sample([hit for hit, hit_type in hits.items() if hit_type.lower() == 'простой'],
    #                                      k=int(row['Простой удар'])))
    #         if row['Сложный удар']:
    #             unit_hits.extend(sample([hit for hit, hit_type in hits.items() if hit_type.lower() == 'сложный'],
    #                                      k=int(row['Сложный удар'])))
    #         if row['Даосский удар']:
    #             unit_hits.append('Даосский удар')
    #
    #         if row['Простая защита']:
    #             unit_defenses.extend(sample([defense for defense, defense_type in defenses.items()
    #                                          if defense_type.lower() == 'простой'],
    #                                         k=int(row['Простая защита'])))
    #         if row['Сложная защита']:
    #             unit_defenses.extend(sample([defense for defense, defense_type in defenses.items()
    #                                          if defense_type.lower() == 'сложный'],
    #                                         k=int(row['Сложная защита'])))
    #         if row['Даосская защита']:
    #             unit_defenses.append('Даосская защита')
    #
    #         if row['Спецабилка']:
    #             ultra = sample(ultras, k=row['Спецабилка'])
    #
    #         res.append({'Тип юнита': row['Тип юнита'],
    #                     'Хиты': row['Хиты'],
    #                     'Удары': ', '.join(unit_hits),
    #                     'Защита': ', '.join(unit_defenses),
    #                     'Спецабилка': ', '.join(ultra)})
    #     print(res)
    #
    #     with open('data/result.csv', 'w') as res_f:
    #         fieldnames = res[0].keys()
    #         writer = csv.DictWriter(res_f, fieldnames=fieldnames, delimiter="\t")
    #         writer.writeheader()
    #         for item in res:
    #             writer.writerow(item)

main()
