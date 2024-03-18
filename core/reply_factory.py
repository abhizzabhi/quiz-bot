
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    if current_question_id is None:
        return False, "No current question to answer."
    session["question_{}_answer".format(current_question_id)] = answer
    session.save()
    Validates and stores the answer for the current question to django session.

    return True, ""


def get_next_question(current_question_id):
    if current_question_id is None:
        return None, None
    next_question_id = current_question_id + 1
    if next_question_id < len(PYTHON_QUESTION_LIST):
        return PYTHON_QUESTION_LIST[next_question_id], next_question_id
    else:
        return None, None
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    

    return "dummy question", -1


def generate_final_response(session):
    score = 0
    for question_id, question in enumerate(PYTHON_QUESTION_LIST):
        answer_key = "question_{}_answer".format(question_id)
        if answer_key in session:
            score += 1  # Dummy logic, increment score for each answered question

    final_response = "Congratulations! You have completed the Python quiz. Your score is {} out of {}.".format(score, len(PYTHON_QUESTION_LIST))
    return final_response
    return "dummy result"
