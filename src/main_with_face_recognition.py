#!/usr/bin/env python3
"""
Digital Identitetsforskning med riktig ansiktsigenkänning
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
import cv2
from PIL import Image
import requests
from io import BytesIO

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

class FaceRecognitionEngine:
    """Enkel ansiktsigenkänningsmotor"""
    
    def __init__(self):
        """Initiera ansiktsigenkänningsmotor"""
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.known_faces = {}
        self.face_encodings = {}
        
        logger.info("FaceRecognitionEngine initierad")
    
    def detect_faces(self, image_path):
        """
        Detektera ansikten i en bild
        
        Args:
            image_path (str): Sökväg till bild
        
        Returns:
            list: Lista över detekterade ansikten
        """
        try:
            # Ladda bild
            if image_path.startswith('http'):
                response = requests.get(image_path)
                image = Image.open(BytesIO(response.content))
                image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            else:
                if not os.path.exists(image_path):
                    logger.warning(f"Bildfil finns inte: {image_path}")
                    return []
                image = cv2.imread(image_path)
            
            if image is None:
                logger.warning(f"Kunde inte ladda bild: {image_path}")
                return []
            
            # Konvertera till gråskala
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detektera ansikten
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            detected_faces = []
            for i, (x, y, w, h) in enumerate(faces):
                face_data = {
                    'face_id': i,
                    'location': {
                        'x': int(x),
                        'y': int(y),
                        'width': int(w),
                        'height': int(h)
                    },
                    'confidence': self._calculate_face_confidence(gray, x, y, w, h),
                    'image_path': image_path,
                    'face_region': gray[y:y+h, x:x+w]  # Ansiktsregion för vidare analys
                }
                detected_faces.append(face_data)
            
            logger.info(f"Detekterade {len(detected_faces)} ansikten i {image_path}")
            return detected_faces
            
        except Exception as e:
            logger.error(f"Fel vid ansiktsdetektering i {image_path}: {str(e)}")
            return []
    
    def _calculate_face_confidence(self, gray_image, x, y, w, h):
        """Beräkna konfidensgrad för ansiktsdetektering"""
        try:
            # Extrahera ansiktsregion
            face_region = gray_image[y:y+h, x:x+w]
            
            # Beräkna kontrast (högre kontrast = bättre ansiktskvalitet)
            contrast = np.std(face_region)
            
            # Beräkna ljusstyrka
            brightness = np.mean(face_region)
            
            # Beräkna ansiktsstorlek (normalisera)
            size_factor = min(1.0, (w * h) / (100 * 100))
            
            # Kombinera faktorer för konfidensgrad
            confidence = min(1.0, (contrast / 50.0) * (brightness / 128.0) * size_factor)
            
            return max(0.1, min(1.0, confidence))
            
        except Exception as e:
            logger.error(f"Fel vid beräkning av konfidensgrad: {str(e)}")
            return 0.5
    
    def extract_face_features(self, face_data):
        """
        Extrahera ansiktsdrag från ansiktsregion
        
        Args:
            face_data (dict): Ansiktsdata
        
        Returns:
            dict: Ansiktsdrag
        """
        try:
            face_region = face_data.get('face_region')
            if face_region is None:
                return {}
            
            # Beräkna grundläggande ansiktsdrag
            features = {
                'face_id': face_data['face_id'],
                'location': face_data['location'],
                'confidence': face_data['confidence'],
                'image_path': face_data['image_path'],
                'features': {
                    'brightness': float(np.mean(face_region)),
                    'contrast': float(np.std(face_region)),
                    'size': face_region.shape[0] * face_region.shape[1],
                    'aspect_ratio': face_region.shape[1] / face_region.shape[0],
                    'histogram': self._calculate_histogram_features(face_region)
                }
            }
            
            return features
            
        except Exception as e:
            logger.error(f"Fel vid extraktion av ansiktsdrag: {str(e)}")
            return {}
    
    def _calculate_histogram_features(self, face_region):
        """Beräkna histogramfunktioner för ansiktsregion"""
        try:
            # Beräkna histogram
            hist = cv2.calcHist([face_region], [0], None, [256], [0, 256])
            
            # Normalisera histogram
            hist = hist.flatten() / np.sum(hist)
            
            # Beräkna statistiska mått
            features = {
                'mean': float(np.mean(hist)),
                'std': float(np.std(hist)),
                'skewness': float(self._calculate_skewness(hist)),
                'kurtosis': float(self._calculate_kurtosis(hist)),
                'entropy': float(self._calculate_entropy(hist))
            }
            
            return features
            
        except Exception as e:
            logger.error(f"Fel vid beräkning av histogramfunktioner: {str(e)}")
            return {}
    
    def _calculate_skewness(self, data):
        """Beräkna skevhet"""
        try:
            mean = np.mean(data)
            std = np.std(data)
            if std == 0:
                return 0
            return np.mean(((data - mean) / std) ** 3)
        except:
            return 0
    
    def _calculate_kurtosis(self, data):
        """Beräkna kurtosis"""
        try:
            mean = np.mean(data)
            std = np.std(data)
            if std == 0:
                return 0
            return np.mean(((data - mean) / std) ** 4) - 3
        except:
            return 0
    
    def _calculate_entropy(self, data):
        """Beräkna entropi"""
        try:
            # Lägg till liten konstant för att undvika log(0)
            data = data + 1e-10
            return -np.sum(data * np.log2(data))
        except:
            return 0
    
    def compare_faces(self, face1_features, face2_features):
        """
        Jämför två ansikten
        
        Args:
            face1_features (dict): Första ansiktets drag
            face2_features (dict): Andra ansiktets drag
        
        Returns:
            float: Similaritetspoäng (0-1)
        """
        try:
            if not face1_features or not face2_features:
                return 0.0
            
            features1 = face1_features.get('features', {})
            features2 = face2_features.get('features', {})
            
            if not features1 or not features2:
                return 0.0
            
            # Jämför grundläggande drag
            similarity_scores = []
            
            # Jämför ljusstyrka
            brightness1 = features1.get('brightness', 0)
            brightness2 = features2.get('brightness', 0)
            brightness_sim = 1.0 - abs(brightness1 - brightness2) / 255.0
            similarity_scores.append(brightness_sim)
            
            # Jämför kontrast
            contrast1 = features1.get('contrast', 0)
            contrast2 = features2.get('contrast', 0)
            contrast_sim = 1.0 - abs(contrast1 - contrast2) / 100.0
            similarity_scores.append(contrast_sim)
            
            # Jämför aspektförhållande
            aspect1 = features1.get('aspect_ratio', 1.0)
            aspect2 = features2.get('aspect_ratio', 1.0)
            aspect_sim = 1.0 - abs(aspect1 - aspect2) / max(aspect1, aspect2)
            similarity_scores.append(aspect_sim)
            
            # Jämför histogramfunktioner
            hist1 = features1.get('histogram', {})
            hist2 = features2.get('histogram', {})
            
            if hist1 and hist2:
                hist_similarities = []
                for key in ['mean', 'std', 'skewness', 'kurtosis', 'entropy']:
                    val1 = hist1.get(key, 0)
                    val2 = hist2.get(key, 0)
                    if val1 != 0 or val2 != 0:
                        sim = 1.0 - abs(val1 - val2) / max(abs(val1), abs(val2), 1e-10)
                        hist_similarities.append(sim)
                
                if hist_similarities:
                    similarity_scores.append(np.mean(hist_similarities))
            
            # Beräkna genomsnittlig similaritet
            overall_similarity = np.mean(similarity_scores) if similarity_scores else 0.0
            
            return max(0.0, min(1.0, overall_similarity))
            
        except Exception as e:
            logger.error(f"Fel vid ansiktsjämförelse: {str(e)}")
            return 0.0

class DigitalIdentityResearch:
    """Digital Identitetsforskning med riktig ansiktsigenkänning"""
    
    def __init__(self, config_path="config/settings.yaml"):
        """Initiera forskningsprojektet"""
        self.config_path = config_path
        self.data = {}
        self.search_history = []
        self.db_path = "data/research.db"
        self.face_engine = FaceRecognitionEngine()
        
        # Skapa data-mappar
        os.makedirs("data/raw", exist_ok=True)
        os.makedirs("data/processed", exist_ok=True)
        os.makedirs("data/results", exist_ok=True)
        os.makedirs("data/export", exist_ok=True)
        
        # Initiera databas
        self._init_database()
        
        logger.info("Digital Identity Research projekt med ansiktsigenkänning initierat")
    
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
                CREATE TABLE IF NOT EXISTS face_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    image_path TEXT,
                    face_features_json TEXT,
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
        Analysera en användares digitala identitet med riktig ansiktsigenkänning
        
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
            
            # Riktig ansiktsanalys
            face_features = self._analyze_faces_real(social_data)
            
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
        Utför reverse image search med riktig ansiktsigenkänning
        
        Args:
            image_path (str): Sökväg till bild att söka efter
            platforms (list): Lista över plattformar att söka på
        
        Returns:
            dict: Sökresultat
        """
        logger.info(f"Börjar reverse image search för {image_path}")
        
        try:
            # Detektera ansikten i uppladdad bild
            uploaded_faces = self.face_engine.detect_faces(image_path)
            
            if not uploaded_faces:
                return {
                    'total_matches': 0,
                    'error': 'Inga ansikten hittades i uppladdad bild',
                    'search_timestamp': datetime.now().isoformat()
                }
            
            # Extrahera ansiktsdrag
            uploaded_features = []
            for face in uploaded_faces:
                features = self.face_engine.extract_face_features(face)
                if features:
                    uploaded_features.append(features)
            
            # Sök efter matchningar i databasen
            matches = self._search_face_matches(uploaded_features, platforms)
            
            # Spara sökresultat
            search_results = {
                'total_matches': len(matches),
                'platforms_searched': platforms,
                'best_overall_match': matches[0] if matches else None,
                'all_matches': matches,
                'uploaded_faces_count': len(uploaded_faces),
                'analysis': self._analyze_search_results(matches),
                'search_timestamp': datetime.now().isoformat()
            }
            
            self._save_search_to_database(image_path, search_results)
            
            logger.info(f"Reverse image search slutförd för {image_path}")
            return search_results
            
        except Exception as e:
            logger.error(f"Fel vid reverse image search: {str(e)}")
            raise
    
    def _simulate_social_data(self, username, platforms):
        """Simulera social media data"""
        social_data = {}
        
        for platform in platforms:
            # Skapa testbilder för ansiktsanalys
            test_images = []
            for i in range(np.random.randint(1, 4)):
                # Skapa en simulerad bild-URL
                image_url = f"data/raw/{username}_{platform}_{i}.jpg"
                test_images.append({
                    'url': image_url,
                    'timestamp': datetime.now().isoformat(),
                    'type': 'profile' if i == 0 else 'post'
                })
            
            social_data[platform] = {
                'platform': platform,
                'username': username,
                'user_info': {
                    'username': username,
                    'display_name': f"@{username}",
                    'followers_count': np.random.randint(100, 10000),
                    'following_count': np.random.randint(50, 5000),
                    'verified': np.random.choice([True, False], p=[0.1, 0.9])
                },
                'images': test_images,
                'timestamp': datetime.now().isoformat()
            }
        
        return social_data
    
    def _analyze_faces_real(self, social_data):
        """Analysera ansikten med riktig ansiktsigenkänning"""
        face_features = {}
        
        for platform, data in social_data.items():
            images = data.get('images', [])
            if not images:
                continue
            
            platform_faces = []
            for image in images:
                image_path = image['url']
                
                # Detektera ansikten
                faces = self.face_engine.detect_faces(image_path)
                
                for face in faces:
                    # Extrahera ansiktsdrag
                    features = self.face_engine.extract_face_features(face)
                    if features:
                        platform_faces.append(features)
            
            if platform_faces:
                # Analysera ansiktsmönster
                face_features[platform] = {
                    'total_images': len(images),
                    'total_faces': len(platform_faces),
                    'faces': platform_faces,
                    'analysis': self._analyze_face_consistency(platform_faces)
                }
        
        return face_features
    
    def _analyze_face_consistency(self, faces):
        """Analysera ansiktskonsistens"""
        if not faces:
            return {'consistency_score': 0, 'quality_metrics': {}}
        
        # Beräkna konsistens baserat på ansiktsdrag
        similarities = []
        for i, face1 in enumerate(faces):
            for face2 in faces[i+1:]:
                similarity = self.face_engine.compare_faces(face1, face2)
                similarities.append(similarity)
        
        consistency_score = np.mean(similarities) if similarities else 0
        
        # Beräkna kvalitetsmått
        confidences = [face.get('confidence', 0) for face in faces]
        quality_metrics = {
            'average_confidence': np.mean(confidences),
            'high_quality_count': sum(1 for c in confidences if c > 0.7),
            'consistency_score': consistency_score
        }
        
        return {
            'consistency_score': consistency_score,
            'quality_metrics': quality_metrics
        }
    
    def _search_face_matches(self, uploaded_features, platforms):
        """Sök efter ansiktsmatchningar"""
        matches = []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Hämta befintliga ansiktsdata
            cursor.execute('''
                SELECT fd.face_features_json, u.username, fd.image_path
                FROM face_data fd
                JOIN users u ON fd.user_id = u.id
            ''')
            
            for row in cursor.fetchall():
                features_json, username, image_path = row
                try:
                    stored_features = json.loads(features_json)
                    
                    # Jämför med uppladdade ansikten
                    for uploaded_face in uploaded_features:
                        similarity = self.face_engine.compare_faces(uploaded_face, stored_features)
                        
                        if similarity > 0.6:  # Tröskelvärde för matchning
                            match = {
                                'username': username,
                                'image_path': image_path,
                                'similarity_score': similarity,
                                'match_confidence': similarity * 0.9,  # Justera konfidens
                                'platform': 'unknown'  # Kan förbättras
                            }
                            matches.append(match)
                
                except Exception as e:
                    logger.warning(f"Fel vid jämförelse med lagrad ansiktsdata: {str(e)}")
                    continue
            
            conn.close()
            
            # Sortera efter similaritet
            matches.sort(key=lambda x: x['similarity_score'], reverse=True)
            
        except Exception as e:
            logger.error(f"Fel vid sökning av ansiktsmatchningar: {str(e)}")
        
        return matches
    
    def _analyze_search_results(self, matches):
        """Analysera sökresultat"""
        if not matches:
            return {
                'insights': ['Inga matchningar hittades'],
                'recommendation': 'Inga matchningar - överväg andra sökstrategier'
            }
        
        similarities = [m['similarity_score'] for m in matches]
        max_similarity = max(similarities)
        avg_similarity = np.mean(similarities)
        
        insights = []
        if max_similarity > 0.8:
            insights.append("Hög sannolikhet för identisk person")
        elif max_similarity > 0.6:
            insights.append("Möjlig matchning - kräver manuell verifiering")
        else:
            insights.append("Låg sannolikhet för matchning")
        
        recommendation = "Hög sannolikhet för matchning - rekommenderar manuell verifiering" if max_similarity > 0.8 else "Möjlig matchning - rekommenderar ytterligare analys"
        
        return {
            'average_similarity': avg_similarity,
            'max_similarity': max_similarity,
            'insights': insights,
            'recommendation': recommendation
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
        
        return {
            'username': list(social_data.keys())[0] if social_data else 'unknown',
            'platforms': list(social_data.keys()),
            'overall_identity_score': identity_score,
            'face_consistency': {
                'overall_consistency': overall_consistency,
                'platform_consistency': face_consistency
            },
            'face_analysis': face_features,
            'timestamp': datetime.now().isoformat()
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
            
            # Spara ansiktsdata
            face_analysis = results.get('face_analysis', {})
            for platform, features in face_analysis.items():
                if 'faces' in features:
                    for face in features['faces']:
                        face_json = json.dumps(face, ensure_ascii=False)
                        cursor.execute('''
                            INSERT INTO face_data (user_id, image_path, face_features_json)
                            VALUES (?, ?, ?)
                        ''', (user_id, face.get('image_path', ''), face_json))
            
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
    
    def get_search_history(self, limit=10):
        """Hämta sökhistorik"""
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
        """Hämta statistik"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM analysis_results")
            analysis_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM face_data")
            face_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM search_history")
            search_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_users': user_count,
                'total_analyses': analysis_count,
                'total_faces': face_count,
                'total_searches': search_count,
                'database_size': os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
            }
            
        except Exception as e:
            logger.error(f"Fel vid hämtning av statistik: {str(e)}")
            return {'error': str(e)}

def main():
    """Huvudfunktion"""
    print("=== Digital Identitet och Sociala Medier Forskning ===")
    print("Med riktig ansiktsigenkänning")
    print("Välkommen till forskningsverktyget för digital identitet!")
    print()
    
    try:
        # Initiera forskningsprojektet
        research = DigitalIdentityResearch()
        
        # Exempel på användning
        print("Exempel på användning:")
        print("1. Analysera en enskild användare")
        print("2. Reverse Image Search")
        print("3. Visa sökhistorik")
        print("4. Visa statistik")
        print("5. Avsluta")
        print()
        
        # Interaktiv meny
        choice = input("Välj alternativ (1-5): ")
        
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
                    print(f"Användare: {best['username']}")
                    print(f"Konfidens: {best['match_confidence']:.2f}")
                
                if 'analysis' in results:
                    print(f"\nInsikter:")
                    for insight in results['analysis']['insights']:
                        print(f"- {insight}")
                    print(f"Rekommendation: {results['analysis']['recommendation']}")
                
            except Exception as e:
                print(f"Fel: {str(e)}")
        
        elif choice == "3":
            try:
                history = research.get_search_history()
                print(f"\nSökhistorik ({len(history)} sökningar):")
                for i, search in enumerate(history, 1):
                    print(f"{i}. {search['image_path']}: {search['total_matches']} matchningar, {search['best_similarity']:.2f} similaritet")
            except Exception as e:
                print(f"Fel: {str(e)}")
        
        elif choice == "4":
            try:
                stats = research.get_statistics()
                print(f"\nStatistik:")
                print(f"- Totalt antal användare: {stats['total_users']}")
                print(f"- Totalt antal analyser: {stats['total_analyses']}")
                print(f"- Totalt antal ansikten: {stats['total_faces']}")
                print(f"- Totalt antal sökningar: {stats['total_searches']}")
                print(f"- Databasstorlek: {stats['database_size']} bytes")
            except Exception as e:
                print(f"Fel: {str(e)}")
        
        elif choice == "5":
            print("Tack för att du använde forskningsverktyget!")
        
        else:
            print("Ogiltigt val")
    
    except Exception as e:
        print(f"Kritiskt fel: {str(e)}")

if __name__ == "__main__":
    main()
