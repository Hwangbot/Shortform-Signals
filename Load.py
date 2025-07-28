import os
import pandas as pd
from sqlalchemy import create_engine

# Absolute path to the folder where Load.py lives
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "../Database")

# Build full file paths
videos_path = os.path.join(data_dir, "shortform_videos.csv")
creators_path = os.path.join(data_dir, "shortform_creators.csv")
platforms_path = os.path.join(data_dir, "shortform_platforms.csv")

# Connect to PostgreSQL
engine = create_engine("postgresql://postgres:password@localhost:5432/database_name")

# Load data
videos = pd.read_csv(videos_path)
creators = pd.read_csv(creators_path)
platforms = pd.read_csv(platforms_path)

# Push to PostgreSQL
videos.to_sql("shortform_videos", engine, if_exists="replace", index=False)
creators.to_sql("shortform_creators", engine, if_exists="replace", index=False)
platforms.to_sql("shortform_platforms", engine, if_exists="replace", index=False)

print("✅ Data loaded successfully into PostgreSQL.")