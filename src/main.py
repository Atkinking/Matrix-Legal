#!/usr/bin/env python3
"""
Huvudprogram för Digital Identitet och Sociala Medier Forskning
Med Reverse Image Search funktionalitet
"""

import sys
import os
import logging
from pathlib import Path

# Lägg till src-katalogen i Python-sökvägen
sys.path.append(str(Path(__file__).parent))

try:
    from face_recognition.face_detector import FaceDetector
    from face_recognition.reverse_image_search import ReverseImageSearch
    from social_media_apis.social_media_manager import SocialMediaManager
    from analysis.identity_analyzer import IdentityAnalyzer
    from data_processing.data_manager import DataManager
    from data_processing.search_manager import SearchManager
    from visualization.report_generator import ReportGenerator
except ImportError as e:
    print(f"Import fel: {e}")
    print("Kontrollera att alla moduler finns i rätt kataloger")
    sys.exit(1)

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
    """Huvudklass för forskningsprojektet med Reverse Image Search"""
    
    def __init__(self, config_path="config/settings.yaml"):
        """Initiera forskningsprojektet"""
        self.config_path = config_path
        
        try:
            self.face_detector = FaceDetector()
            self.social_manager = SocialMediaManager()
            self.analyzer = IdentityAnalyzer()
            self.data_manager = DataManager()
            self.search_manager = SearchManager()
            self.report_generator = ReportGenerator()
            
            # Initiera reverse image search
            self.reverse_search = ReverseImageSearch(
                self.face_detector, 
                self.social_manager, 
                self.data_manager
            )
            
            logger.info("Digital Identity Research projekt med Reverse Image Search initierat")
            
        except Exception as e:
            logger.error(f"Fel vid initiering: {str(e)}")
            raise
    
    def analyze_user_identity(self, username, platforms=['twitter', 'instagram']):
        """
        Analysera en användares digitala identitet
        
        Args:
            username (str): Användarnamn att analysera
            platforms (list): Lista över plattformar att analysera
        
        Returns:
            dict: Analysresultat
        """
        logger.info(f"Börjar analysera användare: {username}")
        
        try:
            # Hämta data från sociala medier
            social_data = {}
            for platform in platforms:
                logger.info(f"Hämtar data från {platform}")
                data = self.social_manager.get_user_data(username, platform)
                social_data[platform] = data
            
            # Analysera ansiktsdrag
            face_features = {}
            for platform, data in social_data.items():
                if 'images' in data:
                    logger.info(f"Analyserar ansiktsdrag från {platform}")
                    features = self.face_detector.analyze_images(data['images'])
                    face_features[platform] = features
                    
                    # Lägg till ansikten i sökindex
                    self._index_faces_for_search(features, platform, username)
            
            # Kombinera och analysera data
            logger.info("Kombinerar och analyserar data")
            analysis_results = self.analyzer.analyze_identity_patterns(
                social_data, face_features
            )
            
            # Spara resultat
            self.data_manager.save_analysis_results(username, analysis_results)
            
            # Generera rapport
            report = self.report_generator.generate_report(analysis_results)
            
            logger.info(f"Analys av {username} slutförd")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Fel vid analys av {username}: {str(e)}")
            raise
    
    def reverse_image_search(self, image_path, platforms=['twitter', 'instagram', 'facebook']):
        """
        Utför reverse image search
        
        Args:
            image_path (str): Sökväg till bild att söka efter
            platforms (list): Lista över plattformar att söka på
        
        Returns:
            dict: Sökresultat
        """
        logger.info(f"Börjar reverse image search för {image_path}")
        
        try:
            # Kontrollera att bilden finns
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Bildfil finns inte: {image_path}")
            
            # Utför sökning
            search_results = self.reverse_search.search_face_in_social_media(
                image_path, platforms
            )
            
            logger.info(f"Reverse image search slutförd för {image_path}")
            return search_results
            
        except Exception as e:
            logger.error(f"Fel vid reverse image search: {str(e)}")
            raise
    
    def batch_analysis(self, usernames, platforms=['twitter', 'instagram']):
        """
        Analysera flera användare i batch
        
        Args:
            usernames (list): Lista över användarnamn
            platforms (list): Lista över plattformar
        
        Returns:
            dict: Sammanställda resultat
        """
        logger.info(f"Börjar batch-analys av {len(usernames)} användare")
        
        results = {}
        for username in usernames:
            try:
                result = self.analyze_user_identity(username, platforms)
                results[username] = result
            except Exception as e:
                logger.error(f"Fel vid analys av {username}: {str(e)}")
                results[username] = {'error': str(e)}
        
        # Generera sammanställd rapport
        summary_report = self.report_generator.generate_summary_report(results)
        
        logger.info("Batch-analys slutförd")
        return results, summary_report
    
    def _index_faces_for_search(self, face_features, platform, username):
        """
        Indexera ansikten för reverse image search
        
        Args:
            face_features (dict): Ansiktsdrag
            platform (str): Plattform
            username (str): Användarnamn
        """
        try:
            faces = face_features.get('faces', [])
            for face in faces:
                face_id = f"{platform}_{username}_{face.get('face_id', 0)}"
                encoding = face.get('encoding', [])
                quality_score = face.get('confidence', 0.5)
                
                self.search_manager.add_face_to_index(
                    face_id, platform, username, encoding, quality_score
                )
            
            logger.info(f"Indexerade {len(faces)} ansikten för {username} på {platform}")
            
        except Exception as e:
            logger.error(f"Fel vid indexering av ansikten: {str(e)}")
    
    def get_search_history(self, limit=10):
        """
        Hämta sökhistorik
        
        Args:
            limit (int): Max antal sökningar
        
        Returns:
            list: Sökhistorik
        """
        return self.reverse_search.get_search_history(limit)
    
    def get_search_statistics(self):
        """
        Hämta statistik över sökningar
        
        Returns:
            dict: Sökstatistik
        """
        return self.search_manager.get_search_statistics()
    
    def export_results(self, output_format='json'):
        """
        Exportera resultat i olika format
        
        Args:
            output_format (str): Format att exportera till ('json', 'csv', 'html')
        """
        logger.info(f"Exporterar resultat i {output_format} format")
        
        if output_format == 'json':
            return self.data_manager.export_to_json()
        elif output_format == 'csv':
            return self.data_manager.export_to_csv()
        elif output_format == 'html':
            return self.report_generator.export_to_html()
        else:
            raise ValueError(f"Okänt format: {output_format}")

def main():
    """Huvudfunktion med Reverse Image Search"""
    print("=== Digital Identitet och Sociala Medier Forskning ===")
    print("Med Reverse Image Search funktionalitet")
    print("Välkommen till forskningsverktyget för digital identitet!")
    print()
    
    try:
        # Initiera forskningsprojektet
        research = DigitalIdentityResearch()
        
        # Exempel på användning
        print("Exempel på användning:")
        print("1. Analysera en enskild användare")
        print("2. Batch-analys av flera användare")
        print("3. Reverse Image Search")
        print("4. Visa sökhistorik")
        print("5. Exportera resultat")
        print()
        
        # Interaktiv meny
        choice = input("Välj alternativ (1-5): ")
        
        if choice == "1":
            username = input("Ange användarnamn: ")
            platforms = input("Ange plattformar (kommaseparerade): ").split(',')
            platforms = [p.strip() for p in platforms]
            
            try:
                results = research.analyze_user_identity(username, platforms)
                print(f"Analys slutförd för {username}")
                print(f"Resultat sparade i data/results/")
            except Exception as e:
                print(f"Fel: {str(e)}")
        
        elif choice == "2":
            usernames = input("Ange användarnamn (kommaseparerade): ").split(',')
            usernames = [u.strip() for u in usernames]
            platforms = input("Ange plattformar (kommaseparerade): ").split(',')
            platforms = [p.strip() for p in platforms]
            
            try:
                results, summary = research.batch_analysis(usernames, platforms)
                print(f"Batch-analys slutförd för {len(usernames)} användare")
            except Exception as e:
                print(f"Fel: {str(e)}")
        
        elif choice == "3":
            image_path = input("Ange sökväg till bild: ")
            platforms = input("Ange plattformar (kommaseparerade): ").split(',')
            platforms = [p.strip() for p in platforms]
            
            try:
                results = research.reverse_image_search(image_path, platforms)
                print(f"Reverse image search slutförd")
                print(f"Totalt antal matchningar: {results.get('total_matches', 0)}")
                
                best_match = results.get('best_overall_match')
                if best_match:
                    print(f"Bästa matchning: {best_match.get('similarity_score', 0):.2f} similaritet")
                    print(f"Plattform: {best_match.get('platform', 'Okänd')}")
            except Exception as e:
                print(f"Fel: {str(e)}")
        
        elif choice == "4":
            try:
                history = research.get_search_history()
                print("Sökhistorik:")
                for search in history:
                    print(f"- {search['search_id']}: {search['total_matches']} matchningar")
            except Exception as e:
                print(f"Fel: {str(e)}")
        
        elif choice == "5":
            format_choice = input("Välj format (json/csv/html): ")
            try:
                research.export_results(format_choice)
                print(f"Resultat exporterade i {format_choice} format")
            except Exception as e:
                print(f"Fel: {str(e)}")
        
        else:
            print("Ogiltigt val")
    
    except Exception as e:
        print(f"Kritiskt fel: {str(e)}")
        print("Kontrollera att alla beroenden är installerade")

if __name__ == "__main__":
    main()
