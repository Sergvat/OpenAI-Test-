from openai import OpenAI
import logging

from question_generator.settings import openai_api_key
from api.models import Vacancy, Question

client = OpenAI(api_key=openai_api_key)

logging.basicConfig(level=logging.INFO, format='%(asctime)s, %(levelname)s, %(name)s, %(message)s')

def generate_question(vacancy_id: int) -> str:
    """
    Генерирует вопрос для кандидата на основе информации о вакансии.
    """
    try:
        vacancy = Vacancy.objects.get(id=vacancy_id)
    except Vacancy.DoesNotExist:
        return 'Vacancy not found'

    message_system_content = "You are a helpful hr assistant."
    message_user_content = (f"Сгенирируй вопрос кандидату от HR-специалиста для вакансии"
                            f"{vacancy.name} с описанием {vacancy.description}")

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
            save_generated_question(chat_response, vacancy_id)
            return chat_response

    return 'No valid response found'


def save_generated_question(question: str, vacancy_id: int) -> None:
    """
    Сохраняет сгенерированный вопрос в базе данных.
    """
    try:
        generated_question = Question(text=question, vacancy=vacancy_id)
        generated_question.save()
    except Exception as e:
        logging.error(f'Error saving generated question: {str(e)}')