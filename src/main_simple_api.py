#!/usr/bin/env python3
"""
Enkel version av Digital Identitetsforskning utan externa API:er
Fokuserar på lokal analys och simulering
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
import sqlite3

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
    """Enkel version utan externa API:er"""
    
    def __init__(self, config_path="config/settings.yaml"):
        """Initiera forskningsprojektet"""
        self.config_path = config_path
        self.data = {}
        self.search_history = []
        self.db_path = "data/research.db"
        
        # Skapa data-mappar
        os.makedirs("data/raw", exist_ok=True)
        os.makedirs("data/processed", exist_ok=True)
        os.makedirs("data/results", exist_ok=True)
        os.makedirs("data/export", exist_ok=True)
        
        # Initiera databas
        self._init_database()
        
        logger.info("Digital Identity Research projekt initierat (enkel version)")
    
    def _init_database(self):
        """Initiera SQLite-databas"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Skapa tabeller
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    analysis_type TEXT,
                    results_json TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_path TEXT,
                    search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    results_json TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("Databas initierad")
            
        except Exception as e:
            logger.error(f"Fel vid initiering av databas: {str(e)}")
    
    def analyze_user_identity(self, username, platforms=['twitter', 'instagram']):
        """
        Analysera en användares digitala identitet (simulerad)
        
        Args:
            username (str): Användarnamn att analysera
            platforms (list): Lista över plattformar att analysera
        
        Returns:
            dict: Analysresultat
        """
        logger.info(f"Börjar analysera användare: {username}")
        
        try:
            # Simulerad datahämtning (ingen extern API)
            social_data = self._simulate_social_data(username, platforms)
            
            # Simulerad ansiktsanalys
            face_features = self._simulate_face_analysis(social_data)
            
            # Analysera identitetsmönster
            analysis_results = self._analyze_identity_patterns(social_data, face_features)
            
            # Spara i databas
            self._save_to_database(username, analysis_results)
            
            logger.info(f"Analys av {username} slutförd")
            return analysis_results
            
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
        logger.info(f"Börjar reverse image search för {image_path}")
        
        try:
            # Simulera reverse image search
            search_results = self._simulate_reverse_search(image_path, platforms)
            
            # Spara sökresultat
            self._save_search_to_database(image_path, search_results)
            
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
        Hämta sökhistorik från databas
        
        Args:
            limit (int): Max antal sökningar
        
        Returns:
            list: Sökhistorik
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT image_path, search_timestamp, results_json
                FROM search_history 
                ORDER BY search_timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            history = []
            for row in cursor.fetchall():
                image_path, timestamp, results_json = row
                results = json.loads(results_json) if results_json else {}
                history.append({
                    'image_path': image_path,
                    'timestamp': timestamp,
                    'total_matches': results.get('total_matches', 0),
                    'best_similarity': results.get('best_overall_match', {}).get('similarity_score', 0)
                })
            
            conn.close()
            return history
            
        except Exception as e:
            logger.error(f"Fel vid hämtning av sökhistorik: {str(e)}")
            return []
    
    def get_statistics(self):
        """
        Hämta statistik från databas
        
        Returns:
            dict: Statistik
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Räkna användare
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            # Räkna analyser
            cursor.execute("SELECT COUNT(*) FROM analysis_results")
            analysis_count = cursor.fetchone()[0]
            
            # Räkna sökningar
            cursor.execute("SELECT COUNT(*) FROM search_history")
            search_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_users': user_count,
                'total_analyses': analysis_count,
                'total_searches': search_count,
                'database_size': os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
            }
            
        except Exception as e:
            logger.error(f"Fel vid hämtning av statistik: {str(e)}")
            return {'error': str(e)}
    
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
    
    def _simulate_social_data(self, username, platforms):
        """Simulera social media data"""
        social_data = {}
        
        for platform in platforms:
            # Simulera användardata
            social_data[platform] = {
                'platform': platform,
                'username': username,
                'user_info': {
                    'username': username,
                    'display_name': f"@{username}",
                    'followers_count': np.random.randint(100, 10000),
                    'following_count': np.random.randint(50, 5000),
                    'verified': np.random.choice([True, False], p=[0.1, 0.9]),
                    'created_at': '2020-01-01T00:00:00Z'
                },
                'images': [
                    {
                        'url': f'https://example.com/{username}_{platform}_{i}.jpg',
                        'timestamp': datetime.now().isoformat(),
                        'type': 'profile' if i == 0 else 'post'
                    } for i in range(np.random.randint(1, 6))
                ],
                'posts': [
                    {
                        'id': f'{platform}_{i}',
                        'text': f'Sample post {i} from {username}',
                        'timestamp': datetime.now().isoformat(),
                        'likes': np.random.randint(0, 1000),
                        'shares': np.random.randint(0, 100)
                    } for i in range(np.random.randint(5, 20))
                ],
                'timestamp': datetime.now().isoformat()
            }
        
        return social_data
    
    def _simulate_face_analysis(self, social_data):
        """Simulera ansiktsanalys"""
        face_features = {}
        
        for platform, data in social_data.items():
            images = data.get('images', [])
            if not images:
                continue
            
            # Simulera ansiktsdetektering
            faces = []
            for i, image in enumerate(images):
                # Simulera ansiktsencoding (128 dimensioner)
                encoding = np.random.rand(128).tolist()
                
                face = {
                    'face_id': i,
                    'location': {
                        'top': np.random.randint(50, 200),
                        'right': np.random.randint(200, 400),
                        'bottom': np.random.randint(250, 400),
                        'left': np.random.randint(50, 200)
                    },
                    'encoding': encoding,
                    'confidence': np.random.uniform(0.7, 0.95),
                    'image_path': image['url'],
                    'quality_score': np.random.uniform(0.6, 0.9)
                }
                faces.append(face)
            
            # Analysera ansiktsmönster
            if faces:
                encodings = np.array([f['encoding'] for f in faces])
                consistency_score = 1.0 - np.std(encodings).mean()  # Högre = mer konsekvent
                
                face_features[platform] = {
                    'total_images': len(images),
                    'total_faces': len(faces),
                    'faces': faces,
                    'analysis': {
                        'consistency_score': max(0, min(1, consistency_score)),
                        'quality_metrics': {
                            'average_confidence': np.mean([f['confidence'] for f in faces]),
                            'high_quality_count': sum(1 for f in faces if f['confidence'] > 0.8),
                            'average_quality_score': np.mean([f['quality_score'] for f in faces])
                        },
                        'face_angle_analysis': {
                            'front_facing': np.random.uniform(0.6, 0.9),
                            'side_profile': np.random.uniform(0.1, 0.4)
                        }
                    }
                }
        
        return face_features
    
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
                'image_quality': {
                    'average_quality': np.random.uniform(0.6, 0.9),
                    'high_quality_ratio': np.random.uniform(0.3, 0.8)
                },
                'posting_frequency': np.random.uniform(0.2, 0.8),
                'engagement_rate': np.random.uniform(0.1, 0.5)
            }
        
        # Analysera tidsmönster
        temporal_patterns = {}
        for platform in social_data.keys():
            temporal_patterns[platform] = {
                'posting_frequency': np.random.uniform(0.2, 0.8),
                'peak_activity_hours': sorted(np.random.choice(range(24), 3, replace=False).tolist()),
                'seasonal_patterns': {
                    'spring': np.random.uniform(0.7, 1.2),
                    'summer': np.random.uniform(0.8, 1.3),
                    'autumn': np.random.uniform(0.6, 1.1),
                    'winter': np.random.uniform(0.5, 1.0)
                },
                'consistency_score': np.random.uniform(0.4, 0.9)
            }
        
        # Analysera innehållsmönster
        content_patterns = {}
        for platform in social_data.keys():
            content_patterns[platform] = {
                'image_types': {
                    'selfie': np.random.uniform(0.2, 0.6),
                    'group_photo': np.random.uniform(0.1, 0.4),
                    'landscape': np.random.uniform(0.1, 0.3),
                    'food': np.random.uniform(0.05, 0.2),
                    'other': np.random.uniform(0.1, 0.4)
                },
                'content_themes': np.random.choice([
                    'personal', 'professional', 'lifestyle', 'travel', 'food', 'fitness'
                ], 3, replace=False).tolist(),
                'diversity_score': np.random.uniform(0.4, 0.8),
                'visual_style': {
                    'color_palette': np.random.choice(['warm', 'cool', 'neutral']),
                    'brightness': np.random.choice(['high', 'medium', 'low']),
                    'filter_usage': np.random.uniform(0.1, 0.6)
                }
            }
        
        return {
            'username': list(social_data.keys())[0] if social_data else 'unknown',
            'platforms': list(social_data.keys()),
            'overall_identity_score': identity_score,
            'face_consistency': {
                'overall_consistency': overall_consistency,
                'platform_consistency': face_consistency,
                'cross_platform_comparison': self._compare_platforms(face_consistency)
            },
            'platform_representation': platform_representation,
            'temporal_patterns': temporal_patterns,
            'content_patterns': content_patterns,
            'insights': self._generate_insights(identity_score, overall_consistency, platform_representation),
            'recommendations': self._generate_recommendations(identity_score, overall_consistency),
            'timestamp': datetime.now().isoformat()
        }
    
    def _compare_platforms(self, face_consistency):
        """Jämför ansiktskonsistens mellan plattformar"""
        platforms = list(face_consistency.keys())
        comparisons = {}
        
        for i, platform1 in enumerate(platforms):
            for platform2 in platforms[i+1:]:
                key = f"{platform1}_vs_{platform2}"
                consistency1 = face_consistency.get(platform1, 0)
                consistency2 = face_consistency.get(platform2, 0)
                
                comparisons[key] = {
                    'similarity': 1.0 - abs(consistency1 - consistency2),
                    'consistency1': consistency1,
                    'consistency2': consistency2,
                    'difference': abs(consistency1 - consistency2)
                }
        
        return comparisons
    
    def _generate_insights(self, identity_score, consistency, platform_rep):
        """Generera insikter från analys"""
        insights = []
        
        if identity_score > 0.8:
            insights.append("Hög identitetspoäng - stark digital identitet")
        elif identity_score < 0.5:
            insights.append("Låg identitetspoäng - möjlig identitetsutveckling")
        
        if consistency > 0.8:
            insights.append("Hög ansiktskonsistens över plattformar")
        elif consistency < 0.4:
            insights.append("Låg ansiktskonsistens - varierande presentation")
        
        if len(platform_rep) > 2:
            insights.append(f"Aktiv på {len(platform_rep)} plattformar")
        
        return insights
    
    def _generate_recommendations(self, identity_score, consistency):
        """Generera rekommendationer"""
        recommendations = []
        
        if identity_score < 0.6:
            recommendations.append("Fokusera på att skapa en mer konsekvent digital identitet")
        
        if consistency < 0.5:
            recommendations.append("Överväg att använda liknande bilder över plattformar")
        
        if not recommendations:
            recommendations.append("Bra identitetskonsistens - fortsätt som vanligt")
        
        return recommendations
    
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
                    'image_url': f"https://example.com/{platform}_match_{np.random.randint(1, 10)}.jpg",
                    'timestamp': datetime.now().isoformat()
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
                    f'Matchningar hittades på {len(set(m["platform"] for m in matches))} plattformar' if matches else 'Inga matchningar'
                ],
                'recommendation': 'Hög sannolikhet för matchning - rekommenderar manuell verifiering' if matches and matches[0]['similarity_score'] > 0.8 else 'Möjlig matchning - rekommenderar ytterligare analys'
            },
            'search_timestamp': datetime.now().isoformat()
        }
    
    def _save_to_database(self, username, results):
        """Spara analysresultat i databas"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Hitta eller skapa användare
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_result = cursor.fetchone()
            
            if user_result:
                user_id = user_result[0]
            else:
                cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
                user_id = cursor.lastrowid
            
            # Spara analysresultat
            results_json = json.dumps(results, ensure_ascii=False)
            cursor.execute('''
                INSERT INTO analysis_results (user_id, analysis_type, results_json)
                VALUES (?, ?, ?)
            ''', (user_id, 'identity_analysis', results_json))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Sparade analysresultat för {username}")
            
        except Exception as e:
            logger.error(f"Fel vid sparande av analysresultat: {str(e)}")
    
    def _save_search_to_database(self, image_path, results):
        """Spara sökresultat i databas"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            results_json = json.dumps(results, ensure_ascii=False)
            cursor.execute('''
                INSERT INTO search_history (image_path, results_json)
                VALUES (?, ?)
            ''', (image_path, results_json))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Sparade sökresultat för {image_path}")
            
        except Exception as e:
            logger.error(f"Fel vid sparande av sökresultat: {str(e)}")
    
    def _generate_summary_report(self, results):
        """Generera sammanfattningsrapport"""
        successful_analyses = [r for r in results.values() if 'error' not in r]
        
        return {
            'total_users': len(results),
            'successful_analyses': len(successful_analyses),
            'average_identity_score': np.mean([r.get('overall_identity_score', 0) for r in successful_analyses]) if successful_analyses else 0,
            'average_consistency': np.mean([r.get('face_consistency', {}).get('overall_consistency', 0) for r in successful_analyses]) if successful_analyses else 0,
            'platform_distribution': self._calculate_platform_distribution(results),
            'insights': [
                f'Analyserade {len(successful_analyses)} av {len(results)} användare',
                f'Genomsnittlig identitetspoäng: {np.mean([r.get("overall_identity_score", 0) for r in successful_analyses]):.2f}' if successful_analyses else 'Inga framgångsrika analyser',
                f'Genomsnittlig konsistens: {np.mean([r.get("face_consistency", {}).get("overall_consistency", 0) for r in successful_analyses]):.2f}' if successful_analyses else 'Inga framgångsrika analyser'
            ]
        }
    
    def _calculate_platform_distribution(self, results):
        """Beräkna plattformsfördelning"""
        platform_counts = {}
        for username, data in results.items():
            if 'error' not in data:
                for platform in data.get('platforms', []):
                    platform_counts[platform] = platform_counts.get(platform, 0) + 1
        return platform_counts
    
    def _export_to_json(self):
        """Exportera som JSON"""
        output_path = "data/export/results.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Resultat exporterade till {output_path}")
        return output_path
    
    def _export_to_csv(self):
        """Exportera som CSV"""
        output_path = "data/export/results.csv"
        
        # Hämta data från databas
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM analysis_results", conn)
            conn.close()
            
            df.to_csv(output_path, index=False, encoding='utf-8')
            logger.info(f"Resultat exporterade till {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Fel vid CSV-export: {str(e)}")
            return None
    
    def _export_to_html(self):
        """Exportera som HTML"""
        output_path = "data/export/results.html"
        
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
                    <p>Konsistens: {data.get('face_consistency', {}).get('overall_consistency', 0):.2f}</p>
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
    print("(Enkel version utan externa API:er)")
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
                print(f"\nInsikter:")
                for insight in results['insights']:
                    print(f"- {insight}")
                print(f"\nRekommendationer:")
                for rec in results['recommendations']:
                    print(f"- {rec}")
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
                print(f"Genomsnittlig konsistens: {summary['average_consistency']:.2f}")
                print(f"Plattformsfördelning: {summary['platform_distribution']}")
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
                stats = research.get_statistics()
                print(f"\nStatistik:")
                print(f"- Totalt antal användare: {stats['total_users']}")
                print(f"- Totalt antal analyser: {stats['total_analyses']}")
                print(f"- Totalt antal sökningar: {stats['total_searches']}")
                print(f"- Databasstorlek: {stats['database_size']} bytes")
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
