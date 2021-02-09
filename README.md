# ARTWAY-PROJECT
Core backend service for open-source "ArtWay" project for RTUITLab

Frontend source code:
https://github.com/Zayac11/ARTWAY-FRONTEND

All API documentation is on the "Wiki" page of this GitHub repository

## Launching project locally
1. Clone project

`git clone <repo_name> .`

2. Create new virtual environment and then activate it

```
python3 -m venv venv`

source venv/bin/activate
```

3. Install dependencies

`pip install -r requirements.txt`

4. Create new PostgreSQL database


5. Create `.env` file in the directory named `project` and add your secret data to it

```
SECRET_KEY=<your_secret_key>
DOMAIN_NAME_DEV=127.0.0.1:8000
DOMAIN_NAME=<your_prod_domain_name_if_exists>
EMAIL_HOST_PASSWORD=<your_email_app_password>
DB_NAME=<your_db_name>
DB_USER=<your_db_user_name>
DB_PASSWORD=<your_db_user_password>
```

6. Make migrations

`python manage.py makemigrations`


7. Apply them.

`python manage.py migrate`

8. Start the development server

`python manage.py runserver`

## Deploying project to prod.
