"""
Social Media API Manager för digital identitetsforskning
"""

import requests
import json
import logging
from typing import Dict, List, Optional
import os
from pathlib import Path
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class SocialMediaManager:
    """Huvudklass för hantering av sociala medier APIs"""
    
    def __init__(self, config_path: str = "config/api_keys.json"):
        """
        Initiera social media manager
        
        Args:
            config_path (str): Sökväg till API-nycklar
        """
        self.config_path = config_path
        self.api_keys = self._load_api_keys()
        self.rate_limits = {
            'twitter': {'calls': 0, 'reset_time': None},
            'instagram': {'calls': 0, 'reset_time': None},
            'facebook': {'calls': 0, 'reset_time': None}
        }
        
        logger.info("SocialMediaManager initierad")
    
    def _load_api_keys(self) -> Dict:
        """Ladda API-nycklar från konfigurationsfil"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            else:
                logger.warning(f"API-nycklar inte hittade i {self.config_path}")
                return {}
        except Exception as e:
            logger.error(f"Fel vid laddning av API-nycklar: {str(e)}")
            return {}
    
    def get_user_data(self, username: str, platform: str) -> Dict:
        """
        Hämta användardata från specifik plattform
        
        Args:
            username (str): Användarnamn
            platform (str): Plattform ('twitter', 'instagram', 'facebook')
        
        Returns:
            Dict: Användardata
        """
        logger.info(f"Hämtar data för {username} från {platform}")
        
        if platform == 'twitter':
            return self._get_twitter_data(username)
        elif platform == 'instagram':
            return self._get_instagram_data(username)
        elif platform == 'facebook':
            return self._get_facebook_data(username)
        else:
            raise ValueError(f"Okänd plattform: {platform}")
    
    def _get_twitter_data(self, username: str) -> Dict:
        """Hämta data från Twitter"""
        try:
            # Kontrollera rate limit
            if not self._check_rate_limit('twitter'):
                logger.warning("Twitter rate limit nådd, väntar...")
                time.sleep(60)
            
            # Hämta användarinformation
            user_info = self._get_twitter_user_info(username)
            
            # Hämta tweets med bilder
            tweets_with_images = self._get_twitter_images(username)
            
            # Hämta profilbilder
            profile_images = self._get_twitter_profile_images(username)
            
            return {
                'platform': 'twitter',
                'username': username,
                'user_info': user_info,
                'images': tweets_with_images + profile_images,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Fel vid hämtning av Twitter-data: {str(e)}")
            return {'error': str(e)}
    
    def _get_instagram_data(self, username: str) -> Dict:
        """Hämta data från Instagram"""
        try:
            # Kontrollera rate limit
            if not self._check_rate_limit('instagram'):
                logger.warning("Instagram rate limit nådd, väntar...")
                time.sleep(60)
            
            # Hämta användarinformation
            user_info = self._get_instagram_user_info(username)
            
            # Hämta posts med bilder
            posts_with_images = self._get_instagram_posts(username)
            
            # Hämta profilbilder
            profile_images = self._get_instagram_profile_images(username)
            
            return {
                'platform': 'instagram',
                'username': username,
                'user_info': user_info,
                'images': posts_with_images + profile_images,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Fel vid hämtning av Instagram-data: {str(e)}")
            return {'error': str(e)}
    
    def _get_facebook_data(self, username: str) -> Dict:
        """Hämta data från Facebook"""
        try:
            # Kontrollera rate limit
            if not self._check_rate_limit('facebook'):
                logger.warning("Facebook rate limit nådd, väntar...")
                time.sleep(60)
            
            # Hämta användarinformation
            user_info = self._get_facebook_user_info(username)
            
            # Hämta posts med bilder
            posts_with_images = self._get_facebook_posts(username)
            
            # Hämta profilbilder
            profile_images = self._get_facebook_profile_images(username)
            
            return {
                'platform': 'facebook',
                'username': username,
                'user_info': user_info,
                'images': posts_with_images + profile_images,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Fel vid hämtning av Facebook-data: {str(e)}")
            return {'error': str(e)}
    
    def _get_twitter_user_info(self, username: str) -> Dict:
        """Hämta Twitter-användarinformation"""
        # Simulerad implementation - ersätt med riktig Twitter API
        return {
            'id': f"twitter_{username}",
            'username': username,
            'display_name': f"@{username}",
            'followers_count': 0,
            'following_count': 0,
            'tweet_count': 0,
            'verified': False,
            'created_at': '2020-01-01T00:00:00Z'
        }
    
    def _get_twitter_images(self, username: str) -> List[Dict]:
        """Hämta bilder från Twitter tweets"""
        # Simulerad implementation
        return []
    
    def _get_twitter_profile_images(self, username: str) -> List[Dict]:
        """Hämta profilbilder från Twitter"""
        # Simulerad implementation
        return []
    
    def _get_instagram_user_info(self, username: str) -> Dict:
        """Hämta Instagram-användarinformation"""
        # Simulerad implementation
        return {
            'id': f"instagram_{username}",
            'username': username,
            'full_name': username,
            'followers_count': 0,
            'following_count': 0,
            'media_count': 0,
            'is_private': False,
            'is_verified': False
        }
    
    def _get_instagram_posts(self, username: str) -> List[Dict]:
        """Hämta Instagram posts med bilder"""
        # Simulerad implementation
        return []
    
    def _get_instagram_profile_images(self, username: str) -> List[Dict]:
        """Hämta profilbilder från Instagram"""
        # Simulerad implementation
        return []
    
    def _get_facebook_user_info(self, username: str) -> Dict:
        """Hämta Facebook-användarinformation"""
        # Simulerad implementation
        return {
            'id': f"facebook_{username}",
            'username': username,
            'name': username,
            'friends_count': 0,
            'likes_count': 0,
            'is_verified': False
        }
    
    def _get_facebook_posts(self, username: str) -> List[Dict]:
        """Hämta Facebook posts med bilder"""
        # Simulerad implementation
        return []
    
    def _get_facebook_profile_images(self, username: str) -> List[Dict]:
        """Hämta profilbilder från Facebook"""
        # Simulerad implementation
        return []
    
    def _check_rate_limit(self, platform: str) -> bool:
        """
        Kontrollera om rate limit är nådd
        
        Args:
            platform (str): Plattform att kontrollera
        
        Returns:
            bool: True om API-anrop tillåts
        """
        if platform not in self.rate_limits:
            return True
        
        current_time = datetime.now()
        rate_limit = self.rate_limits[platform]
        
        # Reset rate limit om tiden har gått
        if rate_limit['reset_time'] and current_time > rate_limit['reset_time']:
            rate_limit['calls'] = 0
            rate_limit['reset_time'] = None
        
        # Kontrollera om vi har nått gränsen
        if rate_limit['calls'] >= 100:  # Exempelgräns
            return False
        
        # Öka räknare
        rate_limit['calls'] += 1
        if rate_limit['calls'] == 1:
            rate_limit['reset_time'] = current_time + timedelta(hours=1)
        
        return True
    
    def download_image(self, image_url: str, save_path: str) -> bool:
        """
        Ladda ner bild från URL
        
        Args:
            image_url (str): URL till bilden
            save_path (str): Sökväg att spara bilden till
        
        Returns:
            bool: True om nedladdning lyckades
        """
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Skapa mapp om den inte finns
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Spara bild
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Laddade ner bild: {save_path}")
            return True
            
        except Exception as e:
            logger.error(f"Fel vid nedladdning av bild {image_url}: {str(e)}")
            return False
    
    def batch_download_images(self, image_urls: List[str], base_path: str) -> List[str]:
        """
        Ladda ner flera bilder i batch
        
        Args:
            image_urls (List[str]): Lista över bild-URLs
            base_path (str): Basmapp för nedladdning
        
        Returns:
            List[str]: Lista över nedladdade filer
        """
        downloaded_files = []
        
        for i, url in enumerate(image_urls):
            filename = f"image_{i:04d}.jpg"
            save_path = os.path.join(base_path, filename)
            
            if self.download_image(url, save_path):
                downloaded_files.append(save_path)
            
            # Paus mellan nedladdningar för att undvika rate limiting
            time.sleep(1)
        
        logger.info(f"Nedladdade {len(downloaded_files)} av {len(image_urls)} bilder")
        return downloaded_files
    
    def get_platform_statistics(self) -> Dict:
        """
        Hämta statistik för alla plattformar
        
        Returns:
            Dict: Plattformsstatistik
        """
        stats = {}
        
        for platform, rate_limit in self.rate_limits.items():
            stats[platform] = {
                'calls_made': rate_limit['calls'],
                'reset_time': rate_limit['reset_time'],
                'api_available': platform in self.api_keys
            }
        
        return stats
    
    def reset_rate_limits(self):
        """Återställ alla rate limits"""
        for platform in self.rate_limits:
            self.rate_limits[platform]['calls'] = 0
            self.rate_limits[platform]['reset_time'] = None
        
        logger.info("Rate limits återställda")
