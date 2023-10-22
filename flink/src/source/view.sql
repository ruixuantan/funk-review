CREATE TABLE view (
    id INT,
    user_id VARCHAR,
    track_id INT,
    viewed_on TIMESTAMP(3),
    WATERMARK FOR viewed_on AS viewed_on - INTERVAL '15' SECOND
) WITH (
    'connector' = '{{ connector }}',
    'topic' = '{{ topic }}',
    'properties.bootstrap.servers' = '{{ bootstrap_servers }}',
    'properties.group.id' = '{{ consumer_group_id }}',
    'scan.startup.mode' = '{{ scan_startup_mode }}',
    'format' = '{{ format }}'
);
