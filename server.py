from flask import Flask, request, render_template,redirect
import data_manager
import util
import time


app = Flask(__name__)


@app.route("/")
@app.route('/list', methods=['GET','POST'])
def display_list():
    list_of_questions = data_manager.get_list_of_questions("sample_data/question.csv")
    if request.method == "POST":
        counters={}
        for head in list_of_questions[0]:
            try:
                mode = request.form[head]
                counter =1
                direction = data_manager.get_direction(counter)
                ordered_list = data_manager.get_an_order(list_of_questions=list_of_questions, mode = mode, bool=direction)
                data_manager.write_csv("sample_data/question.csv", new_data=ordered_list)
            except:
                continue

        return redirect('/')
    else:
        return render_template("list.html", list_of_questions=list_of_questions)



@app.route("/question/<int:question_id>")
def question_page(question_id):
    list_of_questions = data_manager.get_list_of_questions('sample_data/question.csv')
    list_of_answers = data_manager.get_list_of_questions('sample_data/answer.csv')

    title = list_of_questions[question_id][4]
    question = list_of_questions[question_id][5]
    str_id = str(question_id)

    question_answers = [[answer[4],answer[5]] for answer in list_of_answers if answer[3] == str_id]

    return render_template("question.html", question_id= question_id, title=title,
                           question=question, question_answers=question_answers)



@app.route('/add-question', methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        list_of_questions = data_manager.get_list_of_questions("sample_data/question.csv")
        # id-t, submission timeot honnan kap?
        new_question = [create_new_id(list_of_questions), int(time.time()), 0, 0, request.form['questiontitle'], request.form['questionbody'], '']
        list_of_questions.append(new_question)
        data_manager.write_csv("questions.csv", list_of_questions)
        return redirect('/list')
    else:
        return render_template("ask_questions.html")


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    if request.method == 'POST':
        list_of_questions = data_manager.get_list_of_questions("sample_data/question.csv")
        for id in list_of_questions:
            if question_id == id[0]:
                list_of_questions.remove(id)
        data_manager.write_csv("sample_data/question.csv", list_of_questions)
    return redirect('/list')


@app.route("/question/<int:question_id>/new-answer", methods=['GET', 'POST'])
def answer_page(question_id):
    if request.method == 'POST':
        list_of_questions = data_manager.get_list_of_questions('sample_data/question.csv')
        list_of_questions.append([util.create_new_id(list_of_questions), int(time.time()), 0, 0,request.form['answer'], request.form['img']])
        data_manager.write_csv("sample_data/question.csv", list_of_questions)
        return redirect('/question/'+str(question_id))
    return render_template("new_answer.html", question_id=question_id)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
