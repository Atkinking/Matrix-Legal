#!/usr/bin/env python3
"""
Enkel version av huvudprogrammet för testning
"""

import sys
import os
import logging
from pathlib import Path

# Lägg till src-katalogen i Python-sökvägen
sys.path.append(str(Path(__file__).parent))

# Konfigurera logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('research.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class DigitalIdentityResearch:
    """Enkel version av huvudklassen för testning"""
    
    def __init__(self, config_path="config/settings.yaml"):
        """Initiera forskningsprojektet"""
        self.config_path = config_path
        
        try:
            # Använd enkla versioner för testning
            from face_recognition.face_detector_simple import FaceDetector
            from social_media_apis.social_media_manager_simple import SocialMediaManager
            
            self.face_detector = FaceDetector()
            self.social_manager = SocialMediaManager()
            
            logger.info("Digital Identity Research projekt (enkel version) initierat")
            
        except Exception as e:
            logger.error(f"Fel vid initiering: {str(e)}")
            raise
    
    def analyze_user_identity(self, username, platforms=['twitter', 'instagram']):
        """
        Analysera en användares digitala identitet (simulerad)
        
        Args:
            username (str): Användarnamn att analysera
            platforms (list): Lista över plattformar att analysera
        
        Returns:
            dict: Analysresultat
        """
        logger.info(f"Börjar analysera användare: {username} (simulerat)")
        
        try:
            # Simulerad analys
            results = {
                'username': username,
                'platforms': platforms,
                'analysis_type': 'simulated',
                'identity_score': 0.75,
                'consistency': 0.8,
                'timestamp': '2024-01-01T12:00:00Z'
            }
            
            logger.info(f"Simulerad analys av {username} slutförd")
            return results
            
        except Exception as e:
            logger.error(f"Fel vid analys av {username}: {str(e)}")
            raise
    
    def reverse_image_search(self, image_path, platforms=['twitter', 'instagram', 'facebook']):
        """
        Utför reverse image search (simulerad)
        
        Args:
            image_path (str): Sökväg till bild att söka efter
            platforms (list): Lista över plattformar att söka på
        
        Returns:
            dict: Sökresultat
        """
        logger.info(f"Börjar reverse image search för {image_path} (simulerat)")
        
        try:
            # Simulerade sökresultat
            results = {
                'total_matches': 3,
                'platforms_searched': platforms,
                'best_match': {
                    'similarity_score': 0.85,
                    'platform': 'twitter',
                    'confidence': 0.8
                },
                'all_matches': [
                    {'platform': 'twitter', 'similarity': 0.85},
                    {'platform': 'instagram', 'similarity': 0.72},
                    {'platform': 'facebook', 'similarity': 0.68}
                ],
                'search_timestamp': '2024-01-01T12:00:00Z'
            }
            
            logger.info(f"Simulerad reverse image search slutförd för {image_path}")
            return results
            
        except Exception as e:
            logger.error(f"Fel vid reverse image search: {str(e)}")
            raise
    
    def get_search_statistics(self):
        """
        Hämta statistik över sökningar (simulerad)
        
        Returns:
            dict: Sökstatistik
        """
        return {
            'total_searches': 5,
            'total_matches': 15,
            'average_similarity': 0.75,
            'platform_distribution': {
                'twitter': 8,
                'instagram': 4,
                'facebook': 3
            }
        }

def main():
    """Huvudfunktion för enkel version"""
    print("=== Digital Identitet och Sociala Medier Forskning ===")
    print("(Enkel version för testning)")
    print("Välkommen till forskningsverktyget för digital identitet!")
    print()
    
    try:
        # Initiera forskningsprojektet
        research = DigitalIdentityResearch()
        
        # Exempel på användning
        print("Exempel på användning:")
        print("1. Analysera en enskild användare")
        print("2. Reverse Image Search")
        print("3. Visa statistik")
        print("4. Avsluta")
        print()
        
        # Interaktiv meny
        choice = input("Välj alternativ (1-4): ")
        
        if choice == "1":
            username = input("Ange användarnamn: ")
            platforms = input("Ange plattformar (kommaseparerade): ").split(',')
            platforms = [p.strip() for p in platforms]
            
            try:
                results = research.analyze_user_identity(username, platforms)
                print(f"Analys slutförd för {username}")
                print(f"Identitetspoäng: {results['identity_score']}")
                print(f"Konsistens: {results['consistency']}")
            except Exception as e:
                print(f"Fel: {str(e)}")
        
        elif choice == "2":
            image_path = input("Ange sökväg till bild: ")
            platforms = input("Ange plattformar (kommaseparerade): ").split(',')
            platforms = [p.strip() for p in platforms]
            
            try:
                results = research.reverse_image_search(image_path, platforms)
                print(f"Reverse image search slutförd")
                print(f"Totalt antal matchningar: {results['total_matches']}")
                
                best_match = results['best_match']
                print(f"Bästa matchning: {best_match['similarity_score']:.2f} similaritet")
                print(f"Plattform: {best_match['platform']}")
            except Exception as e:
                print(f"Fel: {str(e)}")
        
        elif choice == "3":
            try:
                stats = research.get_search_statistics()
                print("Statistik:")
                print(f"- Totalt antal sökningar: {stats['total_searches']}")
                print(f"- Totalt antal matchningar: {stats['total_matches']}")
                print(f"- Genomsnittlig similaritet: {stats['average_similarity']:.2f}")
                print(f"- Plattformsfördelning: {stats['platform_distribution']}")
            except Exception as e:
                print(f"Fel: {str(e)}")
        
        elif choice == "4":
            print("Tack för att du använde forskningsverktyget!")
        
        else:
            print("Ogiltigt val")
    
    except Exception as e:
        print(f"Kritiskt fel: {str(e)}")
        print("Kontrollera att alla filer finns på rätt plats")

if __name__ == "__main__":
    main()
