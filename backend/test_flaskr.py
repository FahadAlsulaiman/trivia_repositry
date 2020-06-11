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
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "Q2",
            "answer": "A2",
            "difficulty": 2,
            "category": 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_Categories_List(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertTrue(data['categories'])

    def test_Categories_List_404_error(self):
        res = self.client().get('/categories/list')
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 404)
        self.assertEquals(data['success'], False)
        self.assertTrue(data['message'], 'not found')

    def test_Questions_List(self):
        res = self.client().get('/questions/1')
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertGreaterEqual(data['totalQuestions'], 0)
        self.assertTrue(data['categories'])
        self.assertEquals(data['currentCategory'], None)

    def test_Questions_List_404_error(self):
        res = self.client().get('/questions/test')
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 404)
        self.assertEquals(data['success'], False)
        self.assertTrue(data['message'], 'not found')

    def test_Delete_question(self):
        res = self.client().delete('/questions/22/deleteQuestion')
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertEquals(data['success'], True)

    def test_Delete_question_422_error(self):
        res = self.client().delete('/questions/17/deleteQuestion')
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 422)
        self.assertEquals(data['success'], False)
        self.assertTrue(data['message'], 'not found')

    def test_Add_question(self):
        res = self.client().post('/questions/addQuestion', json=self.new_question)
        data = json.loads(res.data)
        self.assertEquals(res.status_code, 200)
        self.assertEquals(data['success'], True)

    def test_Add_question_404_error(self):
        res = self.client().post('/questions/addQuestion/45', json=self.new_question)
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 404)
        self.assertEquals(data['success'], False)
        self.assertTrue(data['message'], 'not found')

    def test_Category_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertEquals(data['currentCategory'], 1)

    def test_Category_questions_422_error(self):
        res = self.client().get('/categories/Test/questions')
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 404)
        self.assertEquals(data['success'], False)
        self.assertTrue(data['message'], 'not found')

    def test_Search_For_Question(self):
        res = self.client().post('/questions', json={'searchTerm': 'W'})
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertGreaterEqual(data['totalQuestions'], 0)
        self.assertEquals(data['currentCategory'], None)

    def test_Search_For_Question_422_error(self):
        res = self.client().post('/questions', json={'search_Term': 'W'})
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 422)
        self.assertEquals(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

    def test_quiz(self):
        res = self.client().post(
            '/quizzes', json={"previous_questions": [], "quiz_category": {"type": "Science", "id": "1"}})
        data = json.loads(res.data)

        self.assertEquals(data['success'], True)
        self.assertTrue(data['question'])

    """
    TOD
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
