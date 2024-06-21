create_venv:
	python -m venv venv

activate_venv:
	venv\Scripts\activate

install_reqs:
	pip install -r requirements.txt

build:
	docker compose build

docker_up:
	docker compose up -d

docker_logs:
	docker compose logs -f

docker_down:
	docker compose down