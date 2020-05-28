import csv


def get_list_of_questions(filename):
    with open(filename, "r", encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader]


def get_display_list(list_of_questions):
    use_to_display=[]
    for i in range(len(list_of_questions)):
        if i !=0:
            for j in range(len(list_of_questions[i])):
                if 0 <= j <4:
                    list_of_questions[i][j] = int(list_of_questions[i][j])
            use_to_display.append(list_of_questions[i])
    return use_to_display



# used_list=(get_display_list(get_list_of_questions("próba.csv")))
# print("get_display",used_list)

def get_an_order(used_list,list_of_questions,mode,direction):
    print(mode)
    print(direction)
    if mode is None:
        mode='id'
        direction='True'
    print(mode)
    print(direction)
    index = (list_of_questions[0]).index(mode)
    if direction == "True":
        ordered_list = ([list_of_questions[0]] + sorted(used_list, key=lambda x: x[index], reverse=True))
        print("trueorder",ordered_list)
    else:
        ordered_list = ([list_of_questions[0]] + sorted(used_list, key=lambda x: x[index], reverse=False))
        print("falseorder",ordered_list)
    return ordered_list


def write_csv(filename, new_data):
    with open(filename, "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in new_data:
            writer.writerow(row)
        return "true"
