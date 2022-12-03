from django.urls import path
from .views import user_login, user_registration, quiz,\
    module, tests, result, index, logout_view

urlpatterns = [
    path("", index, name='index'),
    path('logout/', logout_view, name='logout'),
    path("quiz/", quiz, name='quiz'),
    path('login/', user_login, name='login'),
    path("register/", user_registration, name="register"),
    path(r"quiz/<module>/", module, name="tests_of_module"),
    path(r"quiz/<module>/<test>", tests, name='questions'),
    path('quiz/result', result, name='result')
]
