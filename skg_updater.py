"""
SKG Updater - Updates configuration from analytics feedback
Uses performance data to improve production quality
"""

import json
from datetime import datetime
from typing import Dict, Any
import sys


class SKGUpdater:
    """Updates SKG configuration based on analytics feedback"""
    
    def __init__(self, skg_file: str):
        """
        Initialize updater with SKG file
        
        Args:
            skg_file: Path to SKG configuration file
        """
        self.skg_file = skg_file
        self.skg_config = self._load_skg()
    
    def _load_skg(self) -> Dict[str, Any]:
        """Load SKG configuration"""
        try:
            with open(self.skg_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ SKG file not found: {self.skg_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            sys.exit(1)
    
    def update_from_analytics(self, analytics_file: str, update_types: list):
        """
        Update SKG configuration from analytics data
        
        Args:
            analytics_file: Path to analytics JSON file
            update_types: List of update types to apply
        """
        # Load analytics data
        try:
            with open(analytics_file, 'r', encoding='utf-8') as f:
                analytics = json.load(f)
        except FileNotFoundError:
            print(f"❌ Analytics file not found: {analytics_file}")
            sys.exit(1)
        
        print(f"📊 Updating SKG from analytics...")
        
        # Apply updates
        for update_type in update_types:
            if update_type == 'voice_performance':
                self._update_voice_performance(analytics)
            elif update_type == 'listener_retention':
                self._update_listener_retention(analytics)
            elif update_type == 'engagement_metrics':
                self._update_engagement_metrics(analytics)
            elif update_type == 'mastery_score':
                self._update_mastery_score(analytics)
            else:
                print(f"⚠️  Unknown update type: {update_type}")
        
        # Save updated SKG
        self._save_skg()
        print(f"✅ SKG updated successfully")
    
    def _update_voice_performance(self, analytics: Dict[str, Any]):
        """Update voice configuration based on performance data"""
        voice_perf = analytics.get('voice_performance', {})
        
        if 'analytics_feedback' not in self.skg_config:
            self.skg_config['analytics_feedback'] = {}
        
        self.skg_config['analytics_feedback']['voice_performance'] = voice_perf
        
        # Adjust speaking rate if clarity score is low
        clarity_score = voice_perf.get('clarity_score', 100)
        if clarity_score < 70:
            current_rate = self.skg_config['voice_config']['host'].get('speaking_rate', 1.0)
            if current_rate > 0.9:
                new_rate = current_rate - 0.1
                self.skg_config['voice_config']['host']['speaking_rate'] = new_rate
                print(f"   📉 Reduced host speaking rate: {current_rate} → {new_rate} (clarity improvement)")
        
        print(f"   ✓ Voice performance updated (clarity: {clarity_score})")
    
    def _update_listener_retention(self, analytics: Dict[str, Any]):
        """Update content structure based on retention data"""
        retention = analytics.get('listener_retention', {})
        
        if 'analytics_feedback' not in self.skg_config:
            self.skg_config['analytics_feedback'] = {}
        
        self.skg_config['analytics_feedback']['listener_retention'] = retention
        
        # Identify drop-off points
        completion_rate = retention.get('average_completion_rate', 100)
        drop_off_points = retention.get('drop_off_points', [])
        
        if completion_rate < 70:
            print(f"   ⚠️  Low completion rate: {completion_rate}%")
            
            # Suggest pacing adjustments
            current_pacing = self.skg_config['tone_style'].get('pacing', 'Moderate')
            if current_pacing == 'Relaxed':
                self.skg_config['tone_style']['pacing'] = 'Moderate'
                print(f"   📈 Adjusted pacing: Relaxed → Moderate (improve retention)")
        
        if drop_off_points:
            print(f"   📍 Identified {len(drop_off_points)} drop-off points")
        
        print(f"   ✓ Listener retention updated (completion: {completion_rate}%)")
    
    def _update_engagement_metrics(self, analytics: Dict[str, Any]):
        """Update distribution strategy based on engagement"""
        engagement = analytics.get('engagement_metrics', {})
        
        if 'analytics_feedback' not in self.skg_config:
            self.skg_config['analytics_feedback'] = {}
        
        self.skg_config['analytics_feedback']['engagement_metrics'] = engagement
        
        listener_count = engagement.get('listener_count', 0)
        average_rating = engagement.get('average_rating', 0)
        share_count = engagement.get('share_count', 0)
        
        print(f"   ✓ Engagement metrics updated")
        print(f"      Listeners: {listener_count}")
        print(f"      Rating: {average_rating}/5")
        print(f"      Shares: {share_count}")
    
    def _update_mastery_score(self, analytics: Dict[str, Any]):
        """Calculate and update overall mastery score"""
        # Calculate mastery score from analytics
        voice_perf = analytics.get('voice_performance', {})
        retention = analytics.get('listener_retention', {})
        engagement = analytics.get('engagement_metrics', {})
        
        # Weighted scoring
        clarity_score = voice_perf.get('clarity_score', 0)
        naturalness_score = voice_perf.get('naturalness_score', 0)
        completion_rate = retention.get('average_completion_rate', 0)
        avg_rating = engagement.get('average_rating', 0)
        
        mastery_score = (
            clarity_score * 0.25 +
            naturalness_score * 0.25 +
            completion_rate * 0.30 +
            (avg_rating * 20) * 0.20  # Convert 5-star to 100-point scale
        )
        
        self.skg_config['metadata']['mastery_score'] = round(mastery_score, 2)
        print(f"   ✓ Mastery score updated: {mastery_score:.2f}/100")
    
    def _save_skg(self):
        """Save updated SKG configuration"""
        # Update last modified timestamp
        self.skg_config['metadata']['last_modified'] = datetime.utcnow().isoformat()
        
        # Write to file
        with open(self.skg_file, 'w', encoding='utf-8') as f:
            json.dump(self.skg_config, f, indent=2, ensure_ascii=False)


def main():
    """Command-line interface for SKG updates"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SKG Analytics Updater')
    parser.add_argument('--skg', required=True, help='Path to SKG config file')
    parser.add_argument('--analytics', required=True, help='Path to analytics JSON file')
    parser.add_argument('--update', action='append', required=True, 
                       choices=['voice_performance', 'listener_retention', 'engagement_metrics', 'mastery_score'],
                       help='Types of updates to apply (can specify multiple)')
    
    args = parser.parse_args()
    
    # Update SKG
    updater = SKGUpdater(args.skg)
    updater.update_from_analytics(args.analytics, args.update)


if __name__ == '__main__':
    main()
