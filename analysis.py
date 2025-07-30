import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

class ShortformAnalyzer:
    def __init__(self, videos_df, creators_df, platforms_df):
        self.videos = videos_df
        self.creators = creators_df
        self.platforms = platforms_df
        self.merged = None
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare merged dataset for analysis"""
        # Merge videos with creators
        self.merged = self.videos.merge(self.creators, on='creator_id', how='left')
        
        # Calculate additional metrics
        self.merged['engagement_rate'] = (
            (self.merged['likes'] + self.merged['comments'] + self.merged['shares']) / 
            self.merged['views']
        ) * 100
        
        self.merged['avg_watch_time_per_view'] = self.merged['watch_time'] / self.merged['views']
        self.merged['like_to_view_ratio'] = self.merged['likes'] / self.merged['views']
        self.merged['share_to_view_ratio'] = self.merged['shares'] / self.merged['views']
        
        # Calculate retention rate if not present
        if 'retention_rate' not in self.merged.columns:
            self.merged['retention_rate'] = self.merged['full_views'] / self.merged['views']
    
    def format_performance_analysis(self):
        """Analyze performance by content format"""
        format_stats = self.merged.groupby('format_type').agg({
            'views': ['mean', 'std'],
            'likes': ['mean', 'std'],
            'comments': ['mean', 'std'],
            'shares': ['mean', 'std'],
            'retention_rate': ['mean', 'std'],
            'engagement_rate': ['mean', 'std'],
            'hook_watch_rate': ['mean', 'std']
        }).round(2)
        
        return format_stats
    
    def creator_performance_ranking(self, top_n=10):
        """Rank creators by various performance metrics"""
        creator_stats = self.merged.groupby(['creator_name', 'niche']).agg({
            'views': 'mean',
            'likes': 'mean',
            'shares': 'mean',
            'retention_rate': 'mean',
            'engagement_rate': 'mean',
            'hook_watch_rate': 'mean'
        }).round(3)
        
        # Add follower count
        creator_stats = creator_stats.merge(
            self.creators[['creator_name', 'followers']], 
            on='creator_name', 
            how='left'
        )
        
        return creator_stats.sort_values('retention_rate', ascending=False).head(top_n)
    
    def niche_analysis(self):
        """Analyze performance by creator niche"""
        niche_stats = self.merged.groupby('niche').agg({
            'views': ['mean', 'count'],
            'likes': 'mean',
            'shares': 'mean',
            'retention_rate': 'mean',
            'engagement_rate': 'mean',
            'hook_watch_rate': 'mean'
        }).round(3)
        
        # Flatten column names for easier access
        niche_stats.columns = ['_'.join(col).strip() for col in niche_stats.columns.values]
        
        return niche_stats
    
    def duration_analysis(self):
        """Analyze the relationship between video duration and performance"""
        # Create duration bins
        self.merged['duration_bin'] = pd.cut(
            self.merged['duration_sec'], 
            bins=[0, 15, 30, 45, 60, 100], 
            labels=['0-15s', '15-30s', '30-45s', '45-60s', '60s+']
        )
        
        duration_stats = self.merged.groupby('duration_bin').agg({
            'views': 'mean',
            'retention_rate': 'mean',
            'engagement_rate': 'mean',
            'hook_watch_rate': 'mean'
        }).round(3)
        
        return duration_stats
    
    def correlation_analysis(self):
        """Analyze correlations between different metrics"""
        numeric_cols = [
            'views', 'likes', 'comments', 'shares', 'watch_time', 
            'full_views', 'retention_rate', 'hook_watch_rate',
            'engagement_rate', 'avg_watch_time_per_view',
            'like_to_view_ratio', 'share_to_view_ratio'
        ]
        
        correlation_matrix = self.merged[numeric_cols].corr()
        return correlation_matrix
    
    def performance_clustering(self, n_clusters=4):
        """Cluster videos based on performance metrics"""
        # Select features for clustering
        features = ['views', 'likes', 'shares', 'retention_rate', 'engagement_rate']
        
        # Scale the features
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(self.merged[features])
        
        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.merged['cluster'] = kmeans.fit_predict(scaled_features)
        
        # Analyze clusters
        cluster_analysis = self.merged.groupby('cluster')[features].mean().round(3)
        cluster_analysis['count'] = self.merged.groupby('cluster').size()
        
        return cluster_analysis
    
    def top_performers_analysis(self, metric='retention_rate', top_n=20):
        """Analyze top performing videos"""
        top_videos = self.merged.nlargest(top_n, metric)[
            ['video_id', 'creator_name', 'format_type', 'duration_sec', 
             'views', 'likes', 'shares', 'retention_rate', 'engagement_rate', 
             'hook_watch_rate', 'niche']
        ]
        
        return top_videos
    
    def create_visualizations(self):
        """Create comprehensive visualizations"""
        # Set style
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Shortform Video Performance Analysis', fontsize=16, fontweight='bold')
        
        # 1. Format Performance
        format_means = self.merged.groupby('format_type')['retention_rate'].mean().sort_values(ascending=False)
        axes[0, 0].bar(format_means.index, format_means.values, color='skyblue')
        axes[0, 0].set_title('Average Retention Rate by Format')
        axes[0, 0].set_ylabel('Retention Rate')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. Niche Performance
        niche_means = self.merged.groupby('niche')['engagement_rate'].mean().sort_values(ascending=False)
        axes[0, 1].bar(niche_means.index, niche_means.values, color='lightcoral')
        axes[0, 1].set_title('Average Engagement Rate by Niche')
        axes[0, 1].set_ylabel('Engagement Rate (%)')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. Duration vs Retention
        duration_stats = self.duration_analysis()
        if not duration_stats.empty and 'retention_rate' in duration_stats.columns:
            axes[0, 2].plot(duration_stats.index, duration_stats['retention_rate'], 
                           marker='o', color='green', linewidth=2)
            axes[0, 2].set_title('Retention Rate by Duration')
            axes[0, 2].set_ylabel('Retention Rate')
            axes[0, 2].tick_params(axis='x', rotation=45)
        else:
            axes[0, 2].text(0.5, 0.5, 'No duration data available', 
                           ha='center', va='center', transform=axes[0, 2].transAxes)
            axes[0, 2].set_title('Retention Rate by Duration')
        
        # 4. Views vs Engagement
        axes[1, 0].scatter(self.merged['views'], self.merged['engagement_rate'], 
                          alpha=0.6, color='purple')
        axes[1, 0].set_title('Views vs Engagement Rate')
        axes[1, 0].set_xlabel('Views')
        axes[1, 0].set_ylabel('Engagement Rate (%)')
        
        # 5. Hook Watch Rate Distribution
        axes[1, 1].hist(self.merged['hook_watch_rate'], bins=30, color='orange', alpha=0.7)
        axes[1, 1].set_title('Hook Watch Rate Distribution')
        axes[1, 1].set_xlabel('Hook Watch Rate')
        axes[1, 1].set_ylabel('Frequency')
        
        # 6. Correlation Heatmap
        corr_matrix = self.correlation_analysis()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                   ax=axes[1, 2], fmt='.2f')
        axes[1, 2].set_title('Metric Correlations')
        
        plt.tight_layout()
        return fig
    
    def generate_insights_report(self):
        """Generate a comprehensive insights report"""
        insights = []
        
        # Format insights
        format_stats = self.format_performance_analysis()
        best_format = format_stats['retention_rate']['mean'].idxmax()
        insights.append(f" **Best Performing Format**: {best_format} has the highest average retention rate")
        
        # Creator insights
        top_creators = self.creator_performance_ranking(5)
        if len(top_creators) > 0:
            top_creator_name = top_creators.index[0] if isinstance(top_creators.index[0], str) else str(top_creators.index[0])
            insights.append(f" **Top Creator**: {top_creator_name} leads in retention rate")
        else:
            insights.append(" **Top Creator**: Analysis available in detailed report")
        
        # Niche insights
        niche_stats = self.niche_analysis()
        best_niche = niche_stats['engagement_rate_mean'].idxmax()
        insights.append(f" **Most Engaging Niche**: {best_niche} generates highest engagement rates")
        
        # Duration insights
        duration_stats = self.duration_analysis()
        if not duration_stats.empty and 'retention_rate' in duration_stats.columns:
            optimal_duration = duration_stats['retention_rate'].idxmax()
            insights.append(f" **Optimal Duration**: {optimal_duration} videos perform best")
        else:
            insights.append(" **Duration Analysis**: Available in detailed report")
        
        # Correlation insights
        corr_matrix = self.correlation_analysis()
        highest_corr = corr_matrix.unstack().sort_values(ascending=False)
        if len(highest_corr) > 2:
            insights.append(f" **Strongest Correlation**: {highest_corr.index[1]} and {highest_corr.index[2]}")
        else:
            insights.append(" **Correlation Analysis**: Available in detailed analysis")
        
        return insights

def main():
    """Main function to run analysis"""
    # Load data
    videos = pd.read_csv("shortform_videos.csv")
    creators = pd.read_csv("shortform_creators.csv")
    platforms = pd.read_csv("shortform_platforms.csv")
    
    # Initialize analyzer
    analyzer = ShortformAnalyzer(videos, creators, platforms)
    
    # Run analyses
    print(" SHORTFORM VIDEO ANALYSIS REPORT")
    print("=" * 50)
    
    # Format performance
    print("\n FORMAT PERFORMANCE:")
    print(analyzer.format_performance_analysis())
    
    # Top creators
    print("\n TOP CREATORS:")
    print(analyzer.creator_performance_ranking(10))
    
    # Niche analysis
    print("\n NICHE ANALYSIS:")
    print(analyzer.niche_analysis())
    
    # Duration analysis
    print("\n DURATION ANALYSIS:")
    print(analyzer.duration_analysis())
    
    # Top performers
    print("\n TOP PERFORMING VIDEOS:")
    print(analyzer.top_performers_analysis('retention_rate', 10))
    
    # Generate insights
    print("\n KEY INSIGHTS:")
    insights = analyzer.generate_insights_report()
    for insight in insights:
        print(f"  {insight}")
    
    # Create visualizations
    fig = analyzer.create_visualizations()
    plt.savefig('shortform_analysis.png', dpi=300, bbox_inches='tight')
    print("\n Visualizations saved as 'shortform_analysis.png'")

if __name__ == "__main__":
    main() 