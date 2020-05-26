import csv


def get_list_of_questions(filename):
    with open(filename, "r", encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader]


def get_direction(counter):
    print(counter)
    if counter % 2 == 0:
        return True
    else:
        return False


def get_an_order(list_of_questions, mode, bool):
    ordered_list = ([list_of_questions[0]] + sorted(list_of_questions[1:],
                                                    key=lambda x: x[(list_of_questions[0].index(mode))], reverse=bool))
    return ordered_list


print(get_an_order(get_list_of_questions("sample_data/question.csv"), 'id', False))


def write_csv(filename, new_data):
    with open(filename, "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in new_data:
            writer.writerow(row)
        return "true"
