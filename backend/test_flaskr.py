import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


BASE = '/api/trivia';
class TriviaTestCase(unittest.TestCase):


    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
        self.DB_USER = os.getenv('DB_USER', 'postgres')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
        self.DB_NAME = os.getenv('DB_NAME', 'trivia')
        self.DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        setup_db(self.app, self.DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_all_categories(self):
            res = self.client().get(BASE+'/categories')
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['categories'])
            self.assertEqual(len(data['categories']), 6)
        
    def test_get_invalid_category(self):
            res = self.client().get(BASE+'/categories/7676')
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Resource not found')

    def test_get_all_questions_paginated(self):
            res = self.client().get(BASE+'/questions')
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['categories'])
            self.assertTrue(data['current_category'])
            self.assertTrue(data['total_questions'])
            self.assertTrue(data['questions'])
            self.assertEqual(len(data['questions']), 10)

    def test_get_questions_paginated(self):
            res = self.client().get(BASE+'/questions?page=1')
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['categories'])
            self.assertTrue(data['current_category'])
            self.assertTrue(data['total_questions'])
            self.assertTrue(data['questions'])
            self.assertEqual(len(data['questions']), 10) 

    def test_delete_question(self):
            res = self.client().delete(BASE+'/questions/9')
            data = json.loads(res.data)
            self.assertEqual(data['success'], True)

    def test_delete_invalid_question(self):
            res = self.client().delete(BASE+'/questions/506')
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unprocessable')

    def test_post_new_question(self):
            res = self.client().post(BASE+'/questions', json={
                'question': 'Name the largest planet of our Solar System?',
                'answer': 'Jupiter',
                'category': 1,
                'difficulty': 4
            })
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertIsNotNone(data['question'])

    def test_post_empty_question(self):
            self.question_empty = {
                'question': '',
                'answer': '',
                'category': 2,
                'difficulty': 2
            }
            res = self.client().post(BASE+'/questions', json=self.question_empty)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unprocessable')    

    def test_search_questions(self):
            data_json = {
                'searchTerm': 'Name the largest planet of our Solar System?'
            }
            res = self.client().post(BASE+'/questions/search', json=data_json)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertIsNotNone(data['questions'])
       
    def test_search_empty_questions(self):
            # 404
            res = self.client().post(BASE+'/questions/search', json={'searchTerm': ''})
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 404)
        
    def test_search_invalid_data_questions(self):
            # 422
            res = self.client().post(BASE+'/questions/search',
                                    json={'searchTerm': 'test121212'})
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 422)

    def test_find_questions_by_category_id(self):
            res = self.client().get(BASE+'/categories/{}/questions'.format(2))
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['category_id'], 2)
            self.assertTrue(data['category_id'])
            self.assertTrue(data['total'])
            self.assertTrue(data['questions'])

    def test_get_questions_by_invalid_category_id(self):
            res = self.client().get('/categories/{}/questions'.format(10))
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)

    def test_all_quizzes_by_category(self):
            data_json = {
                'previous_questions': [3, 4, 10, 12, 11, 5],
                'quiz_category': {'type': 'Art', 'id': 2}
            }
            res = self.client().post(BASE+'/quizzes', json=data_json)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertIsNotNone(data['question'])
            self.assertNotEqual(data['question']['id'], 3)
            self.assertNotEqual(data['question']['id'], 12)
        
    def test_quizzes_by_invalid_category(self):
            data_json = {
                'previous_questions': [3, 4, 10, 12, 11, 5],
                'quiz_category': None
            }
            res = self.client().post(BASE+'/quizzes', json=data_json)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()