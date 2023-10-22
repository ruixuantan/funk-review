CREATE TABLE track (
    id INT,
    user_id VARCHAR,
    track_id INT,
    clicked_on TIMESTAMP(3),
    WATERMARK FOR clicked_on AS clicked_on - INTERVAL '15' SECOND
) WITH (
    'connector' = '{{ connector }}',
    'topic' = '{{ topic }}',
    'properties.bootstrap.servers' = '{{ bootstrap_servers }}',
    'properties.group.id' = '{{ consumer_group_id }}',
    'scan.startup.mode' = '{{ scan_startup_mode }}',
    'format' = '{{ format }}'
);
