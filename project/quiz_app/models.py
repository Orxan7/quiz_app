from django.contrib.auth.models import User
from django.db import models


class TestModule(models.Model):
    name = models.TextField(max_length=25)
    description = models.TextField(max_length=500)


class Test(models.Model):
    name = models.TextField(max_length=25)
    test_module = models.ForeignKey(
        TestModule,
        on_delete=models.CASCADE,
    )


class Question(models.Model):
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
    )

    question = models.CharField(max_length=200, null=True)
    var1 = models.CharField(max_length=200, null=True)
    var2 = models.CharField(max_length=200, null=True)
    var3 = models.CharField(max_length=200, null=True)
    var4 = models.CharField(max_length=200, null=True)
    answer = models.CharField(max_length=200, null=True)


class UserHelper(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    i = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
