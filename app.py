from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get("/")
def start():
    """Load home page with survey title and instructions"""

    session["responses"] = []

    return render_template(
        'survey_start.html',
        title=survey.title,
        instructions=survey.instructions,
    )


@app.post("/begin")
def begin():
    """Redirect to question page, passing in starting question number"""

    responses = session["responses"]
    question_number = len(responses)
    return redirect(f"/questions/{question_number}")


@app.get("/questions/<int:question_index>")
def questions(question_index):
    """Show question page with form containing question and possible answers.
        Passes along current question index"""

    responses = session["responses"]
    if (question_index != len(responses)):
        question_index = len(responses)
        flash("""You are trying to access an invalid question, 
            please answer questions in order.""")
        return redirect(f'/questions/{question_index}')
      
    return render_template(
        "question.html",
        question=survey.questions[question_index],
        question_index=question_index,
    )


@app.post("/answer")
def save_answer():
    """Reads answer from form and stores answer in responses. Redirects to
        next question or completion form if no more questions available"""

    responses = session["responses"]
    responses.append(request.form["answer"])
    session["responses"] = responses

    # Move to next question
    question_index = int(request.form["question_index"]) + 1

    if (question_index >= len(survey.questions)):
        return redirect("/completed_survey")
    else:
        return redirect(f"/questions/{question_index}")


@app.get("/completed_survey")
def completed():
    """Show completion page once all questions have been answered"""

    return render_template("completion.html")
