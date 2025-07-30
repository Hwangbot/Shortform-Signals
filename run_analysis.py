#!/usr/bin/env python3
"""
Shortform Signals Analysis Runner

This script runs the complete analysis pipeline including data loading,
validation, analysis, and visualization generation.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from data_loader import ShortformDataLoader
from analysis import ShortformAnalyzer
import matplotlib.pyplot as plt

def main():
    """Run the complete analysis pipeline"""
    print("🚀 Starting Shortform Signals Analysis")
    print("=" * 50)
    
    # Step 1: Load and validate data
    print("\n📊 Step 1: Loading and validating data...")
    loader = ShortformDataLoader()
    
    if not loader.load_csv_data():
        print(" Failed to load data. Exiting.")
        return
    
    if not loader.validate_data():
        print(" Data validation issues found, but continuing...")
    
    loader.calculate_derived_metrics()
    
    # Step 2: Run analysis
    print("\n Step 2: Running comprehensive analysis...")
    analyzer = ShortformAnalyzer(loader.videos, loader.creators, loader.platforms)
    
    # Generate reports
    print("\n Format Performance:")
    print(analyzer.format_performance_analysis())
    
    print("\n Top Creators:")
    print(analyzer.creator_performance_ranking(10))
    
    print("\n Niche Analysis:")
    print(analyzer.niche_analysis())
    
    print("\n Duration Analysis:")
    print(analyzer.duration_analysis())
    
    print("\n Top Performing Videos:")
    print(analyzer.top_performers_analysis('retention_rate', 10))
    
    # Step 3: Generate insights
    print("\n Key Insights:")
    insights = analyzer.generate_insights_report()
    for insight in insights:
        print(f"  {insight}")
    
    # Step 4: Create visualizations
    print("\n Step 3: Generating visualizations...")
    fig = analyzer.create_visualizations()
    plt.savefig('shortform_analysis.png', dpi=300, bbox_inches='tight')
    print(" Visualizations saved as 'shortform_analysis.png'")
    
    # Step 5: Database loading (optional)
    print("\n Step 4: Loading to database (if configured)...")
    if loader.connect_database():
        if loader.load_to_database():
            print(" Data loaded to database successfully")
        else:
            print(" Failed to load data to database")
    else:
        print(" Database connection not available, skipping database load")
    
    # Final summary
    print("\n Analysis Complete!")
    print("=" * 50)
    summary = loader.get_data_summary()
    print(" Final Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\n Generated Files:")
    print("  - shortform_analysis.png (visualizations)")
    print("  - Database tables (if configured)")
    
    print("\n Next Steps:")
    print("  - Review the generated visualizations")
    print("  - Explore the Jupyter notebook for interactive analysis")
    print("  - Use the Tableau dashboard for business insights")

if __name__ == "__main__":
    main() 