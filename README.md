News Blog
deploy project on your local machine:
1 - To deploy project on your local machine create new virtual environment and execute this command:

pip install -r requirements.txt

2 - Rename example.env to .env and change config.

3 - Migrate db models to PostgreSQL:

python manage.py migrate

4 - Run app:

python manage.py runserver

5: Run celery worker:

celery -A <MODULE_NAME> worker -l info