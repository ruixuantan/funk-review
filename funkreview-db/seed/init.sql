DROP TABLE IF EXISTS Tracks CASCADE;

CREATE TABLE Tracks(
    id SERIAL PRIMARY KEY,
    track_name TEXT NOT NULL,
    artists_name TEXT NOT NULL,
    artist_count SMALLINT NOT NULL,
    released_year INT NOT NULL,
    released_month SMALLINT NOT NULL,
    released_day SMALLINT NOT NULL
);

CREATE TABLE TrackMetrics(
    track_id INT NOT NULL,
    total_rating BIGINT NOT NULL,
    rating_count BIGINT NOT NULL,
    view_count BIGINT NOT NULL,
    start_at TIMESTAMP NOT NULL,
    end_at TIMESTAMP NOT NULL,
    FOREIGN KEY (track_id) REFERENCES Tracks(id)
);

COPY Tracks FROM '/docker-entrypoint-initdb.d/seed.csv' DELIMITER ',' CSV HEADER;
