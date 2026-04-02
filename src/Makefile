SOURCE_PATH = projectBody/manage.py

all: run

run:
	docker rm -f container
	docker build -t firstproject .
	docker run -p 8000:8000 --rm --name container -v $(PWD)/projectBody/media:/app/projectBody/media firstproject

run_launch:
	python3 $(SOURCE_PATH) makemigrations
	python3 $(SOURCE_PATH) migrate
	python3 $(SOURCE_PATH) runserver 0.0.0.0:8000

run_test:
	cd projectBody && python3 manage.py test

install_dep:
	pip3 install -r requirements.txt

stop_docker:
	docker stop container