INSERT INTO TrackMetrics
SELECT
    COALESCE(r.track_id, t.track_id) AS track_id,
    COALESCE(r.total_rating, 0) AS total_rating,
    COALESCE(r.rating_count, 0) AS rating_count,
    COALESCE(t.view_count, 0) AS view_count,
    COALESCE(r.window_start, t.window_start) AS start_at,
    COALESCE(r.window_end, t.window_end) AS end_at
FROM
(
    SELECT
        window_start,
        window_end,
        track_id,
        SUM(rating) AS total_rating,
        COUNT(id) AS rating_count
    FROM TABLE(TUMBLE(TABLE review, DESCRIPTOR(reviewed_on), INTERVAL '5' MINUTES))
    GROUP BY window_start, window_end, track_id
) AS r
FULL JOIN
(
    SELECT
        window_start,
        window_end,
        track_id,
        COUNT(id) AS view_count
    FROM TABLE(TUMBLE(TABLE view, DESCRIPTOR(viewed_on), INTERVAL '5' MINUTES))
    GROUP BY window_start, window_end, track_id
) AS t
ON
    r.track_id = t.track_id AND
    r.window_start = t.window_start AND
    r.window_end = t.window_end;
