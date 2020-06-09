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
        try:
            categories = Category.query.all()
            return jsonify({
                'success': True,
                'categories': {category.id: category.type for category in categories}
            })
        except:
            abort(404)

    @app.route('/questions/<int:page>', methods=['GET'])
    def questionsList(page):
        try:
            questionsList = Question.query.order_by(Question.id).all()
            start = (page-1)*10
            end = start+10
            pageList = []
            for question in questionsList[start:end]:
                pageList.append(question)
            formated_questionList = [question.format()
                                     for question in pageList]
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
        except:
            abort(422)

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def deleteQuestion(id):
        try:
            question = Question.query.filter_by(id=id).first()
            question.delete()
            return jsonify({
                'success': True
            })
        except:
            abort(404)

    @app.route('/questions/addQuestion', methods=['POST'])
    def addQuestion():
        try:
            req = request.get_json()
            question = req.get('question', None)
            answer = req.get('answer', None)
            difficulty = req.get('difficulty', None)
            category = req.get('category', None)
            questionObj = Question(question, answer, difficulty, category)
            questionObj.insert()
            return jsonify({
                'success': True
            })
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def searchForQeustion():
        try:
            reqJson = request.json
            searchTerm = reqJson['searchTerm']
            searched_questions = Question.query.filter(
                Question.question.ilike(f'%{searchTerm}%')).all()
            formatted_questions = [question.format()
                                   for question in searched_questions]
            totalQuestions = len(formatted_questions)
            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'totalQuestions': totalQuestions,
                'currentCategory': None
            })
        except:
            abort(422)

    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def categoryQuestions(id):
        try:
            categoryId = id
            questionsList = Question.query.filter_by(
                category=id).all()

            formated_questionList = [question.format()
                                     for question in questionsList]
            totalQuestions = len(questionsList)
            return jsonify({
                'success': True,
                'questions': formated_questionList,
                'totalQuestions': totalQuestions,
                'currentCategory': categoryId
            })
        except:
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        try:
            req = request.get_json()
            previous_questions = req.get('previous_questions', None)
            quiz_category = req.get('quiz_category', None)
            questions = Question.query.filter_by(category=quiz_category['id']).filter(
                Question.id.notin_(previous_questions)).all()
            if len(questions) > 0:
                question = random.choice(questions).format()
                return jsonify({
                    'success': True,
                    'question': question
                })
            else:
                return jsonify({
                    'success': True,
                    'question': None

                })
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(erroe):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422
    return app
