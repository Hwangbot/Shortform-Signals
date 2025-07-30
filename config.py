import os

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'shortform_signals',
    'user': 'postgres',
    'password': 'password'  # Change this in production
}

# File Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")

# CSV Files
VIDEOS_FILE = os.path.join(SCRIPT_DIR, "shortform_videos.csv")
CREATORS_FILE = os.path.join(SCRIPT_DIR, "shortform_creators.csv")
PLATFORMS_FILE = os.path.join(SCRIPT_DIR, "shortform_platforms.csv")

# Database Connection String
DB_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}" 