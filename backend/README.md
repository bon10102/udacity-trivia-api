# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

**Windows (psql tool)**
```powershell
CREATE DATABASE trivia;
```

**Linux**
```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

**Windows (psql tool)**
```powershell
\c trivia
\i trivia.psql
```

**Linux**
```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

In **Windows**, set the following parameters:
```powershell
$env:FLASK_APP='flaskr'
$env:FLASK_DEBUG='true'
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## API Endpoints

### `GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

### `GET '/questions'`

- Query the database for trivia questions
- Requests are paginated in groups of 10
- Request Parameters: (optional) page number:*int*
- Sample Request: `http://127.0.0.1:5000/questions?page=1`
- Return: list of question objects, success value, total number of questions, and dictionary of categories

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
  ],
  "success": true,
  "total_questions": 2
}
```

### `DELETE '/questions/{question_id}'`

- Delete the question with the specified ID, if it exists
- Request Arguments: question_id:*int*
- Sample Request: `curl http://127.0.0.1:5000/questions/1 -X DELETE` 
- Return: Success value, ID of the deleted book

```json
{
  "deleted": 1,
  "success": true
}
```

### `POST '/questions'`

- Add a new trivia question
- Request Parameters: (optional) page number:*int*
- Request Body:
  - question:*string*
  - answer:*string*
  - difficulty:*int*
  - category:*int*
- Sample Request: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Which continent are monkeys found?", "answer": "Africa", "category": 3, "difficulty": 1}'`
- Return: Success value, ID of the created book, and a list of updated questions based on page number

```json
{
  "created": 27,
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Africa",
      "category": 3,
      "difficulty": 1,
      "id": 27,
      "question": "Which continent are monkeys found?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

### `POST '/questions/search`

- Fetches all questions which matches the search term. Case insensitive and partial string matching
- Request Body: searchTerm:*string*
- Sample Request: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "monkey"}'`
- Returns: success value, list of questions matching the search term, number of questions matching the search term

```json
{
  "questions": [
    {
      "answer": "Africa",
      "category": 3,
      "difficulty": 1,
      "id": 27,
      "question": "Which continent are monkeys found?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

### `GET 'categories/{category_id}/questions'`

- Fetches all questions which belongs to the specified category ID. 
- Requests are paginated in groups of 10
- Request Parameters: (optional) page:*int*
- Request Arguments: category_id:*int*
- Sample Request: `curl http://127.0.0.1:5000/categories/1/questions?page=1`
- Returns: success value, list of questions, number of questions in the category, current category

```json
{
  "current_category": 1,
  "questions": [
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
    }
  ],
  "success": true,
  "total_questions": 3
}
```

### `POST '/quizzes'`

- Gets a randomized question to play the quiz
- previous_questions is a list used to store the questions already played. This is expected to be updated by the frontend
- Request Arguments:
  - previous_questions [ ]:*question object*
  - quiz_category {id:*int*, type:*string*}
- Sample Request: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "Science", "id": "1"}}'`
- Return: success value, one question object

```json
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true
}
``` 

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

**Windows (psql tool)**
```powershell
DROP DATABASE trivia_test;
CREATE DATABASE trivia_test;
\i trivia.psql
python test_flaskr.py
```

**Linux**
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
