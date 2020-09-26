# UdacityProductionHouse
This project is the capstone project for the Udacity Nanodegree program.

This project will serve as the backend of a Production House website. It shall have details of the movies and actors associated with it. 

- In the first phase of the project, I shall be working and submitting the backend to support actor and movie details.
- In the second phase of the project, I shall be creating a basic User Interface to access the information.
- In the next phase, I shall be working on associating actors with movies and its UI.

It is an exciting project for me as I shall be submitting a very initial version (with the first phase implemented), but will continue to build it further for better user experience.

## DETAILS OF THE INITIAL PHASE

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

# The current structure

When this project will be submitted, it shall have working API endpoints to:

- GET /actors
- POST /actors
- PATCH /actors/<int:actor_id>
- DELETE /actors/<int:actor_id>
- GET /movies
- POST /movies
- PATCH /movies/<int:movie_id>
- DELETE /movies/<int:movie_id>

To test this application, you can check all the above mentioned endpoints on postman using the following collection:

This is a RBAC