build: 
	python3 manage.py runserver

src:
	django-admin startproject src .

app:
	python3 manage.py startapp drive

mig:
	python3 manage.py migrate drive

appmig:
	python3 manage.py makemigrations drive

clean:
	find . -name "__pycache__" -exec rm -rf {} +

