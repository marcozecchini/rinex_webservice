sudo docker-compose up -d --build
heroku login
heroku container:login
heroku container:push web
heroku container:release web

heroku run python3 manage.py migrate
heroku open