sudo docker-compose up -d --build
heroku login
heroku container:login
sudo heroku container:push web
sudo heroku container:release web

heroku run python3 manage.py migrate
heroku open