#!/usr/bin/python3
"""
Initialize db -> manual testing
Usage:
    $ cat setup_mysql_test.sql | sudo mysql;
    $ NERVENEX_TYPE_STORAGE=db NERVENEX_ENV=test ./check_models.py
"""
from models import storage
from models.answer import Answer
from models.attempt import Attempt
from models.category import Category
from models.comment import Comment
from models.post import Post
from models.question import Question
from models.quiz import Quiz
from models.thread import Thread
from models.user import User


# Category
cat1 = Category()
cat1.name = "Anatomy"
cat1.save()


# User
u1 = User()
u1.first_name = "John"
u1.last_name = "Doe"
u1.password = "john_doe_pwd"
u1.email = "johndoe@gmail.com"
u1.save()


# Quiz
quiz1 = Quiz()
quiz1.user_id = u1.id
quiz1.category_id = cat1.id
quiz1.title = "ANA 205"
quiz1.description = "Wonderful quiz"
quiz1.duration = 5
quiz1.is_active = True
quiz1.save()


# Question
quest1 = Question()
quest1.quiz_id = quiz1.id
quest1.content = "What is what?"
quest1.option_a = "opt 1"
quest1.option_b = "opt 2"
quest1.option_c = "opt 3"
quest1.option_d = "opt 4"
quest1.correct_answer = 4
quest1.explanation = "Lorem ipsum"
quest1.save()


# Attempt
at1 = Attempt()
at1.user_id = u1.id
at1.quiz_id = quiz1.id
at1.score = len(quiz1.questions)
at1.duration = quiz1.duration
at1.save()


# Answers
an1 = Answer()
an1.attempt_id = at1.id
an1.question_id = quest1.id
an1.value = 2
an1.save()


# Thread
t1 = Thread()
t1.category_id = cat1.id
t1.author_id = u1.id
t1.title = "General"
t1.save()


# Post
p1 = Post()
p1.author_id = u1.id
p1.thread_id = t1.id
p1.content = "Lorem ipsum content of post"
p1.save()


# Comment
com1 = Comment()
com1.author_id = u1.id
com1.post_id = p1.id
com1.content = "Lorem ipsum comment"
com1.save()


# Display
print("Displaying objects")
for obj in storage.all().values():
    print("\n\n{}".format(obj))

storage.close()
