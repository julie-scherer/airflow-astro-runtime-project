SELECT course_id, video_url, raw_video_url
FROM schema_name.courses
WHERE 1=1
  and (raw_video_url ilike '%.mp4')
  and (video_url ilike '%.mp4' or video_url is null)
ORDER BY course_id desc