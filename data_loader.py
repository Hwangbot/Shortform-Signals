import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from config import DB_URL, VIDEOS_FILE, CREATORS_FILE, PLATFORMS_FILE
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ShortformDataLoader:
    def __init__(self):
        self.engine = None
        self.videos = None
        self.creators = None
        self.platforms = None
        
    def connect_database(self):
        """Establish database connection with error handling"""
        try:
            self.engine = create_engine(DB_URL)
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info(" Database connection established successfully")
            return True
        except Exception as e:
            logger.error(f" Database connection failed: {e}")
            return False
    
    def load_csv_data(self):
        """Load CSV files with validation"""
        try:
            # Load videos data
            self.videos = pd.read_csv(VIDEOS_FILE)
            logger.info(f" Loaded {len(self.videos)} video records")
            
            # Load creators data
            self.creators = pd.read_csv(CREATORS_FILE)
            logger.info(f" Loaded {len(self.creators)} creator records")
            
            # Load platforms data
            self.platforms = pd.read_csv(PLATFORMS_FILE)
            logger.info(f" Loaded {len(self.platforms)} platform records")
            
            return True
        except FileNotFoundError as e:
            logger.error(f" File not found: {e}")
            return False
        except Exception as e:
            logger.error(f" Error loading data: {e}")
            return False
    
    def validate_data(self):
        """Validate data quality and consistency"""
        issues = []
        
        # Check for missing values
        for df_name, df in [('videos', self.videos), ('creators', self.creators), ('platforms', self.platforms)]:
            missing = df.isnull().sum()
            if missing.sum() > 0:
                issues.append(f"Missing values in {df_name}: {missing[missing > 0].to_dict()}")
        
        # Check for duplicate video IDs
        if self.videos['video_id'].duplicated().any():
            issues.append("Duplicate video IDs found")
        
        # Check for invalid retention rates (if column exists)
        if 'retention_rate' in self.videos.columns:
            if (self.videos['retention_rate'] > 1).any():
                issues.append("Invalid retention rates > 100% found")
        
        # Check for negative values in metrics
        numeric_cols = ['views', 'likes', 'comments', 'shares', 'watch_time', 'full_views']
        for col in numeric_cols:
            if (self.videos[col] < 0).any():
                issues.append(f"Negative values found in {col}")
        
        if issues:
            logger.warning(" Data validation issues found:")
            for issue in issues:
                logger.warning(f"  - {issue}")
        else:
            logger.info(" Data validation passed")
        
        return len(issues) == 0
    
    def calculate_derived_metrics(self):
        """Calculate additional metrics for analysis"""
        # Engagement rate
        self.videos['engagement_rate'] = (
            (self.videos['likes'] + self.videos['comments'] + self.videos['shares']) / 
            self.videos['views']
        ) * 100
        
        # Average watch time per view
        self.videos['avg_watch_time_per_view'] = self.videos['watch_time'] / self.videos['views']
        
        # Like-to-view ratio
        self.videos['like_to_view_ratio'] = self.videos['likes'] / self.videos['views']
        
        # Share-to-view ratio
        self.videos['share_to_view_ratio'] = self.videos['shares'] / self.videos['views']
        
        logger.info(" Derived metrics calculated")
    
    def load_to_database(self):
        """Load data to PostgreSQL database"""
        if not self.engine:
            logger.error(" No database connection available")
            return False
        
        try:
            # Load to database
            self.videos.to_sql("shortform_videos", self.engine, if_exists="replace", index=False)
            self.creators.to_sql("shortform_creators", self.engine, if_exists="replace", index=False)
            self.platforms.to_sql("shortform_platforms", self.engine, if_exists="replace", index=False)
            
            logger.info(" Data loaded successfully into PostgreSQL")
            return True
        except Exception as e:
            logger.error(f" Error loading to database: {e}")
            return False
    
    def get_data_summary(self):
        """Generate data summary statistics"""
        summary = {
            'total_videos': len(self.videos),
            'total_creators': len(self.creators),
            'total_platforms': len(self.platforms),
            'avg_views': self.videos['views'].mean(),
            'format_types': self.videos['format_type'].nunique(),
            'creator_niches': self.creators['niche'].nunique()
        }
        
        # Add retention rate if available
        if 'retention_rate' in self.videos.columns:
            summary['avg_retention_rate'] = self.videos['retention_rate'].mean()
        else:
            summary['avg_retention_rate'] = 'Not calculated'
            
        return summary

def main():
    """Main function to run the data loading process"""
    loader = ShortformDataLoader()
    
    # Load CSV data
    if not loader.load_csv_data():
        return
    
    # Validate data
    if not loader.validate_data():
        logger.warning(" Proceeding with validation issues...")
    
    # Calculate derived metrics
    loader.calculate_derived_metrics()
    
    # Connect to database
    if loader.connect_database():
        # Load to database
        loader.load_to_database()
    
    # Print summary
    summary = loader.get_data_summary()
    logger.info(" Data Summary:")
    for key, value in summary.items():
        logger.info(f"  {key}: {value}")

if __name__ == "__main__":
    main() 