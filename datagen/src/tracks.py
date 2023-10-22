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
class TrackClick:
    id: int
    user_id: UUID
    track_id: int

    @classmethod
    def kafka_topic(cls) -> str:
        return os.environ.get("KAFKA_TRACK_TOPIC")

    def to_json(self) -> str:
        return json.dumps(
            {
                "id": self.id,
                "user_id": str(self.user_id),
                "track_id": self.track_id,
                "clicked_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )


def generate_track_click(id: int, track_ids: List[int]) -> TrackClick:
    return TrackClick(
        id=id,
        user_id=uuid4(),
        track_id=random.choice(track_ids),
    )


def generate_track_clicks(track_ids: List[int], freq: int):
    kafka = KafkaProducer.from_env()
    id = 1
    while True:
        track_click = generate_track_click(id, track_ids)
        logging.info(f"{TrackClick.kafka_topic()}\t{track_click.to_json()}")
        kafka.produce(TrackClick.kafka_topic(), track_click.to_json())
        id += 1
        time.sleep(np.random.poisson(freq))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--frequency",
        type=int,
        help="Rate at which reviews are written to kafka topic. Follows poisson distribution.",
        default=1,
    )
    track_ids = get_track_ids()
    generate_track_clicks(track_ids, parser.parse_args().frequency)
