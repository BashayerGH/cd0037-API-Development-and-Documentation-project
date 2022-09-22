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

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.
## API Endpoints

`1. GET '/api/trivia/categories'`

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

`2. GET '/api/trivia/questions'`

- Fetches a dictionary of questions (every 10 questions)
- Request Arguments: None
- Returns: An object with a single key, `questions`, `total`, `currentcategory`, `categories`


```json
{
   "categories":[
      {
         "id":1,
         "type":"Science"
      },
      {
         "id":2,
         "type":"Art"
      },
      {
         "id":3,
         "type":"Geography"
      },
      {
         "id":4,
         "type":"History"
      },
      {
         "id":5,
         "type":"Entertainment"
      },
      {
         "id":6,
         "type":"Sports"
      }
   ],
   "currentcategory":5,
   "questions":[
      {
         "answer":"Apollo 13",
         "category":5,
         "difficulty":4,
         "id":2,
         "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      },
      {
         "answer":"Tom Cruise",
         "category":5,
         "difficulty":4,
         "id":4,
         "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      },
      {
         "answer":"Maya Angelou",
         "category":4,
         "difficulty":2,
         "id":5,
         "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      },
      {
         "answer":"Muhammad Ali",
         "category":4,
         "difficulty":1,
         "id":9,
         "question":"What boxer's original name is Cassius Clay?"
      },
      {
         "answer":"Brazil",
         "category":6,
         "difficulty":3,
         "id":10,
         "question":"Which is the only team to play in every soccer World Cup tournament?"
      },
      {
         "answer":"Uruguay",
         "category":6,
         "difficulty":4,
         "id":11,
         "question":"Which country won the first ever soccer World Cup in 1930?"
      },
      {
         "answer":"George Washington Carver",
         "category":4,
         "difficulty":2,
         "id":12,
         "question":"Who invented Peanut Butter?"
      },
      {
         "answer":"The Palace of Versailles",
         "category":3,
         "difficulty":3,
         "id":14,
         "question":"In which royal palace would you find the Hall of Mirrors?"
      },
      {
         "answer":"Agra",
         "category":3,
         "difficulty":2,
         "id":15,
         "question":"The Taj Mahal is located in which Indian city?"
      },
      {
         "answer":"Escher",
         "category":2,
         "difficulty":1,
         "id":16,
         "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
      }
   ],
   "success":true,
   "total":30
}
```



`3. DELETE '/api/trivia/questions/{id}'`

- Delete a question by its id
- Request Arguments: Id of the question
- Returns: An object with a single key, `question_id` and `success` flag

```json
{
    "question_id": 2,
    "success": true
}
```

`4. POST '/api/trivia/questions'`

- Post a question by `question`, `answer`, `category`, `difficulty`
- Request Arguments: None
- Returns: the same request body with a success flag.

```json
{
    "answer": "..",
    "category": 2,
    "difficulty": 4,
    "question": "..",
    "success": true
}
```


`5. POST '/api/trivia/questions/search'`

- search for a question by `question`
- Request Arguments: searchTerm
- Returns: An object of `questions`, a single key, `currentcategory`, `success` flag and the total results number `total`

```json
{
    "currentcategory": 2,
    "questions": [
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        }
    ],
    "success": true,
    "total": 1
}
```



`6. POST '/api/trivia/categories/{id}/questions'`

- search for a question by `question` by its `category`
- Request Arguments: the id of the category `category_id`
- Returns: An object of `questions`, a single key, `category_id`, `success` flag and the total results number `total`

```json
{
    "category_id": 5,
    "questions": [
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        }
    ],
    "success": true,
    "total": 1
}
```


`7. POST '/api/trivia/quizzes'`

- get a question to play the quiz
- Request Arguments: `category` and `previous question` as parameters 
- Returns: An object of `question` and `success` flag

```json
{
    "question": [
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        }
    ],
    "success": true,
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia
createdb trivia
psql trivia < trivia.psql
python test_flaskr.py
```
