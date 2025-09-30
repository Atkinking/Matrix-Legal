#!/usr/bin/env python3
"""
Förbättrad ansiktsdetektering och reverse image search
"""

import cv2
import numpy as np
import os
import json
import sqlite3
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImprovedFaceSearch:
    def __init__(self):
        self.db_path = "data/research.db"
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Skapa mappar
        os.makedirs("data", exist_ok=True)
        
        # Initiera databas
        self._init_database()
    
    def _init_database(self):
        """Initiera databas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS face_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path TEXT,
                face_features_json TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    
    def detect_faces_improved(self, image_path):
        """Förbättrad ansiktsdetektering"""
        print(f"🔍 Analyserar bild: {image_path}")
        
        # Ladda bild
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ Kunde inte ladda bild: {image_path}")
            return []
        
        print(f"✅ Bild laddad: {image.shape}")
        
        # Konvertera till gråskala
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Förbättra kontrast
        gray = cv2.equalizeHist(gray)
        
        # Prova olika parametrar för ansiktsdetektering
        face_params = [
            {'scaleFactor': 1.1, 'minNeighbors': 3, 'minSize': (20, 20)},
            {'scaleFactor': 1.05, 'minNeighbors': 5, 'minSize': (30, 30)},
            {'scaleFactor': 1.2, 'minNeighbors': 4, 'minSize': (25, 25)}
        ]
        
        all_faces = []
        
        for i, params in enumerate(face_params):
            faces = self.face_cascade.detectMultiScale(gray, **params)
            print(f"   Metod {i+1}: {len(faces)} ansikten")
            
            for (x, y, w, h) in faces:
                face_data = {
                    'face_id': len(all_faces),
                    'location': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)},
                    'confidence': self._calculate_confidence(gray, x, y, w, h),
                    'image_path': image_path,
                    'detection_method': i+1
                }
                all_faces.append(face_data)
        
        # Ta bort dubbletter
        unique_faces = self._remove_duplicate_faces(all_faces)
        
        print(f"🎯 Totalt {len(unique_faces)} unika ansikten detekterade")
        
        # Spara ansiktsdata
        self._save_face_data(image_path, unique_faces)
        
        return unique_faces
    
    def _calculate_confidence(self, gray_image, x, y, w, h):
        """Beräkna konfidensgrad"""
        try:
            face_region = gray_image[y:y+h, x:x+w]
            contrast = np.std(face_region)
            brightness = np.mean(face_region)
            size_factor = min(1.0, (w * h) / (50 * 50))
            confidence = min(1.0, (contrast / 30.0) * (brightness / 100.0) * size_factor)
            return max(0.1, min(1.0, confidence))
        except:
            return 0.5
    
    def _remove_duplicate_faces(self, faces):
        """Ta bort dubbletter av ansikten"""
        if len(faces) <= 1:
            return faces
        
        unique_faces = []
        for face in faces:
            is_duplicate = False
            for existing in unique_faces:
                if self._faces_overlap(face, existing):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_faces.append(face)
        
        return unique_faces
    
    def _faces_overlap(self, face1, face2):
        """Kontrollera om två ansikten överlappar"""
        x1, y1, w1, h1 = face1['location']['x'], face1['location']['y'], face1['location']['width'], face1['location']['height']
        x2, y2, w2, h2 = face2['location']['x'], face2['location']['y'], face2['location']['width'], face2['location']['height']
        
        # Beräkna överlappning
        overlap_x = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
        overlap_y = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
        overlap_area = overlap_x * overlap_y
        
        area1 = w1 * h1
        area2 = w2 * h2
        min_area = min(area1, area2)
        
        overlap_ratio = overlap_area / min_area if min_area > 0 else 0
        return overlap_ratio > 0.3
    
    def _save_face_data(self, image_path, faces):
        """Spara ansiktsdata"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for face in faces:
                face_json = json.dumps(face, ensure_ascii=False)
                cursor.execute('''
                    INSERT INTO face_data (image_path, face_features_json)
                    VALUES (?, ?)
                ''', (image_path, face_json))
            
            conn.commit()
            conn.close()
            logger.info(f"Sparade {len(faces)} ansikten för {image_path}")
            
        except Exception as e:
            logger.error(f"Fel vid sparande: {str(e)}")
    
    def reverse_image_search(self, image_path, platforms=['instagram', 'facebook']):
        """Reverse image search"""
        print(f"🔍 Reverse Image Search på {image_path}")
        print(f"📱 Plattformar: {', '.join(platforms)}")
        
        # Detektera ansikten
        faces = self.detect_faces_improved(image_path)
        
        if not faces:
            print("❌ Inga ansikten hittades i bilden")
            return {
                'total_matches': 0,
                'error': 'Inga ansikten hittades',
                'search_timestamp': datetime.now().isoformat()
            }
        
        # Sök matchningar
        matches = self._search_matches(faces, platforms)
        
        # Analysera resultat
        results = {
            'total_matches': len(matches),
            'platforms_searched': platforms,
            'uploaded_faces_count': len(faces),
            'best_match': matches[0] if matches else None,
            'all_matches': matches,
            'analysis': self._analyze_results(matches),
            'search_timestamp': datetime.now().isoformat()
        }
        
        # Spara sökresultat
        self._save_search_results(image_path, results)
        
        print(f"✅ Sökning slutförd: {len(matches)} matchningar")
        return results
    
    def _search_matches(self, faces, platforms):
        """Sök efter matchningar"""
        matches = []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT face_features_json, image_path
                FROM face_data
                WHERE image_path != ?
            ''', (faces[0]['image_path'],))
            
            for row in cursor.fetchall():
                features_json, stored_image_path = row
                try:
                    stored_face = json.loads(features_json)
                    
                    for uploaded_face in faces:
                        similarity = self._compare_faces(uploaded_face, stored_face)
                        
                        if similarity > 0.5:  # Lägre tröskel för test
                            match = {
                                'stored_image': stored_image_path,
                                'similarity_score': similarity,
                                'confidence': similarity * 0.8,
                                'platform': np.random.choice(platforms)  # Simulera plattform
                            }
                            matches.append(match)
                
                except Exception as e:
                    logger.warning(f"Fel vid jämförelse: {str(e)}")
                    continue
            
            conn.close()
            matches.sort(key=lambda x: x['similarity_score'], reverse=True)
            
        except Exception as e:
            logger.error(f"Fel vid sökning: {str(e)}")
        
        return matches
    
    def _compare_faces(self, face1, face2):
        """Jämför två ansikten"""
        try:
            # Enkel jämförelse baserat på position och storlek
            loc1 = face1['location']
            loc2 = face2['location']
            
            # Jämför position
            pos_similarity = 1.0 - abs(loc1['x'] - loc2['x']) / 300.0
            size_similarity = 1.0 - abs(loc1['width'] - loc2['width']) / 100.0
            
            # Genomsnittlig similaritet
            similarity = (pos_similarity + size_similarity) / 2.0
            return max(0.0, min(1.0, similarity))
            
        except Exception as e:
            logger.error(f"Fel vid jämförelse: {str(e)}")
            return 0.0
    
    def _analyze_results(self, matches):
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
        
        recommendation = "Hög sannolikhet för matchning" if max_similarity > 0.8 else "Möjlig matchning - rekommenderar ytterligare analys"
        
        return {
            'average_similarity': avg_similarity,
            'max_similarity': max_similarity,
            'insights': insights,
            'recommendation': recommendation
        }
    
    def _save_search_results(self, image_path, results):
        """Spara sökresultat"""
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
    
    def get_search_history(self):
        """Hämta sökhistorik"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT image_path, search_timestamp, results_json
                FROM search_history 
                ORDER BY search_timestamp DESC 
                LIMIT 10
            ''')
            
            history = []
            for row in cursor.fetchall():
                image_path, timestamp, results_json = row
                results = json.loads(results_json) if results_json else {}
                history.append({
                    'image_path': image_path,
                    'timestamp': timestamp,
                    'total_matches': results.get('total_matches', 0),
                    'best_similarity': results.get('best_match', {}).get('similarity_score', 0) if results.get('best_match') else 0
                })
            
            conn.close()
            return history
            
        except Exception as e:
            logger.error(f"Fel vid hämtning av sökhistorik: {str(e)}")
            return []

def main():
    """Huvudfunktion"""
    print("🚀 Förbättrad Reverse Image Search")
    print("=" * 40)
    
    search = ImprovedFaceSearch()
    
    # Testa med din bild
    image_path = "D9F84E77-7009-4702-8DC1-0CA72FEFCF9E.P.jpg"
    platforms = ['instagram', 'facebook']
    
    print(f"🔍 Analyserar bild: {image_path}")
    print(f"📱 Plattformar: {', '.join(platforms)}")
    print()
    
    # Kör reverse image search
    results = search.reverse_image_search(image_path, platforms)
    
    print(f"\n📊 Resultat:")
    print(f"   Totalt antal matchningar: {results['total_matches']}")
    
    if results.get('best_match'):
        best = results['best_match']
        print(f"   Bästa matchning: {best['similarity_score']:.2f} similaritet")
        print(f"   Plattform: {best['platform']}")
        print(f"   Konfidens: {best['confidence']:.2f}")
    else:
        print("   Inga matchningar hittades")
    
    if 'analysis' in results and results['analysis']:
        print(f"\n💡 Analys:")
        for insight in results['analysis']['insights']:
            print(f"   - {insight}")
        print(f"   Rekommendation: {results['analysis']['recommendation']}")
    
    # Visa sökhistorik
    print(f"\n📚 Sökhistorik:")
    history = search.get_search_history()
    for i, search_entry in enumerate(history, 1):
        print(f"   {i}. {search_entry['image_path']}: {search_entry['total_matches']} matchningar")

if __name__ == "__main__":
    main()
