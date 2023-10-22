from clients import KafkaProducer, PostgresClient


def reset():
    kafka = KafkaProducer.from_env()
    kafka.delete_topic()
    pgcli = PostgresClient.from_env()
    with pgcli:
        pgcli.cur.execute("DELETE FROM TrackMetrics")


if __name__ == "__main__":
    reset()
