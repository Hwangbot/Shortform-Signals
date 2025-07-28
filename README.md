# Shortform Signals Dashboard

## Overview

This project analyzes engagement and retention metrics across shortform videos from platforms like TikTok, YouTube Shorts, and Instagram Reels. The analysis is visualized using an interactive Tableau dashboard that helps uncover trends across formats, creators, and content types.

## Datasets

- **shortform_videos_large.csv**  
  Contains 1,000 video records with fields for views, likes, shares, comments, full views, watch time, and hook effectiveness.

- **shortform_creators_large.csv**  
  Includes 50 shortform creators with metadata such as follower counts and content niche.

- **shortform_platforms_large.csv**  
  Compares platform-level metrics like user base, session length, and algorithm behavior.

## Key Metrics Visualized

-  **Retention Rate** — Percentage of full views vs. total views.
-  **Engagement by Format** — Comparing memes, tutorials, duets, stories, and reactions.
-  **Creator Impact** — Average engagement and retention by creator.
-  **Hook Effectiveness** — Performance in the first few seconds of content.
-  **Watch Time vs. Retention** — Correlation and clustering of performance metrics.

## Tools

- **Tableau** (Public or Desktop)
- **Python & Pandas** for data preparation

## Instructions

1. Open Tableau and load `shortform_videos.csv` as the primary data source.
2. Add `shortform_creators.csv` and `shortform_platforms.csv` as joins.
3. Use joins on `creator_id` and optionally tag platform fields.
4. Create sheets for each key metric and assemble them into a dashboard.
5. Apply filters, color coding, and sorting for clarity and interactivity.

## Optional

To automate preprocessing or build additional visualizations, refer to the Python notebook version of the project.
