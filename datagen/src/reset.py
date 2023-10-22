from clients import KafkaProducer


def reset():
    kafka = KafkaProducer.from_env()
    kafka.delete_topic()


if __name__ == "__main__":
    reset()
