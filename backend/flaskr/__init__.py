import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
BASE = '/api/trivia';

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for origins.
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
      return response


    # Create an endpoint to handle GET requests for all available categories
    @app.route(BASE+'/categories')
    def get_categories():
      categories = [category.format() for category in Category.query.all()]
      
      if len(categories) == 0:
        abort(404)
      else:
        return jsonify({
          "categories": categories,
          "success": True
        })




    # Create an endpoint to handle GET requests for questions, 
    # including pagination (every 10 questions). 
    # This endpoint should return a list of questions, 
    # number of total questions, current category, categories. 

    """
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route(BASE+'/questions')
    def get_questions():
      try:
        questions = Question.query.order_by(Question.id).all()
        total_questions = len(questions)
        categories = [category.format() for category in Category.query.all()]
        

        # pagination
        page = request.args.get('page', 1, type=int)
        start =  (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions  = [question.format() for question in questions]
        questions  = questions [start:end]
        current_category = questions[0]['category']

        return jsonify({
            'questions': questions,
            'total': total_questions,
            'currentcategory': current_category,
            'categories': categories,
            'success': True,
        })

      except Exception:
        if len(questions) == 0:
              abort(404)
        else:
          abort(422)
   

    """
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    # Create an endpoint to DELETE question using a question ID
    @app.route(BASE+'/questions/<int:id>', methods=['DELETE'])
    def remove_question(id):
          try:
            question = Question.query.filter(Question.id == id).one_or_none()
            if question is None:
              abort(404)
            else:
              question.delete()
              return jsonify({
                'question_id': id,
                'success': True
                })
          except Exception:
            abort(422)


    """
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    # Create an endpoint to POST a new question, 
    # which will require the question and answer text, 
    # category, and difficulty score.

    @app.route(BASE+'/questions', methods=['POST'])
    def post_question():
      try:
            data = request.json

            category = int(data['category'])
            difficulty = int(data['difficulty'])
            question = data['question']
            answer = data['answer']

            if (question == '' or answer == ''):
              abort(422)

            Question(question=question, answer=answer,difficulty=difficulty,category=category).insert()
            return jsonify({
              'question': question,
              'answer': answer,
              'difficulty': difficulty,
              'category': category,
              'success': True     
            })

      except Exception:
            abort(422)


    """
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    # Create a POST endpoint to get questions based on a search term. 
    # It should return any questions for whom the search term 
    # is a substring of the question. 
    @app.route(BASE+'/questions/search', methods=['POST'])
    def search():
        data = request.json
        key = data['searchTerm']
        if (key == ''):
          abort(404)
        else:
          data = Question.query.filter(Question.question.ilike('%{}%'.format(key))).all()


          try:
            questions = [i.format() for i in data]
            total = len(questions)
            category = questions[0]['category']
            return jsonify({
                'questions': questions,
                'total': total,
                'currentcategory': category,
                'success': True
                })
          except Exception:
            abort(422)


   

    """
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    # Create a GET endpoint to get questions based on category
    @app.route(BASE+'/categories/<int:category>/questions')
    def get_questions_by_category_id(category):
      data = Question.query.filter(Question.category == category).all()
      if (data == None):
        abort(404)

      questions = [i.format() for i in data]
      total = len(questions)

      if total == 0:
        abort(404)

      else:
        return jsonify({
          'questions': questions,
          'total': total,
          'category_id': category,
          'success': True
          })



    """
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    # Create a POST endpoint to get questions to play the quiz. 
   # This endpoint should take category and previous question parameters 
   # and return a random questions within the given category, 
   # if provided, and that is not one of the previous questions

    @app.route(BASE+'/quizzes', methods=['POST'])
    def play_quizzes():
        try:
            searched_data = request.get_json()
            questions = Question.query.filter_by(category=searched_data['quiz_category']['id']).filter(
                            Question.id.notin_(searched_data['previous_questions'])).all()
            question_length = len(questions)
            random_quiz = Question.format(questions[random.randrange(0, question_length)])

            if question_length > 0:
                return jsonify({
                    'success': True,
                    'question': random_quiz
                })
            else:
              abort(404)
        except:
            abort(422)


    # Create error handler for expected error 404
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
              'error': 404,
              'message': 'Resource not found',
              'success': False }),
            404,
        )

    # Create error handler for expected error 422
    @app.errorhandler(422)
    def unprocessable(error):
      return (
            jsonify({
              'error': 422,
              'message': 'Unprocessable',
              'success': False }),
            422,
        )

    # Create error handler for expected error 500
    @app.errorhandler(500)
    def server_error(error):
      return (
            jsonify({
              'error': 500,
              'message': 'Internal server error',
              'success': False }),
            500,
        )

    return app
