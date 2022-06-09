from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get("/")
def start():
    """doc"""

    title = survey.title
    instructions = survey.instructions

    return render_template('survey_start.html',
        title=title, instructions=instructions)

@app.post("/begin")
def begin():
    """redirect to questions, passing in question number"""

    question_number = 0
    return redirect(f"/questions/{question_number}")


@app.get("/questions/<int:question_index>")
def questions(question_index):
    """render question page"""
    question = survey.questions[question_index]

    return render_template("question.html", question=question)