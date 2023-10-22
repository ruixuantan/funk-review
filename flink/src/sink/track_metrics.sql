CREATE TABLE TrackMetrics(
    track_id INT NOT NULL,
    total_rating INT NOT NULL,
    rating_count BIGINT NOT NULL,
    view_count BIGINT NOT NULL,
    start_at TIMESTAMP(3) NOT NULL,
    end_at TIMESTAMP(3) NOT NULL
) WITH (
    'connector' = '{{ connector }}',
    'url' = '{{ url }}',
    'table-name' = '{{ table_name }}',
    'username' = '{{ username }}',
    'password' = '{{ password }}',
    'driver' = '{{ driver }}'
);
