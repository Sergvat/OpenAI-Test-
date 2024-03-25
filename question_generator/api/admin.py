from django.contrib import admin

from .models import Answer, Question, Result, Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'vacancy')
    readonly_fields = ('text', 'vacancy')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'question')
    search_fields = ('answer', 'question')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('result', 'answer')
    readonly_fields = ('result', 'answer')
