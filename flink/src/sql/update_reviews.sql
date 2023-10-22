SELECT
    r.id AS id,
    r.total_rating AS total_rating,
    r.rating_count AS rating_count,
    t.view_count AS view_count
FROM
(
    SELECT
        window_start,
        window_end,
        track_id AS id,
        SUM(rating) AS total_rating,
        COUNT(id) AS rating_count
    FROM TABLE(TUMBLE(TABLE review, DESCRIPTOR(reviewed_on), INTERVAL '5' MINUTES))
    GROUP BY window_start, window_end, track_id
) AS r
JOIN
(
    SELECT
        window_start,
        window_end,
        track_id AS id,
        COUNT(id) AS view_count
    FROM TABLE(TUMBLE(TABLE track, DESCRIPTOR(clicked_on), INTERVAL '5' MINUTES))
    GROUP BY window_start, window_end, track_id
) AS t
ON r.id = t.id AND r.window_start = t.window_start AND r.window_end = t.window_end
