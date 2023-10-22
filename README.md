# Funk Review
A data engineering streaming project.

## Architecture
![Architecture](./images/architecture_diagram.png)

## Setting up
1. Create a python virtual environment at the root of this project and install the requirements.
    ```sh
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
1. Run `python scripts/seed.py` to create the seed data for the postgres database.
1. Run `make up` to build and start the docker containers. Use `make run` on subsequent runs. Use `make down` to teardown the containers.
1. Once the containers are up, run `make gen-reviews` and `make gen-views` to send messages to the kafka cluster.
1. Run `make flink` to start the flink pipeline. The flink UI can be accessed at `localhost:8081`
1. The postgres database can be accessed with `make db-shell`
