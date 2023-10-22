CREATE TABLE Tracks(
    id INT,
    track_name INT,
    artists_name VARCHAR,
    artist_count INT,
    released_year INT,
    released_month INT,
    released_day INT,
    total_rating INT ,
    rating_count INT
) WITH (
    'connector' = '{{ connector }}',
    'url' = '{{ url }}',
    'table-name' = '{{ table_name }}',
    'username' = '{{ username }}',
    'password' = '{{ password }}',
    'driver' = '{{ driver }}'
);
