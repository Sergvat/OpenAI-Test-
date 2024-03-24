from django.db import models


class Vacancy(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)


class Answer(models.Model):
    answer = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Result(models.Model):
    result = models.CharField(max_length=100)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
