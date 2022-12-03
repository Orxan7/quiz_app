from django.contrib import admin
from .models import Question, Test, TestModule


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class TestInline(admin.StackedInline):
    model = Test
    extra = 1


class TestModuleAdmin(admin.ModelAdmin):
    inlines = [TestInline]


class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Test, TestAdmin)
admin.site.register(TestModule, TestModuleAdmin)
