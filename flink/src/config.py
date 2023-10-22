import os
from dataclasses import asdict, dataclass

from jinja2 import Environment, FileSystemLoader

JARS = [
    "file:///opt/flink/flink-sql-connector-kafka-1.17.0.jar",
    "file:///opt/flink/flink-connector-jdbc-3.0.0-1.16.jar",
    "file:///opt/flink/postgresql-42.6.0.jar",
]


@dataclass(frozen=True)
class KafkaConfig:
    connector: str = "kafka"
    bootstrap_servers: str = (
        f"{os.environ.get('KAFKA_HOST')}:{os.environ.get('KAFKA_PORT')}"
    )
    consumer_group_id: str = os.environ.get("KAFKA_GROUP_ID")
    scan_startup_mode: str = "earliest-offset"
    format: str = "json"


@dataclass(frozen=True)
class TrackConfig(KafkaConfig):
    topic: str = os.environ.get("KAFKA_TRACK_TOPIC")
    filename: str = "track"


@dataclass(frozen=True)
class ReviewConfig(KafkaConfig):
    topic: str = os.environ.get("KAFKA_REVIEW_TOPIC")
    filename: str = "review"


@dataclass(frozen=True)
class TracksPostgresConfig:
    connector: str = "jdbc"
    url: str = (
        f"jdbc:postgresql://{os.environ.get('FUNKREVIEW_DB_HOST')}:"
        f"{os.environ.get('FUNKREVIEW_DB_PORT')}/"
        f"{os.environ.get('FUNKREVIEW_DB_NAME')}"
    )
    table_name: str = "Tracks"
    username: str = os.environ.get("FUNKREVIEW_DB_USER")
    password: str = os.environ.get("FUNKREVIEW_DB_PASSWORD")
    driver: str = "org.postgresql.Driver"
    filename: str = "tracks"


@dataclass(frozen=True)
class UpdateReviewsSQL:
    filename: str = "update_reviews"


def get_sql_query(
    entity: str,
    template_env: Environment = Environment(loader=FileSystemLoader("./")),
) -> str:
    if entity == TrackConfig.__name__:
        config = TrackConfig()
        filename = f"source/{config.filename}.sql"
    elif entity == ReviewConfig.__name__:
        config = ReviewConfig()
        filename = f"source/{config.filename}.sql"
    elif entity == TracksPostgresConfig.__name__:
        config = TracksPostgresConfig()
        filename = f"sink/{config.filename}.sql"
    elif entity == UpdateReviewsSQL.__name__:
        config = UpdateReviewsSQL()
        filename = f"sql/{config.filename}.sql"
    else:
        assert False, f"{entity} is not a valid entity"

    return template_env.get_template(filename).render(asdict(config))
