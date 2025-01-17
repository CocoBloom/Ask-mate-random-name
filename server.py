from flask import Flask, request, render_template,redirect
import data_manager
import util
import time
import os


app = Flask(__name__)


@app.route("/")
@app.route('/list', methods = ['GET','POST'])
def display_list():
    list_of_questions = data_manager.get_list_of_questions("sample_data/question.csv")
    mode = request.args.get('order_by')
    direction = request.args.get('order_direction')
    use_to_display = data_manager.get_display_list(list_of_questions)
    ordered_list=data_manager.get_an_order(use_to_display,list_of_questions,mode=mode,direction=direction)
    data_manager.write_csv("sample_data/question.csv",ordered_list)
    return render_template("list.html", list_of_questions=ordered_list)



@app.route("/question/<int:question_id>")
def question_page(question_id):
    list_of_questions = data_manager.get_list_of_questions('sample_data/question.csv')
    list_of_answers = data_manager.get_list_of_questions('sample_data/answer.csv')

    for question in list_of_questions:
        if str(question_id) == question[0]:
            question[2] = str(int(question[2]) + 1)

    correct_row = [i for i in range(len(list_of_questions)) if list_of_questions[i][0] == str(question_id)][0]
    title = list_of_questions[correct_row][4]
    question = list_of_questions[correct_row][5]
    image = list_of_questions[correct_row][6]
    str_id = str(question_id)
    question_answers = [answer for answer in list_of_answers if answer[3] == str_id]
    data_manager.write_csv("sample_data/question.csv", list_of_questions)
    return render_template("question.html", question_id= question_id, title=title,
                           question=question, question_answers=question_answers, image=image)


@app.route('/add-question', methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        list_of_questions = data_manager.get_list_of_questions("sample_data/question.csv")
        file = request.files['questionimage']
        filename = file.filename
        if filename == '':
            pass
        else:
            filename = os.path.join('static/', filename)
            file.save(filename)
        new_question = [len(list_of_questions), int(time.time()), 0, 0, request.form['questiontitle'], request.form['questionbody'], filename]
        list_of_questions.append(new_question)
        data_manager.write_csv("sample_data/question.csv", list_of_questions)
        return redirect('/list')
    else:
        return render_template("ask_questions.html")


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    if request.method == 'POST':
        list_of_questions = data_manager.get_list_of_questions("sample_data/question.csv")
        list_of_answer = data_manager.get_list_of_questions("sample_data/answer.csv")
        for id in list_of_questions:
            if question_id == id[0]:
                list_of_questions.remove(id)
                data_manager.write_csv("sample_data/question.csv", list_of_questions)
        for answer in list_of_answer:
             if question_id == answer[3]:
                 list_of_answer.remove(answer)
                 data_manager.write_csv("sample_data/answer.csv", list_of_answer)
    return redirect('/list')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    list_of_questions = data_manager.get_list_of_questions("sample_data/question.csv")
    if request.method == 'GET':
        for question in list_of_questions:
            if question_id == question[0]:
                question_title = question[4]
                question_text = question[5]
                question_image = question[6]
        return render_template("edit_question_new.html", question_text=question_text, question_title=question_title, question_id=question_id, question_image=question_image)
    else:
        for question in list_of_questions:
            if question[0] == question_id:
                question[4] = request.form['edittitle']
                question[5] = request.form['editbody']
                file = request.files['editimage']
                filename = file.filename
                if filename == '':
                    question[6] = ''
                else:
                    filename = os.path.join('static/', filename)
                    file.save(filename)
                    question[6] = filename
        data_manager.write_csv("sample_data/question.csv", list_of_questions)
        return redirect('/question/'+ question_id)



@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def answer_page(question_id):
    if request.method == 'POST':
        list_of_answers = data_manager.get_list_of_questions('sample_data/answer.csv')
        file = request.files['img']
        filename = file.filename
        if filename == '':
            pass
        else:
            filename = os.path.join('static/', filename)
            file.save(filename)
        list_of_answers.append([len(list_of_answers), int(time.time()), 0, question_id,
                                  request.form['answer'], filename])
        data_manager.write_csv("sample_data/answer.csv", list_of_answers)
        return redirect('/question/'+ question_id)
    return render_template("new_answer.html", question_id=question_id)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    list_of_answers = data_manager.get_list_of_questions("sample_data/answer.csv")
    question_id = [answer[3] for answer in list_of_answers if answer[0] == answer_id][0]
    for answer in list_of_answers:
        if answer_id == answer[0]:
            list_of_answers.remove(answer)
    data_manager.write_csv("sample_data/answer.csv", list_of_answers)
    return redirect('/question/'+ question_id)


@app.route('/question/<question_id>/vote_up')
def vote_up_question(question_id):
    list_of_questions = data_manager.get_list_of_questions("sample_data/question.csv")
    for question in list_of_questions:
        if question_id == question[0]:
            question[3] = str(int(question[3]) + 1)
    data_manager.write_csv("sample_data/question.csv", list_of_questions)
    return redirect('/list')


@app.route('/question/<question_id>/vote_down')
def vote_down_question(question_id):
    list_of_questions = data_manager.get_list_of_questions("sample_data/question.csv")
    for question in list_of_questions:
        if question_id == question[0]:
            question[3] = str(int(question[3]) - 1)
    data_manager.write_csv("sample_data/question.csv", list_of_questions)
    return redirect('/list')


@app.route('/answer/<answer_id>/vote_up')
def vote_up_answer(answer_id):
    list_of_answers = data_manager.get_list_of_questions("sample_data/answer.csv")
    question_id = [answer[3] for answer in list_of_answers if answer[0] == answer_id][0]
    for answer in list_of_answers:
        if answer_id == answer[0]:
            answer[2] = str(int(answer[2]) + 1)
    data_manager.write_csv("sample_data/answer.csv", list_of_answers)
    return redirect('/question/'+ question_id)


@app.route('/answer/<answer_id>/vote_down')
def vote_down_answer(answer_id):
    list_of_answers = data_manager.get_list_of_questions("sample_data/answer.csv")
    question_id = [answer[3] for answer in list_of_answers if answer[0] == answer_id][0]
    for answer in list_of_answers:
        if answer_id == answer[0]:
            answer[2] = str(int(answer[2]) - 1)
    data_manager.write_csv("sample_data/answer.csv", list_of_answers)
    return redirect('/question/'+ question_id)


if __name__ == "__main__":
    app.run(debug=True,
            port=8000,
            host='0.0.0.0')
