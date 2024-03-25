import logging

from api.models import Answer, Question, Result
from openai import OpenAI

from question_generator.settings import openai_api_key

client = OpenAI(api_key=openai_api_key)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s'
)


def rate_candidate_answer(answer_text: str, question_id: int) -> str:
    """
    Оценивает ответ кандидата на вопрос по 10-балльной шкале.
    Возвращает оценку ответа.
    """
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return 'Question not found'

    save_candidate_answer(answer_text, question_id)

    message_system_content = "You are a helpful hr assistant."
    message_user_content = (
        f"Оцени ответ кандидата: {answer_text} на вопрос: {question.text}"
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
            save_answer_rating(chat_response, answer_text)
            return chat_response

    return 'No valid response found'


def save_candidate_answer(answer_text: str, question_id: int) -> None:
    """
    Сохраняет ответ кандидата в базе данных.
    """
    try:
        candidate_answer = Answer(answer=answer_text, question_id=question_id)
        candidate_answer.save()
    except Exception as e:
        logging.error(f'Error saving answer: {str(e)}')


def save_answer_rating(result: str, answer_text: str) -> None:
    """
    Сохраняет результат оценки ответа кандидата в базе данных.
    """
    try:
        answer = Answer.objects.get(answer=answer_text)
        result_rating = Result(result=result, answer=answer)
        result_rating.save()
    except Answer.DoesNotExist:
        logging.error('Answer does not exist')
    except Exception as e:
        logging.error(f'Error saving answer rating: {str(e)}')
