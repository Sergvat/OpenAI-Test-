from rest_framework import serializers

from .models import Question, Result


class GenerateQuestionInputSerializer(serializers.Serializer):
    vacancy_id = serializers.IntegerField()


class GenerateQuestionOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('text',)


class RateCandidateAnswerInputSerializer(serializers.Serializer):
    answer_text = serializers.CharField()
    question_id = serializers.IntegerField()


class RateCandidateAnswerOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = ('result',)
