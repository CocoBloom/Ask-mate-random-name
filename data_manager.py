import csv


def get_list_of_questions(filename):
    with open(filename, "r", encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader]


def find_index(list_of_questions,mode):
    index = (list_of_questions[0]).index(mode)
    if 0 <= index < 4:
        numbers=[[int(num)for num in row[0:4]] for row in list_of_questions[1:]]
        max_number = max(numbers, key=lambda x: x[index])
        if int(list_of_questions[1][index]) == max_number[index]:
            return False
        else:
            return True
    else:
        max_item= max(list_of_questions[1:], key= lambda x:x[index])
        if list_of_questions[1][index] == max_item[index]:
            return False
        else:
            return True


def get_an_order(list_of_questions, mode, bool):
    ordered_list = ([list_of_questions[0]] + sorted(list_of_questions[1:],
                                                    key=lambda x: x[(list_of_questions[0].index(mode))], reverse=bool))
    return ordered_list

def write_csv(filename, new_data):
    with open(filename, "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in new_data:
            writer.writerow(row)
        return "true"
