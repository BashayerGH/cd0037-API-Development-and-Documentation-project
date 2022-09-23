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


    # GET all available categories
    @app.route(BASE+'/categories')
    def all_categories():
      try:
        all_categories = Category.query.all()
        categories_list = [category.format() for category in all_categories]
        if len(categories_list) == 0:
          abort(404)
        categories_formatted = {}
        for category in categories_list:
          categories_formatted.update({category.get("id"): category.get("type")})
        return jsonify({
          'categories': categories_formatted,
          'success': True
        })
      except Exception:
        abort(500)



    # GET paginated questions list,
    # including number of total questions, current category, categories. 
    @app.route(BASE+'/questions')
    def paginated_questions():
      try:
        all_questions = Question.query.order_by(Question.id).all()
        questions_list = list_paginated(request, all_questions)
        if len(questions_list) == 0:
          abort(404)
        categories_list = [category.format() for category in Category.query.all()]
        categories_formatted = {}
        for category in categories_list:
          categories_formatted.update({category.get("id"): category.get("type")})
            
        return jsonify({
          'questions': questions_list,
          'total_questions': len(all_questions),
          'categories': categories_formatted,
          'current_category': questions_list[0]['category'],
          'success': True
        })
      except Exception:
        abort(500)

    def list_paginated(request, list):
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      questions_list = [question.format() for question in list]
      questions_paginated = questions_list[start:end]
      return questions_paginated


    # DELETE question using its ID
    @app.route(BASE+'/questions/<int:id>', methods=['DELETE'])
    def remove_question(id):
      try:
        deleted_question = Question.query.filter(Question.id == id).one_or_none()
        if deleted_question is None:
          abort(404)
        else:
          deleted_question.delete()
          return jsonify({
            'success': True
          })
      except Exception:
        abort(422)

    # POST a new question, which requires the question and answer text, 
    # category, and difficulty score.
    @app.route(BASE+'/questions', methods=['POST'])
    def post_new_question():
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
          'success': True,
          'question': question,
          'answer': answer,
          'difficulty': difficulty,
          'category': category
        })

      except Exception:
            abort(422)


    # POST endpoint to get questions based on a search term
    @app.route(BASE+'/questions/search', methods=['POST'])
    def search():
        data = request.json
        searchTerm = data['searchTerm']
        if (searchTerm == ''):
          abort(404)
        else:
          data = Question.query.filter(Question.question.ilike('%{}%'.format(searchTerm))).all()
          if (data == None):
            abort(404)

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
   
    # GET endpoint to get questions list by its category id
    @app.route(BASE+'/categories/<int:category>/questions')
    def questions_by_category_id(category):
      filtered_questions = Question.query.filter(Question.category == category).all()
      if (filtered_questions == None):
        abort(404)

      try:
        questions = [i.format() for i in filtered_questions]
        total = len(questions)

        if (total == 0):
          abort(404)

        else:
          return jsonify({
            'questions': questions,
            'total': total,
            'category_id': category,
            'success': True
          })
      except Exception:
        abort(422)


    # POST endpoint to get questions to play the quiz. 
    # it takes category and previous question parameters 
    # and return a random questions within the given category, 
    # if provided, and that is not one of the previous questions
    @app.route(BASE+'/quizzes', methods=['POST'])
    def play_quizzes():
      try:
        searched_data = request.get_json()
        category_id = searched_data['quiz_category']['id']
        previous_questions = searched_data['previous_questions']

        if category_id == 0:
            # questions = Question.query.all()
            questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
        else:
            # questions = Question.query.filter(Question.category == category_id).all()
            questions = Question.query.filter_by(
                    category=category_id).filter(
                        Question.id.notin_(previous_questions)).all()

        question_length = len(questions)

        if question_length == 0:
          random_quiz = None
        else :
        # generate a random quiz
          random_quiz = questions[random.randint(0, question_length - 1)].format()

      # a layer of filteration, to ensure that quiz is not within the previous questiosns
        # while random_quiz.id in previous_questions:
            # random_quiz = questions[random.randint(0, question_length - 1)]

        return jsonify({
            'success': True,
            'question': random_quiz
        })

      except Exception:
        abort(422)

    # Error handler for expected error 404
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
              'error': 404,
              'message': 'Resource not found',
              'success': False }),
            404,
        )

    # Error handler for expected error 422
    @app.errorhandler(422)
    def unprocessable(error):
      return (
            jsonify({
              'error': 422,
              'message': 'Unprocessable',
              'success': False }),
            422,
        )

    # Error handler for expected error 500
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
