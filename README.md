# FSND: Capstone Project

## Content


1. [Motivation](#motivation)
2. [Start Project locally](#start-locally)
3. [API Documentation](#api)
4. [Authentification](#authentification)

<a name="motivation"></a>
## Motivations & Covered Topics

By completing this project, I learn and apply my skills on : 

1. Database modeling with `postgres` & `sqlalchemy` (see `models.py`)
2. API to performance CRUD Operations on database with `Flask` (see `app.py`)
3. Automated testing with `Unittest` (see `test_app`)
4. Authorization RBAC  with `Auth0` (see `auth.py`)
5. Deployment on `Heroku`

<a name="start-locally"></a>
## Start Project locally

Make sure you `cd` into the correct folder (with all app files) before following the setup steps.
Also, you need the latest version of [Python 3](https://www.python.org/downloads/)
and [postgres](https://www.postgresql.org/download/) installed on your machine.

### Pre-requisites and Local Development
Developers using this project should already have Python3, pip and node installed on their local machines.

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

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Getting Started

To start and run the local development server

1. Initialize and activate a virtualenv:
  ```bash
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
```bash
$ pip install -r requirements.txt
```

3. Auth0

If you only want to test the API, you can
simply use the existing bearer tokens in `test_app.py`.


4. Run the development server:
  ```bash 
  $ python3 app.py
  ```

5. Testing
To run the tests, run

```bash 
$ python3 test_app.py
```
It should give this response if everything went fine:

```bash
$ python3 test_app.py
.........................
----------------------------------------------------------------------
Ran 18 tests in 18.132s

OK

```
## API Reference
<a name="api"></a>

### Deployment

- Base URL: **_https://vn-capstone.herokuapp.com_**


### EndPoints

1. Actors
   1. [GET /actors](#get-actors)
   2. [POST /actors](#post-actors)
   3. [DELETE /actors](#delete-actors)
   4. [PATCH /actors](#patch-actors)
2. Movies
   1. [GET /movies](#get-movies)
   2. [POST /movies](#post-movies)
   3. [DELETE /movies](#delete-movies)
   4. [PATCH /movies](#patch-movies)

You can use access_token in for each role in `test_app.py`

### Roles

- Casting Assistant
  - Can view actors and movies
- Casting Director
  - All permissions a Casting Assistant has and…
  - Add or delete an actor from the database
  - Modify actors or movies
- Executive Producer
  - All permissions a Casting Director has and…
  - Add or delete a movie from the database


### Error Handling
Errors are returned as JSON objects in the following format:
```
{
  "success": False,
  "error": 400,
  "message": "bad request"
}
```

- Authorization Error
```
{
  'code': 'invalid_header',
  'description': 'Authorization header must be bearer token'
}
```

The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Unprocessable
- 401: invalid_header



# <a name="get-actors"></a>
### 1. GET /actors

```bash
$ curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X GET https://vn-capstone.herokuapp.com/actors
```
  - Return a list of actors, number of actors, success value

```js
{
  "actors": [
      {
        "age": 25,
        "gender": "male",
        "id": 1,
        "name": "John King"
      }
  ],
  "success": true,
  "total_actors": 1
}
```


# <a name="post-actors"></a>
### 2. POST /actors


```bash
$ curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X POST -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"name":"Dale","age":24,"gender":"male"}' https://vn-capstone.herokuapp.com/actors
```

  - Create a new actor using the submitted name, age, and gender. Return a list of actors, number of actors, success value.


```js
{
  "actors": [
      {
        "age": 25,
        "gender": "male",
        "id": 1,
        "name": "John King"
      },
      {
        "age": 24,
        "gender": "male",
        "id": 2,
        "name": "Dale"
      }
  ],
  "success": true,
  "total_actors": 2
}

```


# <a name="patch-actors"></a>
### 3. PATCH /actors

```bash
$ curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X PATCH -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"name":"Andy","age":24,"gender":"male"}' https://vn-capstone.herokuapp.com/actors/2
```


  - Update the actor of the given ID if it exists using the submitted name, age, and gender. Return a list of actors, number of actors, success value, updated actor id.



```js
{
  "actors": [
      {
        "age": 25,
        "gender": "male",
        "id": 1,
        "name": "John King"
      },
      {
        "age": 24,
        "gender": "male",
        "id": 2,
        "name": "Andy"
      }
  ],
  "success": true,
  "total_actors": 2,
  "updated": 2
}
```


# <a name="delete-actors"></a>
### 4. DELETE /actors


```bash
$ curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X DELETE https://vn-capstone.herokuapp.com/actors/2
```


  - Deletes the actor of the given ID if it exists. Return a list of remaining actors, success value, deleted actor id.


```js
{
  "actors": [
      {
        "age": 25,
        "gender": "male",
        "id": 1,
        "name": "John King"
      }
  ],
  "success": true,
  "deleted": 2
}

```


# <a name="get-movies"></a>
### 5. GET /movies

```bash
$ curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X GET https://vn-capstone.herokuapp.com/movies
```

  - Return a list of movies, number of movies, success value

```js
{
  "movies": [
      {
        "id": 1,
        "release_date": "12/2019",
        "title": "King Kong"
      }
  ],
  "success": true,
  "total_movies": 1
}
```

# <a name="post-movies"></a>
### 6. POST /movies


```bash
$ curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X POST -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"title":"New Year","release_date":"5/2018"}' https://vn-capstone.herokuapp.com/movies
```


  - Create a new movie using the submitted title, release_date. Return a list of movies, number of movies, success value.




```js
{
  "movies": [
      {
        "id": 1,
        "release_date": "12/2019",
        "title": "King Kong"
      },
      {
        "id": 2,
        "release_date": "5/2018",
        "title": "New Year"
      }
  ],
  "success": true,
  "total_movies": 2
}
```

# <a name="patch-movies"></a>
### 7. PATCH /movies

```bash
$ curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X PATCH -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"title":"New Year","release_date":"3/2015"}' https://vn-capstone.herokuapp.com/movies/2
```

  - Update the movie of the given ID if it exists using the title, release_date. Return a list of movies, number of movies, success value, and updated movie id.



```js
{
  "movies": [
      {
        "id": 1,
        "release_date": "12/2019",
        "title": "King Kong"
      },
      {
        "id": 2,
        "release_date": "3/2015",
        "title": "New Year"
      }
  ],
  "success": true,
  "total_movies": 2
}
```

# <a name="delete-movies"></a>
### 8. DELETE /movies

```bash
$ curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X DELETE https://vn-capstone.herokuapp.com/movies/2
```

  - Deletes the movie of the given ID if it exists. Return a list of remaining movies, success value, deleted movie id.


```js
{
    "movies": [
        {
          "id": 1,
          "release_date": "12/2019",
          "title": "King Kong"
        }
    ],
    "success": true,
    "deleted": 2
}
```

## Authors
Vu Nguyen

## Acknowledgements
The instructors at Udacity.