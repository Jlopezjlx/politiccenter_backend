# Politic Center

This is a SPA to be able to manage people that belongs to specific politic party with some extras features.

This repo contains the API of the project. 

## Run this project

###### Run locally

Install dependencies:
```
pip install -r requirements.txt 
```
Run project:
```.env
export FLASK_APP=api
flask run

or

python main.py
```

###### Run with Docker
Build and run image
```
docker build -t "<name>"
docker run -p 5000:5000 <name_use_above>
```


## Tools

1. Python
2. Flask
3. Mysql
4. AWS RDS Service
5. Heroku
