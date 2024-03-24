from rest_framework import serializers

from .models import Vacancy, Question, Result


class GenerateQuestionInputSerializer(serializers.Serializer):
    vacancy_id = serializers.IntegerField()

# class GenerateQuestionInputSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Vacancy
#         fields = ('vacancy_id',)


class GenerateQuestionOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('text',)


class RateCandidateAnswerInputSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('answer_id', 'question_id')


class RateCandidateAnswerOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = ('result',)
