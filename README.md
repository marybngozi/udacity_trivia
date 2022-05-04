# Trivia App

This is an amazing quiz app, where users can play a trivia based on category.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

All required packages are included in the requirements file.

```
cd backend/
pip install requirements.txt
```

To run the application run the following commands:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

#### Frontend

From the root folder, run the following commands to start the client:

```
cd frontend/
npm install // only once to install dependencies
npm start
```

By default, the frontend will run on localhost:3000.

### Tests

In order to run tests navigate from the root folder and run the following commands:

```
cd backend/
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 405: Method Not Found
- 500: Internal Server Error

# Endpoints

### GET /categories

- General:
  - Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
- Sample Request:

```
curl http://127.0.0.1:5000/categories
```

- Sample Response:

```
{
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```

### GET /questions?page=${integer}

- General:
  - Fetches a paginated set of questions, a total number of questions, all categories and current category string.
  - Request Arguments: page - integer
  - Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
- Sample Request:

```
curl http://127.0.0.1:5000/questions?page=1
```

- Sample Response:

```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}
```

### GET /categories/${id}/questions

- General:
  - Fetches questions for a cateogry specified by id request argument
  - Request Arguments: id - integer
  - Returns: An object with questions for the specified category, total questions, and current category string
- Sample Request:

```
curl http://127.0.0.1:5000/categories/1/questions
```

- Sample Response:

```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```

### DELETE /questions/{question_id}

- General:
  - Deletes a question using the id
  - Takes the id of the question to be deleted
  - Returns the id of the deleted question
- Sample Request:

```
curl -X DELETE http://127.0.0.1:5000/questions/12
```

- Sample Response:

```
{
    "deleted": 16,
}
```

### POST /quizzes

- General:
  - Sends a post request in order to get the next question
  - Takes the previous_questions and quiz_category
  - Returns: a single new question object that is not in the previous_questions
- Sample Request:

```
curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [1, 4, 20, 15]
    quiz_category": "current category"}'
```

- Sample Response:

```
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer',
        'difficulty': 5,
        'category': 4
    }
}
```

### POST /questions

- General:
  - Sends a post request in order to add a new question
  - Takes a JSON object containing keys: question, answer, difficulty, category
  - Returns: the new question
- Sample Request:

```
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Heres a new question string", "answer":"Heres a new answer string", "difficulty":1, "category":3}'
```

- Sample Response:

```
{
    'question': {
        'id': 24,
        'question': 'Heres a new question string',
        'answer': 'Heres a new answer string',
        'difficulty': 1,
        'category': 3
    }
}
```

### POST /questions

- General:
  - Sends a post request in order to search for a specific question by search term
  - Takes a JSON object containing key: searchTerm
  - Returns: any array of questions, a number of totalQuestions that met the search term and the current category string
- Sample Request:

```
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "this"}'
```

- Sample Response:

```
{

    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'Entertainment'

}
```

## Deployment N/A

## Authors

Yours truly, MaryBlessing Umeh

## Acknowledgements

The awesome team at Udacity and my friends and families!

## License

The contents of this repository are covered under the MIT License.
