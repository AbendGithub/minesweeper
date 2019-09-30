# minesweeper

## Notes

Api is documented in swagger. It can be accessed through the base URL: https://vast-taiga-54811.herokuapp.com/
Summary:
To create a new game -> POST /games
Send actions to a game -> PUT /games/<game_id>

## Decisions

- As the project was meant to be small, flask was the natural choice over django.
- As the API idea is to be consumed by a mobile app, practicality was chosen over standard. A truly RESTful api expose resources with basics CRUD operations, but usually it is not completely handy.
- flask-restplus was chosen mainly because the swagger feature which is very useful.
- Flask-Migrate is almost a standard in every project and simplify queries.
- The main focus was on the api implementation and swagger documentation.

## Time Spent

Honestly, it has taken me a bit longer than expected, I had to take care of other things along the day and underestimated a bit the challenge. Looking at the commits, it has been the 5 hours more or less in total.
 
 
