CREATE TABLE shortform_videos (
  video_id TEXT PRIMARY KEY,
  creator_id TEXT,
  format_type TEXT,
  duration_sec INT,
  views INT,
  likes INT,
  comments INT,
  shares INT,
  watch_time INT,
  full_views INT,
  hook_watch_rate FLOAT
);

CREATE TABLE shortform_creators (
  creator_id TEXT PRIMARY KEY,
  creator_name TEXT,
  niche TEXT,
  followers INT
);

CREATE TABLE shortform_platforms (
  platform TEXT PRIMARY KEY,
  daily_users_millions INT,
  avg_session_time_min FLOAT,
  algorithm_type TEXT
);
