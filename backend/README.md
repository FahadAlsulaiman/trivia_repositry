# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT

```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.

```

Endpoints
GET '/categories'
GET '/questions/<int:page>'
DELETE '/questions/<int:id>'
POST '/questions/addQuestion'
POST '/questions'
GET '/categories/<int:id>/questions'
POST '/quizzes'

GET '/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
  {'1' : "Science",
  '2' : "Art",
  '3' : "Geography",
  '4' : "History",
  '5' : "Entertainment",
  '6' : "Sports"}

GET '/questions/<int:page>'

- Fetches a list of questions based on the page size
- Request arguments : page number should be passed.
- Retruns: A dictionary of Questions, total numebr of questions, category list and current category if exists.
  {
  "categories": {
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
  },
  "currentCategory": null,
  "questions": [
  {
  "answer": "Escher",
  "category": 2,
  "difficulty": 1,
  "id": 16,
  "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
  },
  {
  "answer": "Mona Lisa",
  "category": 2,
  "difficulty": 3,
  "id": 17,
  "question": "La Giaconda is better known as what?"
  },
  {
  "answer": "One",
  "category": 2,
  "difficulty": 4,
  "id": 18,
  "question": "How many paintings did Van Gogh sell in his lifetime?"
  },
  {
  "answer": "Jackson Pollock",
  "category": 2,
  "difficulty": 2,
  "id": 19,
  "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
  },
  {
  "answer": "The Liver",
  "category": 1,
  "difficulty": 4,
  "id": 20,
  "question": "What is the heaviest organ in the human body?"
  },
  {
  "answer": "Alexander Fleming",
  "category": 1,
  "difficulty": 3,
  "id": 21,
  "question": "Who discovered penicillin?"
  },
  {
  "answer": "Blood",
  "category": 1,
  "difficulty": 4,
  "id": 22,
  "question": "Hematology is a branch of medicine involving the study of what?"
  },
  {
  "answer": "Scarab",
  "category": 4,
  "difficulty": 4,
  "id": 23,
  "question": "Which dung beetle was worshipped by the ancient Egyptians?"
  },
  {
  "answer": "A1",
  "category": 1,
  "difficulty": 1,
  "id": 50,
  "question": "Q1"
  },
  {
  "answer": "A2",
  "category": 2,
  "difficulty": 1,
  "id": 51,
  "question": "Q2"
  }
  ],
  "success": true,
  "totalQuestions": 10
  }
  DELETE '/questions/<int:id>'
- Deletes a Question based on the id passed
- request arguments : Question id
- Returns: A flag if the deletion is successfull
  {
  'success': True
  }

POST '/questions/addQuestion'

- Add a question to the questions list
- request arguments : takes an object as below
  {"question":"Q7",
  "answer":"A7",
  "difficulty":1,
  "category":1
  }
- Returns: A flag if the questuin added successfull

POST '/questions'

- Fetch questions based on search term.
- Request Arguments: Search Term
- Return: A question,answer,category and difficulty.
  {
  'success': True,
  'questions': formatted_questions,
  'totalQuestions': totalQuestions,
  'currentCategory': None
  }

GET '/categories/<int:id>/questions'

- Fetches questions based on category
- Requests Arguments: Category id
- Returns: A dictionary of Questions, total numebr of questions and current category if exists.
  {
  'success': True,
  'questions': formated_questionList,
  'totalQuestions': totalQuestions,
  'currentCategory': categoryId
  }
  POST '/quizzes'
- This API is responible of fetching the questions one by one based on the questions list that will be loaded in the first call based on the category , the api will pick one question
  randomly.
- Request argumants: previous_questions and category
- Returns: A question object
  {
  "question": {
  "answer": "Blood",
  "category": 1,
  "difficulty": 4,
  "id": 22,
  "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true
  }

## Testing

To run the tests, run

```
dropdb trivia_test -U postgres
createdb trivia_test -U postgres
psql trivia_test < trivia.psql -U postgres
python test_flaskr.py
```
