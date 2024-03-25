import logging

from api.models import Answer, Question, Result
from openai import OpenAI

from question_generator.settings import openai_api_key

client = OpenAI(api_key=openai_api_key)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s'
)


def rate_candidate_answer(answer_id: int, question_id: int) -> str:
    """
    Оценивает ответ кандидата на вопрос по 10-балльной шкале.
    Возвращает оценку ответа.
    """
    try:
        answer = Answer.objects.get(id=answer_id)
    except Answer.DoesNotExist:
        return 'Answer not found'

    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return 'Question not found'

    message_system_content = "You are a helpful hr assistant."
    message_user_content = (
        f"Оцени ответ кандидата: {answer.answer} на вопрос: {question.text}"
        f"от HR-специалиста по 10-балльной шкале"
        f"в формате оценка/10 (например 6/10),"
        f"дай краткий ответ."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": message_system_content},
                {"role": "user", "content": message_user_content},
            ]
        )
    except Exception as e:
        return f'Error generating question: {str(e)}'

    if not response.choices:
        return 'No response choices available'

    for choice in response.choices:
        if choice.message is not None:
            chat_response = choice.message.content
            save_answer_rating(chat_response, answer_id)
            return chat_response

    return 'No valid response found'


# def save_candidate_answer(answer: str, question_id: int) -> None:
#     """
#     Сохраняет ответ кандидата в базе данных.
#     """
#     try:
#         candidate_answer = Answer(answer=answer, question_id=question_id)
#         candidate_answer.save()
#     except Exception as e:
#         logging.error(f'Error saving answer: {str(e)}')


def save_answer_rating(result: str, answer_id: int) -> None:
    """
    Сохраняет результат оценки ответа кандидата в базе данных.
    """
    try:
        answer = Answer.objects.get(id=answer_id)
        result_rating = Result(result=result, answer=answer)
        result_rating.save()
    except Answer.DoesNotExist:
        logging.error(f'Vacancy with id {answer_id} does not exist')
    except Exception as e:
        logging.error(f'Error saving answer rating: {str(e)}')
