include .env

up:
	docker compose up --build -d

run:
	docker compose up

down:
	docker compose down

db-shell:
	docker-compose exec funkreview-db psql -d ${FUNKREVIEW_DB_NAME} -U ${FUNKREVIEW_DB_USER} -p ${FUNKREVIEW_DB_PORT}

gen-reviews:
	docker-compose run --rm datagen python reviews.py

gen-tracks:
	docker-compose run --rm datagen python tracks.py

reset-data:
	docker-compose run --rm datagen python reset.py

flink:
	docker-compose exec jobmanager ../bin/flink run --python update_reviews.py

.PHONY: datagen flink
