from api.core.answer import rate_candidate_answer
from api.core.question import generate_question
from api.serializer import (GenerateQuestionInputSerializer,
                            GenerateQuestionOutputSerializer,
                            RateCandidateAnswerInputSerializer,
                            RateCandidateAnswerOutputSerializer)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def generate_question_controller(request) -> Response:
    serializer = GenerateQuestionInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    vacancy_id = serializer.validated_data['vacancy_id']

    question = generate_question(vacancy_id)
    question_data = {'text': question}
    question_serializer = GenerateQuestionOutputSerializer(data=question_data)
    if not question_serializer.is_valid():
        return Response(
            question_serializer.errors,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response(question_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def rate_candidate_answer_controller(request) -> Response:
    serializer = RateCandidateAnswerInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    answer_text = serializer.validated_data['answer_text']
    question_id = serializer.validated_data['question_id']

    result = rate_candidate_answer(answer_text, question_id)
    rating_data = {'result': result}
    serializer = RateCandidateAnswerOutputSerializer(data=rating_data)
    if not serializer.is_valid():
        return Response(
            serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response(serializer.data, status=status.HTTP_200_OK)
