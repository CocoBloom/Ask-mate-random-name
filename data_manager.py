import csv

def get_list_of_questions(filename):
    with open(filename, "r", encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader]


print(len(get_list_of_questions("question.csv")))
listed = get_list_of_questions("question.csv")
revered_list=listed[::-1]
print(listed)
print(revered_list)


def write_csv(filename, new_data):
    with open(filename, "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in new_data:
            writer.writerow(row)
        return "true"