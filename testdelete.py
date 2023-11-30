#!/usr/bin/python3
"""Test delete feature for student platform"""
from models.engine.file_storage import FileStorage
from models.user import User
from models.quiz import Quiz
from models.question import Question
from models.answer import Answer
from models.attempt import Attempt


def test_student_platform_delete_feature():
    # Initialize FileStorage instance
    fs = FileStorage()

    # Create a user
    user = User(email="test@example.com", password="testpassword")
    fs.new(user)
    fs.save()

    # Create a quiz
    quiz = Quiz(title="Math Quiz", description="A basic math quiz")
    fs.new(quiz)
    fs.save()

    # Create a question
    question = Question(quiz_id=quiz.id, text="What is 2 + 2?", solution="4")
    fs.new(question)
    fs.save()

    # Create an answer
    answer = Answer(question_id=question.id, text="5", is_correct=False)
    fs.new(answer)
    fs.save()

    # Create an attempt
    attempt = Attempt(user_id=user.id, quiz_id=quiz.id, score=0)
    fs.new(attempt)
    fs.save()

    # Check all existing objects
    all_objs = fs.all()
    print("-- Initial Objects --")
    for obj_id in all_objs.keys():
        print(all_objs[obj_id])

    # Delete the question
    fs.delete(question)

    # Reload all objects from storage
    all_objs = fs.all()
    print("-- Reloaded Objects --")
    for obj_id in all_objs.keys():
        print(all_objs[obj_id])

    # Verify that the deleted question is no longer in storage
    assert question.id not in all_objs
    print("-- Verified Question Deleted --")

    # Delete the quiz
    fs.delete(quiz)

    # Reload all objects from storage
    all_objs = fs.all()
    print("-- Reloaded Objects --")
    for obj_id in all_objs.keys():
        print(all_objs[obj_id])

    # Verify that the deleted quiz is no longer in storage
    assert quiz.id not in all_objs
    print("-- Verified Quiz Deleted --")

    # Delete the user
    fs.delete(user)

    # Reload all objects from storage
    all_objs = fs.all()
    print("-- Reloaded Objects --")
    for obj_id in all_objs.keys():
        print(all_objs[obj_id])

    # Verify that the deleted user is no longer in storage
    assert user.id not in all_objs
    print("-- Verified User Deleted --")


if __name__ == "__main__":
    test_student_platform_delete_feature()
