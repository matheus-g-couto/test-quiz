import pytest
from model import Question

def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct
    
def test_create_choice_with_invalid_text():
    question = Question(title='q1')
    
    with pytest.raises(Exception):
        question.add_choice('', False)
    with pytest.raises(Exception):
        question.add_choice('a'*101, False)

def test_create_multiple_choices():
    question = Question(title='q1')
    
    question.add_choice('a', False)
    question.add_choice('b', True)

    assert len(question.choices) == 2
    assert question.choices[0].text == 'a'
    assert not question.choices[0].is_correct
    assert question.choices[1].text == 'b'
    assert question.choices[1].is_correct
    assert question.choices[0].id != question.choices[1].id
    
def test_remove_choice_by_id():
    question = Question(title='q1')
    
    choice1 = question.add_choice('a', False)
    
    assert len(question.choices) == 1

    question.remove_choice_by_id(choice1.id)
    
    assert len(question.choices) == 0
    
def test_remove_choice_by_invalid_id():
    question = Question(title='q1')
    
    choice1 = question.add_choice('a', False)
    
    assert len(question.choices) == 1

    with pytest.raises(Exception):
        question.remove_choice_by_id('invalid_id')
    
    assert len(question.choices) == 1
    
def test_remove_all_choices():
    question = Question(title='q1')
    
    question.add_choice('a', False)
    question.add_choice('b', True)
    
    assert len(question.choices) == 2

    question.remove_all_choices()
    
    assert len(question.choices) == 0
    
def test_set_correct_choices():
    q = Question("q1", max_selections=2)

    c1 = q.add_choice("a")
    c2 = q.add_choice("b")
    c3 = q.add_choice("c")

    q.set_correct_choices([c1.id, c3.id])

    assert c1.is_correct is True
    assert c2.is_correct is False
    assert c3.is_correct is True
    
def test_set_correct_choices_with_invalid_id():
    q = Question("q1")

    c1 = q.add_choice("a")

    with pytest.raises(Exception):
        q.set_correct_choices([c1.id, 'invalid_id'])
        
def test_correct_selected_choices():
    q = Question("q1", max_selections=2)

    c1 = q.add_choice("a", True)
    c2 = q.add_choice("b", False)
    c3 = q.add_choice("c", True)

    corrects = q.correct_selected_choices([c1.id, c2.id])

    assert corrects == [c1.id]
    
def test_correct_selected_choices_with_too_many_selections():
    q = Question("q1", max_selections=2)

    c1 = q.add_choice("a", True)
    c2 = q.add_choice("b", False)
    c3 = q.add_choice("c", True)

    with pytest.raises(Exception):
        q.correct_selected_choices([c1.id, c2.id, c3.id])