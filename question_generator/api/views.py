from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from question_generator.api.core.question import generate_question
from question_generator.api.core.answer import rate_candidate_answer, save_answer_rating
from .serializers import (
    GenerateQuestionInputSerializer, GenerateQuestionOutputSerializer,
    RateCandidateAnswerInputSerializer, RateCandidateAnswerOutputSerializer
)


@api_view(['POST'])
def generate_question_controller(request) -> Response:
    # из тела запроса получить ваканси_айди с помощью сереализатора(GenerateQuestionInputSerializer)
    # вызвать свою функцию с полученной ваканси_айди
    # сгенерированный вопрос для кандидата от гпт вернуть в виде джейсон ответ
    # применить сериализатор(который будет ответ GenerateQuestionOutputSerializer)
    serializer = GenerateQuestionInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    vacancy_id = serializer.validated_data['vacancy_id']

    question = generate_question(vacancy_id)
    question_serializer = GenerateQuestionOutputSerializer(data={'text': question})
    if not question_serializer.is_valid():
        return Response(question_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(question_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def rate_candidate_answer_controller(request) -> Response:
    # получить ответ кандидата с помощью сериалайзер
    # сохранить ответ кандидата в базе
    # отправить ответ на оценку в опенай
    # ответ джсон с полем рейт, например строка 6/10 с помощью сериалайзера
    serializer = RateCandidateAnswerInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    answer_id = serializer.validated_data['answer_id']
    question_id = serializer.validated_data['question_id']

    result = rate_candidate_answer(answer_id, question_id)
    save_answer_rating(result, answer_id)

    rating_data = {'rating': result}
    serializer = RateCandidateAnswerOutputSerializer(data=rating_data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.data, status=status.HTTP_200_OK)
