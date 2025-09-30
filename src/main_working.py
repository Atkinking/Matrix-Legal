#!/usr/bin/env python3
"""
Fungerande version av huvudprogrammet för Digital Identitetsforskning
"""

import sys
import os
import logging
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json

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
    """Fungerande version av forskningsprojektet"""
    
    def __init__(self, config_path="config/settings.yaml"):
        """Initiera forskningsprojektet"""
        self.config_path = config_path
        self.data = {}
        self.search_history = []
        
        logger.info("Digital Identity Research projekt initierat")
    
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
            # Simulerad datahämtning från sociala medier
            social_data = {}
            for platform in platforms:
                logger.info(f"Hämtar data från {platform}")
                data = self._get_simulated_social_data(username, platform)
                social_data[platform] = data
            
            # Simulerad ansiktsanalys
            face_features = {}
            for platform, data in social_data.items():
                logger.info(f"Analyserar ansiktsdrag från {platform}")
                features = self._simulate_face_analysis(data)
                face_features[platform] = features
            
            # Analysera identitetsmönster
            logger.info("Kombinerar och analyserar data")
            analysis_results = self._analyze_identity_patterns(social_data, face_features)
            
            # Spara resultat
            self._save_analysis_results(username, analysis_results)
            
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
                logger.warning(f"Bildfil finns inte: {image_path} - använder simulerad data")
            
            # Simulera reverse image search
            search_results = self._simulate_reverse_search(image_path, platforms)
            
            # Spara sökresultat
            self._save_search_results(image_path, search_results)
            
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
        summary_report = self._generate_summary_report(results)
        
        logger.info("Batch-analys slutförd")
        return results, summary_report
    
    def get_search_history(self, limit=10):
        """
        Hämta sökhistorik
        
        Args:
            limit (int): Max antal sökningar
        
        Returns:
            list: Sökhistorik
        """
        return self.search_history[-limit:] if self.search_history else []
    
    def get_search_statistics(self):
        """
        Hämta statistik över sökningar
        
        Returns:
            dict: Sökstatistik
        """
        return {
            'total_searches': len(self.search_history),
            'total_matches': sum(search.get('total_matches', 0) for search in self.search_history),
            'average_similarity': np.mean([search.get('best_similarity', 0) for search in self.search_history]) if self.search_history else 0,
            'platform_distribution': self._calculate_platform_distribution()
        }
    
    def export_results(self, output_format='json'):
        """
        Exportera resultat i olika format
        
        Args:
            output_format (str): Format att exportera till ('json', 'csv', 'html')
        """
        logger.info(f"Exporterar resultat i {output_format} format")
        
        if output_format == 'json':
            return self._export_to_json()
        elif output_format == 'csv':
            return self._export_to_csv()
        elif output_format == 'html':
            return self._export_to_html()
        else:
            raise ValueError(f"Okänt format: {output_format}")
    
    def _get_simulated_social_data(self, username, platform):
        """Simulera social media data"""
        return {
            'platform': platform,
            'username': username,
            'user_info': {
                'username': username,
                'display_name': f"@{username}",
                'followers_count': np.random.randint(100, 10000),
                'following_count': np.random.randint(50, 5000),
                'verified': np.random.choice([True, False], p=[0.1, 0.9])
            },
            'images': [
                {
                    'url': f'https://example.com/{username}_profile_{i}.jpg',
                    'timestamp': datetime.now().isoformat(),
                    'type': 'profile'
                } for i in range(np.random.randint(1, 5))
            ],
            'timestamp': datetime.now().isoformat()
        }
    
    def _simulate_face_analysis(self, data):
        """Simulera ansiktsanalys"""
        num_images = len(data.get('images', []))
        if num_images == 0:
            return {'total_faces': 0, 'faces': [], 'analysis': {}}
        
        faces = []
        for i in range(num_images):
            face = {
                'face_id': i,
                'location': {
                    'top': np.random.randint(50, 200),
                    'right': np.random.randint(200, 400),
                    'bottom': np.random.randint(250, 400),
                    'left': np.random.randint(50, 200)
                },
                'encoding': np.random.rand(128).tolist(),  # Simulerad 128-dimensionell encoding
                'confidence': np.random.uniform(0.7, 0.95),
                'image_path': data['images'][i]['url']
            }
            faces.append(face)
        
        return {
            'total_images': num_images,
            'total_faces': len(faces),
            'faces': faces,
            'analysis': {
                'consistency_score': np.random.uniform(0.6, 0.9),
                'quality_metrics': {
                    'average_confidence': np.mean([f['confidence'] for f in faces]),
                    'high_quality_count': sum(1 for f in faces if f['confidence'] > 0.8)
                }
            }
        }
    
    def _analyze_identity_patterns(self, social_data, face_features):
        """Analysera identitetsmönster"""
        # Beräkna identitetspoäng
        identity_score = np.random.uniform(0.5, 0.9)
        
        # Analysera ansiktskonsistens
        face_consistency = {}
        for platform, features in face_features.items():
            if 'analysis' in features:
                face_consistency[platform] = features['analysis'].get('consistency_score', 0)
        
        overall_consistency = np.mean(list(face_consistency.values())) if face_consistency else 0
        
        # Analysera plattformsrepresentation
        platform_representation = {}
        for platform, data in social_data.items():
            platform_representation[platform] = {
                'activity_level': np.random.uniform(0.3, 0.9),
                'profile_completeness': np.random.uniform(0.5, 1.0),
                'image_quality': {'average_quality': np.random.uniform(0.6, 0.9)}
            }
        
        return {
            'username': list(social_data.keys())[0] if social_data else 'unknown',
            'platforms': list(social_data.keys()),
            'overall_identity_score': identity_score,
            'face_consistency': {
                'overall_consistency': overall_consistency,
                'platform_consistency': face_consistency
            },
            'platform_representation': platform_representation,
            'temporal_patterns': {
                p: {
                    'posting_frequency': np.random.uniform(0.2, 0.8),
                    'peak_activity_hours': np.random.choice(range(24), 3, replace=False).tolist(),
                    'seasonal_patterns': {
                        'spring': np.random.uniform(0.7, 1.2),
                        'summer': np.random.uniform(0.8, 1.3),
                        'autumn': np.random.uniform(0.6, 1.1),
                        'winter': np.random.uniform(0.5, 1.0)
                    }
                } for p in social_data.keys()
            },
            'content_patterns': {
                p: {
                    'image_types': {
                        'selfie': np.random.uniform(0.2, 0.6),
                        'group_photo': np.random.uniform(0.1, 0.4),
                        'landscape': np.random.uniform(0.1, 0.3),
                        'other': np.random.uniform(0.1, 0.4)
                    },
                    'content_themes': np.random.choice(['personal', 'professional', 'lifestyle', 'travel'], 2, replace=False).tolist(),
                    'diversity_score': np.random.uniform(0.4, 0.8)
                } for p in social_data.keys()
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def _simulate_reverse_search(self, image_path, platforms):
        """Simulera reverse image search"""
        # Simulera matchningar
        matches = []
        for platform in platforms:
            similarity = np.random.uniform(0.3, 0.9)
            if similarity > 0.6:  # Bara visa matchningar över tröskelvärdet
                match = {
                    'platform': platform,
                    'similarity_score': similarity,
                    'match_confidence': similarity * np.random.uniform(0.8, 1.0),
                    'user_id': f"user_{np.random.randint(1, 100)}",
                    'image_url': f"https://example.com/{platform}_match_{np.random.randint(1, 10)}.jpg"
                }
                matches.append(match)
        
        # Sortera efter similaritet
        matches.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return {
            'total_matches': len(matches),
            'platforms_searched': platforms,
            'best_overall_match': matches[0] if matches else None,
            'all_matches': matches,
            'analysis': {
                'average_similarity': np.mean([m['similarity_score'] for m in matches]) if matches else 0,
                'max_similarity': max([m['similarity_score'] for m in matches]) if matches else 0,
                'platform_distribution': {p: sum(1 for m in matches if m['platform'] == p) for p in platforms},
                'insights': [
                    'Hög sannolikhet för identisk person' if matches and matches[0]['similarity_score'] > 0.8 else 'Möjlig matchning',
                    f'Matchningar hittades på {len(set(m["platform"] for m in matches))} plattformar'
                ],
                'recommendation': 'Hög sannolikhet för matchning - rekommenderar manuell verifiering' if matches and matches[0]['similarity_score'] > 0.8 else 'Möjlig matchning - rekommenderar ytterligare analys'
            },
            'search_timestamp': datetime.now().isoformat()
        }
    
    def _save_analysis_results(self, username, results):
        """Spara analysresultat"""
        self.data[username] = results
        logger.info(f"Sparade analysresultat för {username}")
    
    def _save_search_results(self, image_path, results):
        """Spara sökresultat"""
        search_entry = {
            'image_path': image_path,
            'timestamp': datetime.now().isoformat(),
            'total_matches': results['total_matches'],
            'best_similarity': results['best_overall_match']['similarity_score'] if results['best_overall_match'] else 0
        }
        self.search_history.append(search_entry)
        logger.info(f"Sparade sökresultat för {image_path}")
    
    def _generate_summary_report(self, results):
        """Generera sammanfattningsrapport"""
        successful_analyses = [r for r in results.values() if 'error' not in r]
        
        return {
            'total_users': len(results),
            'successful_analyses': len(successful_analyses),
            'average_identity_score': np.mean([r.get('overall_identity_score', 0) for r in successful_analyses]) if successful_analyses else 0,
            'platform_distribution': self._calculate_platform_distribution(),
            'insights': [
                f'Analyserade {len(successful_analyses)} av {len(results)} användare',
                f'Genomsnittlig identitetspoäng: {np.mean([r.get("overall_identity_score", 0) for r in successful_analyses]):.2f}' if successful_analyses else 'Inga framgångsrika analyser'
            ]
        }
    
    def _calculate_platform_distribution(self):
        """Beräkna plattformsfördelning"""
        platform_counts = {}
        for username, data in self.data.items():
            for platform in data.get('platforms', []):
                platform_counts[platform] = platform_counts.get(platform, 0) + 1
        return platform_counts
    
    def _export_to_json(self):
        """Exportera som JSON"""
        output_path = "data/export/results.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Resultat exporterade till {output_path}")
        return output_path
    
    def _export_to_csv(self):
        """Exportera som CSV"""
        output_path = "data/export/results.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Skapa DataFrame från data
        rows = []
        for username, data in self.data.items():
            row = {
                'username': username,
                'platforms': ', '.join(data.get('platforms', [])),
                'identity_score': data.get('overall_identity_score', 0),
                'timestamp': data.get('timestamp', '')
            }
            rows.append(row)
        
        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False, encoding='utf-8')
        
        logger.info(f"Resultat exporterade till {output_path}")
        return output_path
    
    def _export_to_html(self):
        """Exportera som HTML"""
        output_path = "data/export/results.html"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="sv">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Digital Identitetsanalys - Rapport</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .section {{ margin: 20px 0; }}
                .metric {{ background-color: #e8f4f8; padding: 10px; margin: 10px 0; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Digital Identitetsanalys</h1>
                <p>Rapport genererad: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
            
            <div class="section">
                <h2>Sammanfattning</h2>
                <p>Totalt antal användare analyserade: {len(self.data)}</p>
                <p>Totalt antal sökningar: {len(self.search_history)}</p>
            </div>
            
            <div class="section">
                <h2>Användaranalys</h2>
        """
        
        for username, data in self.data.items():
            html_content += f"""
                <div class="metric">
                    <h3>{username}</h3>
                    <p>Plattformar: {', '.join(data.get('platforms', []))}</p>
                    <p>Identitetspoäng: {data.get('overall_identity_score', 0):.2f}</p>
                </div>
            """
        
        html_content += """
            </div>
        </body>
        </html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Resultat exporterade till {output_path}")
        return output_path

def main():
    """Huvudfunktion"""
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
        print("5. Visa statistik")
        print("6. Exportera resultat")
        print("7. Avsluta")
        print()
        
        # Interaktiv meny
        choice = input("Välj alternativ (1-7): ")
        
        if choice == "1":
            username = input("Ange användarnamn: ")
            platforms = input("Ange plattformar (kommaseparerade): ").split(',')
            platforms = [p.strip() for p in platforms]
            
            try:
                results = research.analyze_user_identity(username, platforms)
                print(f"\nAnalys slutförd för {username}")
                print(f"Identitetspoäng: {results['overall_identity_score']:.2f}")
                print(f"Ansiktskonsistens: {results['face_consistency']['overall_consistency']:.2f}")
                print(f"Plattformar: {', '.join(results['platforms'])}")
            except Exception as e:
                print(f"Fel: {str(e)}")
        
        elif choice == "2":
            usernames = input("Ange användarnamn (kommaseparerade): ").split(',')
            usernames = [u.strip() for u in usernames]
            platforms = input("Ange plattformar (kommaseparerade): ").split(',')
            platforms = [p.strip() for p in platforms]
            
            try:
                results, summary = research.batch_analysis(usernames, platforms)
                print(f"\nBatch-analys slutförd för {len(usernames)} användare")
                print(f"Framgångsrika analyser: {summary['successful_analyses']}")
                print(f"Genomsnittlig identitetspoäng: {summary['average_identity_score']:.2f}")
            except Exception as e:
                print(f"Fel: {str(e)}")
        
        elif choice == "3":
            image_path = input("Ange sökväg till bild: ")
            platforms = input("Ange plattformar (kommaseparerade): ").split(',')
            platforms = [p.strip() for p in platforms]
            
            try:
                results = research.reverse_image_search(image_path, platforms)
                print(f"\nReverse image search slutförd")
                print(f"Totalt antal matchningar: {results['total_matches']}")
                
                if results['best_overall_match']:
                    best = results['best_overall_match']
                    print(f"Bästa matchning: {best['similarity_score']:.2f} similaritet")
                    print(f"Plattform: {best['platform']}")
                    print(f"Konfidens: {best['match_confidence']:.2f}")
                
                print(f"\nInsikter:")
                for insight in results['analysis']['insights']:
                    print(f"- {insight}")
                print(f"Rekommendation: {results['analysis']['recommendation']}")
                
            except Exception as e:
                print(f"Fel: {str(e)}")
        
        elif choice == "4":
            try:
                history = research.get_search_history()
                print(f"\nSökhistorik ({len(history)} sökningar):")
                for i, search in enumerate(history, 1):
                    print(f"{i}. {search['image_path']}: {search['total_matches']} matchningar, {search['best_similarity']:.2f} similaritet")
            except Exception as e:
                print(f"Fel: {str(e)}")
        
        elif choice == "5":
            try:
                stats = research.get_search_statistics()
                print(f"\nStatistik:")
                print(f"- Totalt antal sökningar: {stats['total_searches']}")
                print(f"- Totalt antal matchningar: {stats['total_matches']}")
                print(f"- Genomsnittlig similaritet: {stats['average_similarity']:.2f}")
                print(f"- Plattformsfördelning: {stats['platform_distribution']}")
            except Exception as e:
                print(f"Fel: {str(e)}")
        
        elif choice == "6":
            format_choice = input("Välj format (json/csv/html): ")
            try:
                output_path = research.export_results(format_choice)
                print(f"Resultat exporterade till: {output_path}")
            except Exception as e:
                print(f"Fel: {str(e)}")
        
        elif choice == "7":
            print("Tack för att du använde forskningsverktyget!")
        
        else:
            print("Ogiltigt val")
    
    except Exception as e:
        print(f"Kritiskt fel: {str(e)}")

if __name__ == "__main__":
    main()
