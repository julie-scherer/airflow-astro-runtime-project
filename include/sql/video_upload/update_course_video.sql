UPDATE schema_name.courses
SET
  video_url = '{{ s3_m3u8_path }}',
  duration_seconds = {{ duration_seconds }},
  processing_completion_time = '{{ timestamp }}'
WHERE course_id = {{ course_id }} and raw_video_url = '{{ raw_video_url }}'