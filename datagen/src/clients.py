from __future__ import annotations

import logging
import os

import psycopg2
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient

logging.basicConfig(level=logging.DEBUG)


class KafkaProducer:
    producer: Producer
    admin: AdminClient

    def __init__(self, url: str):
        conf = {"bootstrap.servers": url}
        self.producer = Producer(conf)
        self.admin = AdminClient(conf)

    @classmethod
    def from_env(cls) -> KafkaProducer:
        return cls(
            f"{os.environ.get('KAFKA_HOST')}:{os.environ.get('KAFKA_PORT')}",
        )

    def produce(self, topic: str, event: str):
        self.producer.produce(topic, event)
        self.producer.flush()

    def delete_topic(self):
        topics = list(self.admin.list_topics().topics.keys())
        try:
            fs = self.admin.delete_topics(topics)
        except ValueError:
            logging.debug("All topics deleted")
            return

        for topic, f in fs.items():
            try:
                f.result()
                logging.debug(f"Topic {topic} deleted")
            except Exception as e:
                logging.debug(f"Failed to delete topic {topic}: {e}")


class PostgresClient:
    host: str
    db: str
    user: str
    password: str
    port: str
    conn: psycopg2.extensions.connection
    cur: psycopg2.extensions.cursor

    def __init__(self, host: str, db: str, user: str, password: str, port: str):
        self.host = host
        self.db = db
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_env(cls) -> PostgresClient:
        return cls(
            host=os.environ.get("FUNKREVIEW_DB_HOST"),
            db=os.environ.get("FUNKREVIEW_DB_NAME"),
            user=os.environ.get("FUNKREVIEW_DB_USER"),
            password=os.environ.get("FUNKREVIEW_DB_PASSWORD"),
            port=os.environ.get("FUNKREVIEW_DB_PORT"),
        )

    def __enter__(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.db,
            user=self.user,
            password=self.password,
            port=self.port,
        )
        self.cur = self.conn.cursor()

    def __exit__(self, exception_type, exc_val, traceback):
        self.cur.close()
        self.conn.commit()
        self.conn.close()
