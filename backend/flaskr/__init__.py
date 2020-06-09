import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import requests
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
   # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def root():
        return jsonify({'message': 'works'})

    @app.route('/categories', methods=['GET'])
    def categoriesList():
        categories = Category.query.all()
        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories}
        })

    @app.route('/questions/<int:page>', methods=['GET'])
    def questionsList(page):
        questionsList = Question.query.order_by(Question.id).all()
        start = (page-1)*10
        end = start+10
        pageList = []
        for question in questionsList[start:end]:
            pageList.append(question)
        formated_questionList = [question.format() for question in pageList]
        totalQuestions = len(questionsList)
        res = requests.get("http://127.0.0.1:5000/categories")
        json_res = res.json()
        categoriesList = json_res['categories']
        return jsonify({
            'success': True,
            'questions': formated_questionList,
            'totalQuestions': totalQuestions,
            'categories': categoriesList,
            'currentCategory': None
        })

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def deleteQuestion(id):

        question = Question.query.filter_by(id=id).first()
        if question is None:
            abort(404)

        question.delete()

        return jsonify({
            'success': True
        })

    @app.route('/questions/addQuestions', methods=['POST'])
    def addQuestion():
        question = request.form.get('question')
        answer = request.form.get('answer')
        difficulty = request.form.get('difficulty')
        category = request.form.get('cartegory')
        question = Question(question, answer, difficulty, category)
        question.insert()
        return jsonify({
            'success': True
        })

    @app.route('/questions', methods=['POST'])
    def searchForQeustion():
        reqJson = request.json
        searchTerm = reqJson['searchTerm']
        searched_questions = Question.query.filter(
            Question.question.ilike(f'%{searchTerm}%')).all()

        formatted_questions = [question.format()
                               for question in searched_questions]
        totalQuestions = len(formatted_questions)

        if formatted_questions is None:
            abort(404)

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'totalQuestions': totalQuestions,
            'currentCategory': None


        })
  '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.

  '''
    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.
  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.






//Done!

  '''

    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''

    return app
