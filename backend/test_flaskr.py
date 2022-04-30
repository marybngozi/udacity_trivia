import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.delete_id = 24  # to be updated
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'maryb', '', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            # set up a question to be deleted to avoid delete failure
            delete_quest = Question(
                question='question', answer='answer', difficulty=2, category=1)
            delete_quest.insert()
            self.delete_id = delete_quest.id

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    # success: get all categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['categories']['1'])

    # success: get questions in pages
    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])
        self.assertIn('categories', data)
        self.assertTrue(data['categories']['1'])
        self.assertIn('currentCategory', data)
        self.assertTrue(data['currentCategory'])

    # error: get questions in page out of range
    def test_404_get_questions_out_of_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertNotIn('questions', data)
        self.assertEqual(data['message'], 'resource not found')

    # success: post new question
    def test_post_new_question(self):
        res = self.client().post('/questions', json={"question": "Here is a newer question string",
                                                     "answer":  "Heres a new answer string", "difficulty": 1, "category": 3})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('question', data)
        self.assertIn('id', data['question'])
        self.delete_id = data['question']['id']

    # error: post new question with empty or invalid parameter
    def test_400_post_new_question_empty_or_invalid_parameter(self):
        res = self.client().post('/questions', json={
            'question':  'Heres a new question string',
            'category': 3,
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    # success: delete a question
    def test_delete_question(self):
        res = self.client().delete('/questions/'+str(self.delete_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('deleted', data)
        self.assertEqual(data['deleted'], self.delete_id)

    # error: delete a question without and ID goes to a wrong invalid route
    def test_405_delete_question_no_id(self):
        res = self.client().delete('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'method not allowed')

    # error: delete a question with an id that does not exists
    def test_404_delete_question(self):
        res = self.client().delete('/questions/2244')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    # success: search for questions by keyword in the search term
    def test_post_search_questions(self):
        res = self.client().post('/questions', json={"searchTerm": "question"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('questions', data)
        self.assertIn('totalQuestions', data)
        self.assertTrue(data['totalQuestions'])
        self.assertIn('currentCategory', data)

    # error: search for questions for search term that does not exist
    def test_search_questions_no_question(self):
        res = self.client().post(
            '/questions', json={"searchTerm": "qweasdrfxccjcidiffj"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('questions', data)
        self.assertIn('totalQuestions', data)
        self.assertFalse(data['totalQuestions'])

    # success: get questions by category
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])
        self.assertIn('categories', data)
        self.assertTrue(data['categories']['1'])
        self.assertIn('currentCategory', data)
        self.assertTrue(data['currentCategory'])

    # error: get questions by a category that does not exist
    def test_404_questions_by_category_not_exists(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    # success: get a random question for quiz
    def test_post_quizzes(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [5, 9, 12, 23],
            'quiz_category': 4
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('question', data)
        self.assertIn('id', data['question'])

    # error: get no question when all category questions are in the previous
    def test_post_quizzes_no_more_question_found(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [16, 17, 18, 19],
            'quiz_category': 2
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['question'])

    # error: get no question when the max number of questions (5) have been reached
    def test_post_quizzes_max_reached(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [22, 17, 9, 5, 1],
            'quiz_category': None
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
