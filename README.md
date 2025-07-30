# Shortform Signals Dashboard

## Overview

This project analyzes engagement and retention metrics across shortform videos from platforms like TikTok, YouTube Shorts, and Instagram Reels. The analysis is visualized using an interactive Tableau dashboard and comprehensive Python analytics that help uncover trends across formats, creators, and content types.

## Features

- **Comprehensive Data Analysis**: Advanced analytics with clustering, correlation analysis, and performance ranking
- **Interactive Visualizations**: Both static matplotlib plots and interactive Plotly charts
- **Data Validation**: Robust data quality checks and error handling
- **Database Integration**: PostgreSQL support with automated data loading
- **Modular Architecture**: Clean, maintainable code structure

## Datasets

- **shortform_videos.csv**  
  Contains 1,000 video records with fields for views, likes, shares, comments, full views, watch time, and hook effectiveness.

- **shortform_creators.csv**  
  Includes 50 shortform creators with metadata such as follower counts and content niche.

- **shortform_platforms.csv**  
  Compares platform-level metrics like user base, session length, and algorithm behavior.

## Key Metrics Analyzed

- **Retention Rate** — Percentage of full views vs. total views
- **Engagement Rate** — Combined likes, comments, and shares relative to views
- **Hook Effectiveness** — Performance in the first few seconds of content
- **Format Performance** — Comparing memes, tutorials, duets, stories, and reactions
- **Creator Impact** — Average engagement and retention by creator
- **Niche Analysis** — Performance across different content categories
- **Duration Optimization** — Relationship between video length and performance
- **Performance Clustering** — Grouping videos by similar performance patterns

## Tools & Technologies

- **Python 3.8+** with pandas, numpy, matplotlib, seaborn, plotly
- **Scikit-learn** for machine learning analysis
- **SQLAlchemy** for database operations
- **PostgreSQL** for data storage
- **Tableau** for interactive dashboards
- **Jupyter Notebooks** for exploratory analysis

## Project Structure

```
Shortform Signals/
├──  shortform_videos.csv          # Main video dataset
├──  shortform_creators.csv        # Creator information
├──  shortform_platforms.csv       # Platform metrics
├──  analysis.py                   # Comprehensive analysis module
├──  data_loader.py                # Data loading and validation
├──  config.py                     # Configuration settings
├──  requirements.txt              # Python dependencies
├──  README.md                     # Project documentation
├──  Notebook/
│   └── shortform_analysis.ipynb     # Jupyter notebook
├──  Database/                     # Database files (if using local DB)
└──  Tableau Insights.twbx         # Tableau dashboard
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database (Optional)

Edit `config.py` to set your PostgreSQL connection details:

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'shortform_signals',
    'user': 'your_username',
    'password': 'your_password'
}
```

### 3. Load and Analyze Data

```bash
# Load data with validation
python data_loader.py

# Run comprehensive analysis
python analysis.py
```

### 4. Explore with Jupyter

```bash
jupyter notebook Notebook/shortform_analysis.ipynb
```

## Analysis Capabilities

### Basic Analytics

- Format performance comparison
- Creator ranking by retention rate
- Niche-based engagement analysis
- Duration optimization insights

### Advanced Analytics

- **Correlation Analysis**: Identify relationships between metrics
- **Performance Clustering**: Group similar-performing videos
- **Top Performer Analysis**: Identify best-performing content
- **Hook Effectiveness**: Analyze opening performance

### Visualizations

- Interactive performance dashboards
- Correlation heatmaps
- Distribution plots
- Comparative bar charts
- Scatter plots for metric relationships

## Key Insights

The analysis reveals several important patterns:

1. **Format Impact**: Story format videos show highest retention rates
2. **Creator Influence**: Top creators consistently outperform in retention
3. **Niche Performance**: Different niches excel in different metrics
4. **Duration Sweet Spot**: Optimal video length varies by content type
5. **Engagement Patterns**: Strong correlation between hook performance and overall success

## Tableau Dashboard Setup

1. Open Tableau and load `shortform_videos.csv` as the primary data source
2. Add `shortform_creators.csv` and `shortform_platforms.csv` as joins
3. Use joins on `creator_id` and optionally tag platform fields
4. Create sheets for each key metric and assemble them into a dashboard
5. Apply filters, color coding, and sorting for clarity and interactivity

## Data Quality

The project includes comprehensive data validation:

- Missing value detection
- Duplicate record identification
- Range validation for metrics
- Consistency checks across datasets

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note**: This project is designed for educational and analytical purposes. Ensure compliance with data privacy regulations when working with real user data.
