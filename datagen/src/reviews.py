import argparse
import json
import logging
import os
import random
import time
from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID, uuid4

import numpy as np
from clients import KafkaProducer
from commons import get_track_ids

logging.basicConfig(level=logging.INFO)


@dataclass
class Review:
    id: int
    user_id: UUID
    track_id: int
    rating: int

    @classmethod
    def kafka_topic(cls) -> str:
        return os.environ.get("KAFKA_REVIEW_TOPIC")

    def to_json(self) -> str:
        return json.dumps(
            {
                "id": self.id,
                "user_id": str(self.user_id),
                "track_id": self.track_id,
                "rating": self.rating,
                "reviewed_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )


def generate_review(id: int, track_ids: List[int]) -> Review:
    return Review(
        id=id,
        user_id=uuid4(),
        track_id=random.choice(track_ids),
        rating=random.randint(1, 5),
    )


def generate_reviews(track_ids: List[int], freq: int):
    kafka = KafkaProducer.from_env()
    id = 1
    while True:
        review = generate_review(id, track_ids)
        logging.info(f"{Review.kafka_topic()}\t{review.to_json()}")
        kafka.produce(Review.kafka_topic(), review.to_json())
        id += 1
        time.sleep(np.random.poisson(freq))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--frequency",
        type=int,
        help="Rate at which reviews are written to kafka topic. Follows poisson distribution.",
        default=5,
    )
    ids = get_track_ids()
    generate_reviews(ids, parser.parse_args().frequency)
