# UdacityProductionHouse
This project is the capstone project for the Udacity Nanodegree program.

This project will serve as the backend of a Production House website. It shall have details of the movies and actors associated with it. 

- In the first phase of the project, I shall be working and submitting the backend to support actor and movie details.
- In the second phase of the project, I shall be creating a basic User Interface to access the information.
- In the next phase, I shall be working on associating actors with movies and its UI.

It is an exciting project for me as I shall be submitting a very initial version (with the first phase implemented), but will continue to build it further for better user experience.

# DETAILS OF THE INITIAL PHASE

This project is based on Role Based Access Control. It has been set up via Auth0. The following roles along with their permissions have been set up:

- Casting Assistant: 
    - Can view actors and movies

- Casting Director:
    - All permissions a Casting Assistant has
    - Add or delete an actor from the database
    - Modify actors or movies

- Executive Producer:
    - All permissions a Casting Director has
    - Add or delete a movie from the database

- The application is hosted on heroku at: https://udacityproductionhouse.herokuapp.com/
- The Auth0 is set up at: https://gogirl.us.auth0.com/authorize?audience=productionhouse&response_type=token&client_id=K1ueY2GupUBMrurXVADOyt8QFOguy2za&redirect_uri=https://udacityproductionhouse.herokuapp.com/

As the frontend is not developed, you will be able to test all endpoints using Postman:
- Sign up an account on [Postman](https://getpostman.com).
- Import the postman collection from the GitHub repository.
- Run the udacityproduction collection.

This collection contains the tests for RBAC based on the roles and permissions mentioned above. All roles have updated JWT token information. If you want to create new tokens:
1. Navigate to https://gogirl.us.auth0.com/authorize?audience=productionhouse&response_type=token&client_id=K1ueY2GupUBMrurXVADOyt8QFOguy2za&redirect_uri=https://udacityproductionhouse.herokuapp.com/
2. Sign in using one of the following email addresses:
    - email: executiveproducer@gmail.com    password: zahra2017!
    - email: castingdirector@gmail.com      password: zahra2017!
    - email: castingassistant@gmail.com     password: zahra2017!
3. Note the access token and based on the role, update in the postman collection and setup.sh file and then run the tests.

## The current database structure

The database is set up with the following three tables and their column details:

- actors:
    id: Integer, Primary Key
    name: String(Text)
    age: Integer 
    gender: String(Text)

- movies:
    id: Integer, Primary Key
    title: String(Text)
    releasedate: String(Text)

- castdetails: Many-to-Many relationship table - Will be worked on in the second phase
    id: Integer, Primary Key
    movie_id: Foreign key (id from the table 'movies')
    actor_id: Foreign key (id from the table 'actors')

## The current API structure

This project has the following working API endpoints (You can test them all using the postman collection as described above):

- GET /actors
    returns a json with the following information:
    - 'success': True or false based on the successful or unsuccessful run of method
    - 'actors': List of actors with the detail of each actor as stored in the database
- POST /actors
    returns a json with the following information:
    - 'success': True or false based on the successful or unsuccessful run of method
    - 'actor': The newly added actor details
- PATCH /actors/<int:actor_id>
    returns a json with the following information:
    - 'success': True or false based on the successful or unsuccessful run of method
    - 'actor': The updated actor details
- DELETE /actors/<int:actor_id>
    returns a json with the following information:
    - 'success': True or false based on the successful or unsuccessful run of method
    - 'deleted': The id of the deleted actor
 GET /movies
    returns a json with the following information:
    - 'success': True or false based on the successful or unsuccessful run of method
    - 'movies': List of movies with the title and release date of each movie as stored in the database
- POST /movies
    returns a json with the following information:
    - 'success': True or false based on the successful or unsuccessful run of method
    - 'movie': The newly added movie details
- PATCH /movies/<int:movie_id>
    returns a json with the following information:
    - 'success': True or false based on the successful or unsuccessful run of method
    - 'movie': The updated movie details
- DELETE /movies/<int:movie_id>
    returns a json with the following information:
    - 'success': True or false based on the successful or unsuccessful run of method
    - 'deleted': The id of the deleted movie


## Running the unit test

You can run the unit test on your local environment by following the method mentioned below:

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

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Running the unit test

1. Download the GitHub repository sughramehdi/UdacityProductionHouse
2. Export environment variables by running the setup.sh file:
    - For Windows: run command 'source setup.sh' from the command prompt
3. Run the test_app.py file by running command: 'python test_app.py'
