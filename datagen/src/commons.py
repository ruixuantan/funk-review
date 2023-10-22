from typing import List

from clients import PostgresClient


def get_track_ids() -> List[int]:
    ids = []
    db = PostgresClient.from_env()
    with db:
        db.cur.execute("SELECT id FROM Tracks")
        ids = [row[0] for row in db.cur.fetchall()]

    return ids
