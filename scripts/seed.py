import argparse
import csv
from dataclasses import dataclass
from typing import Iterator

DATASET_FILE = "dataset/spotify-2023.csv"
OUTPUT_FILE = "funkreview-db/seed/seed.csv"


@dataclass
class Track:
    id: int
    track_name: str
    artists_name: str
    artist_count: int
    released_year: int
    released_month: int
    released_day: int


def read_file(num_tracks: int, file_path: str = DATASET_FILE) -> Iterator[Track]:
    id = 1
    with open(file_path, encoding="ISO-8859-1") as f:
        reader = csv.DictReader(f)
        for line in reader:
            yield Track(
                id=id,
                track_name=line["track_name"],
                artists_name=line["artist(s)_name"],
                artist_count=line["artist_count"],
                released_year=line["released_year"],
                released_month=line["released_month"],
                released_day=line["released_day"],
            )
            if id == num_tracks:
                return
            id += 1


def write_file(num_tracks: int, file_path: str = OUTPUT_FILE):
    with open(file_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "id",
                "track_name",
                "artists_name",
                "artist_count",
                "released_year",
                "released_month",
                "released_day",
                "total_rating",
                "rating_count",
            ]
        )
        for track in read_file(num_tracks):
            writer.writerow(
                [
                    track.id,
                    track.track_name,
                    track.artists_name,
                    track.artist_count,
                    track.released_year,
                    track.released_month,
                    track.released_day,
                ]
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--num_tracks",
        type=int,
        help="Number of tracks to be included in parsed dataset.",
        default=25,
    )
    write_file(parser.parse_args().num_tracks)
