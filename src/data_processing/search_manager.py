"""
Sökhanteringsmodul för reverse image search
"""

import sqlite3
import json
import hashlib
from typing import Dict, List, Optional
from datetime import datetime
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class SearchManager:
    """Klass för hantering av sökresultat och sökhistorik"""
    
    def __init__(self, db_path: str = "data/research.db"):
        """
        Initiera sökhanterare
        
        Args:
            db_path (str): Sökväg till databas
        """
        self.db_path = db_path
        self._init_search_tables()
        logger.info("SearchManager initierad")
    
    def _init_search_tables(self):
        """Initiera tabeller för sökhantering"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Sökhistorik tabell
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    search_id TEXT UNIQUE NOT NULL,
                    image_path TEXT NOT NULL,
                    search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    results_json TEXT,
                    total_matches INTEGER DEFAULT 0,
                    best_similarity REAL DEFAULT 0.0
                )
            ''')
            
            # Matchningar tabell
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS search_matches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    search_id TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    similarity_score REAL NOT NULL,
                    confidence_score REAL NOT NULL,
                    matched_face_id TEXT,
                    match_data_json TEXT,
                    FOREIGN KEY (search_id) REFERENCES search_history (search_id)
                )
            ''')
            
            # Ansiktsindex för snabb sökning
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS face_index (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    face_id TEXT UNIQUE NOT NULL,
                    platform TEXT NOT NULL,
                    user_id TEXT,
                    encoding_json TEXT NOT NULL,
                    quality_score REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Skapa index för snabbare sökning
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_face_platform ON face_index (platform)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_face_quality ON face_index (quality_score)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_search_timestamp ON search_history (search_timestamp)')
            
            conn.commit()
            conn.close()
            
            logger.info("Sökhanteringstabeller initierade")
            
        except Exception as e:
            logger.error(f"Fel vid initiering av sökhanteringstabeller: {str(e)}")
    
    def save_search_result(self, search_id: str, image_path: str, results: Dict) -> bool:
        """
        Spara sökresultat
        
        Args:
            search_id (str): Unikt ID för sökningen
            image_path (str): Sökväg till ursprungsbild
            results (Dict): Sökresultat
        
        Returns:
            bool: True om sparande lyckades
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Spara huvudresultat
            results_json = json.dumps(results, ensure_ascii=False)
            total_matches = results.get('total_matches', 0)
            best_match = results.get('best_overall_match')
            best_similarity = best_match.get('similarity_score', 0.0) if best_match else 0.0
            
            cursor.execute('''
                INSERT OR REPLACE INTO search_history 
                (search_id, image_path, results_json, total_matches, best_similarity)
                VALUES (?, ?, ?, ?, ?)
            ''', (search_id, image_path, results_json, total_matches, best_similarity))
            
            # Spara individuella matchningar
            matches = results.get('all_matches', [])
            for match in matches:
                match_data_json = json.dumps(match, ensure_ascii=False)
                cursor.execute('''
                    INSERT INTO search_matches 
                    (search_id, platform, similarity_score, confidence_score, matched_face_id, match_data_json)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    search_id,
                    match.get('platform', ''),
                    match.get('similarity_score', 0.0),
                    match.get('match_confidence', 0.0),
                    match.get('existing_face', {}).get('face_id', ''),
                    match_data_json
                ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Sparade sökresultat för {search_id}")
            return True
            
        except Exception as e:
            logger.error(f"Fel vid sparande av sökresultat: {str(e)}")
            return False
    
    def get_search_history(self, limit: int = 10) -> List[Dict]:
        """
        Hämta sökhistorik
        
        Args:
            limit (int): Max antal sökningar
        
        Returns:
            List[Dict]: Sökhistorik
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT search_id, image_path, search_timestamp, total_matches, best_similarity
                FROM search_history 
                ORDER BY search_timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            history = []
            for row in cursor.fetchall():
                search_id, image_path, timestamp, total_matches, best_similarity = row
                history.append({
                    'search_id': search_id,
                    'image_path': image_path,
                    'timestamp': timestamp,
                    'total_matches': total_matches,
                    'best_similarity': best_similarity
                })
            
            conn.close()
            return history
            
        except Exception as e:
            logger.error(f"Fel vid hämtning av sökhistorik: {str(e)}")
            return []
    
    def get_search_details(self, search_id: str) -> Dict:
        """
        Hämta detaljer för specifik sökning
        
        Args:
            search_id (str): ID för sökning
        
        Returns:
            Dict: Sökdetaljer
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Hämta huvudsökning
            cursor.execute('''
                SELECT image_path, search_timestamp, results_json, total_matches, best_similarity
                FROM search_history 
                WHERE search_id = ?
            ''', (search_id,))
            
            search_result = cursor.fetchone()
            if not search_result:
                return {'error': 'Sökning inte hittad'}
            
            image_path, timestamp, results_json, total_matches, best_similarity = search_result
            
            # Hämta matchningar
            cursor.execute('''
                SELECT platform, similarity_score, confidence_score, match_data_json
                FROM search_matches 
                WHERE search_id = ? 
                ORDER BY similarity_score DESC
            ''', (search_id,))
            
            matches = []
            for row in cursor.fetchall():
                platform, similarity_score, confidence_score, match_data_json = row
                match_data = json.loads(match_data_json)
                matches.append({
                    'platform': platform,
                    'similarity_score': similarity_score,
                    'confidence_score': confidence_score,
                    'match_data': match_data
                })
            
            conn.close()
            
            return {
                'search_id': search_id,
                'image_path': image_path,
                'timestamp': timestamp,
                'total_matches': total_matches,
                'best_similarity': best_similarity,
                'matches': matches,
                'results': json.loads(results_json) if results_json else {}
            }
            
        except Exception as e:
            logger.error(f"Fel vid hämtning av sökdetaljer: {str(e)}")
            return {'error': str(e)}
    
    def add_face_to_index(self, face_id: str, platform: str, user_id: str, 
                         encoding: List[float], quality_score: float = 0.0) -> bool:
        """
        Lägg till ansikte i sökindex
        
        Args:
            face_id (str): Unikt ID för ansiktet
            platform (str): Plattform
            user_id (str): Användar-ID
            encoding (List[float]): Ansiktsencoding
            quality_score (float): Kvalitetspoäng
        
        Returns:
            bool: True om tillägg lyckades
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            encoding_json = json.dumps(encoding)
            
            cursor.execute('''
                INSERT OR REPLACE INTO face_index 
                (face_id, platform, user_id, encoding_json, quality_score)
                VALUES (?, ?, ?, ?, ?)
            ''', (face_id, platform, user_id, encoding_json, quality_score))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Lade till ansikte {face_id} i sökindex")
            return True
            
        except Exception as e:
            logger.error(f"Fel vid tillägg av ansikte i index: {str(e)}")
            return False
    
    def get_faces_by_platform(self, platform: str, min_quality: float = 0.0) -> List[Dict]:
        """
        Hämta ansikten från specifik plattform
        
        Args:
            platform (str): Plattform
            min_quality (float): Minsta kvalitetspoäng
        
        Returns:
            List[Dict]: Ansikten från plattformen
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT face_id, user_id, encoding_json, quality_score, created_at
                FROM face_index 
                WHERE platform = ? AND quality_score >= ?
                ORDER BY quality_score DESC
            ''', (platform, min_quality))
            
            faces = []
            for row in cursor.fetchall():
                face_id, user_id, encoding_json, quality_score, created_at = row
                faces.append({
                    'face_id': face_id,
                    'user_id': user_id,
                    'encoding': json.loads(encoding_json),
                    'quality_score': quality_score,
                    'created_at': created_at,
                    'platform': platform
                })
            
            conn.close()
            return faces
            
        except Exception as e:
            logger.error(f"Fel vid hämtning av ansikten: {str(e)}")
            return []
    
    def search_similar_faces(self, target_encoding: List[float], 
                           platforms: List[str] = None, 
                           similarity_threshold: float = 0.6) -> List[Dict]:
        """
        Sök efter liknande ansikten
        
        Args:
            target_encoding (List[float]): Målsökning
            platforms (List[str]): Plattformar att söka på
            similarity_threshold (float): Similaritetströskel
        
        Returns:
            List[Dict]: Liknande ansikten
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Bygg WHERE-klausul
            where_clause = "WHERE quality_score >= ?"
            params = [similarity_threshold]
            
            if platforms:
                placeholders = ','.join(['?' for _ in platforms])
                where_clause += f" AND platform IN ({placeholders})"
                params.extend(platforms)
            
            cursor.execute(f'''
                SELECT face_id, user_id, platform, encoding_json, quality_score, created_at
                FROM face_index 
                {where_clause}
                ORDER BY quality_score DESC
            ''', params)
            
            similar_faces = []
            for row in cursor.fetchall():
                face_id, user_id, platform, encoding_json, quality_score, created_at = row
                encoding = json.loads(encoding_json)
                
                # Beräkna similaritet (förenklad)
                similarity = self._calculate_encoding_similarity(target_encoding, encoding)
                
                if similarity >= similarity_threshold:
                    similar_faces.append({
                        'face_id': face_id,
                        'user_id': user_id,
                        'platform': platform,
                        'encoding': encoding,
                        'quality_score': quality_score,
                        'similarity': similarity,
                        'created_at': created_at
                    })
            
            # Sortera efter similaritet
            similar_faces.sort(key=lambda x: x['similarity'], reverse=True)
            
            conn.close()
            return similar_faces
            
        except Exception as e:
            logger.error(f"Fel vid sökning av liknande ansikten: {str(e)}")
            return []
    
    def _calculate_encoding_similarity(self, encoding1: List[float], encoding2: List[float]) -> float:
        """
        Beräkna similaritet mellan encodingar
        
        Args:
            encoding1 (List[float]): Första encodingen
            encoding2 (List[float]): Andra encodingen
        
        Returns:
            float: Similaritetspoäng
        """
        try:
            import numpy as np
            
            enc1 = np.array(encoding1)
            enc2 = np.array(encoding2)
            
            if len(enc1) == 0 or len(enc2) == 0:
                return 0.0
            
            # Beräkna avstånd
            distance = np.linalg.norm(enc1 - enc2)
            
            # Konvertera till similaritetspoäng
            similarity = max(0.0, 1.0 - distance)
            
            return similarity
            
        except Exception as e:
            logger.error(f"Fel vid beräkning av encoding-similaritet: {str(e)}")
            return 0.0
    
    def export_search_result(self, search_id: str, format: str = 'json') -> str:
        """
        Exportera sökresultat
        
        Args:
            search_id (str): ID för sökning
            format (str): Exportformat
        
        Returns:
            str: Sökväg till exporterad fil
        """
        try:
            # Hämta sökdetaljer
            details = self.get_search_details(search_id)
            
            if 'error' in details:
                return ""
            
            # Skapa exportmapp
            export_dir = Path("data/export/search_results")
            export_dir.mkdir(parents=True, exist_ok=True)
            
            # Generera filnamn
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"search_result_{search_id}_{timestamp}.{format}"
            filepath = export_dir / filename
            
            if format == 'json':
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(details, f, indent=2, ensure_ascii=False)
            
            elif format == 'csv':
                import pandas as pd
                df = pd.DataFrame(details['matches'])
                df.to_csv(filepath, index=False, encoding='utf-8')
            
            logger.info(f"Exporterade sökresultat till {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Fel vid export av sökresultat: {str(e)}")
            return ""
    
    def get_search_statistics(self) -> Dict:
        """
        Hämta statistik över sökningar
        
        Returns:
            Dict: Sökstatistik
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Totalt antal sökningar
            cursor.execute("SELECT COUNT(*) FROM search_history")
            total_searches = cursor.fetchone()[0]
            
            # Totalt antal matchningar
            cursor.execute("SELECT COUNT(*) FROM search_matches")
            total_matches = cursor.fetchone()[0]
            
            # Genomsnittlig similaritet
            cursor.execute("SELECT AVG(best_similarity) FROM search_history WHERE best_similarity > 0")
            avg_similarity = cursor.fetchone()[0] or 0.0
            
            # Plattformsfördelning
            cursor.execute('''
                SELECT platform, COUNT(*) 
                FROM search_matches 
                GROUP BY platform
            ''')
            platform_distribution = dict(cursor.fetchall())
            
            # Ansiktsindex statistik
            cursor.execute("SELECT COUNT(*) FROM face_index")
            total_faces = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT platform, COUNT(*) 
                FROM face_index 
                GROUP BY platform
            ''')
            face_platform_distribution = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                'total_searches': total_searches,
                'total_matches': total_matches,
                'average_similarity': avg_similarity,
                'platform_distribution': platform_distribution,
                'total_faces_indexed': total_faces,
                'face_platform_distribution': face_platform_distribution
            }
            
        except Exception as e:
            logger.error(f"Fel vid hämtning av sökstatistik: {str(e)}")
            return {'error': str(e)}
    
    def cleanup_old_searches(self, days_old: int = 30) -> bool:
        """
        Rensa gamla sökningar
        
        Args:
            days_old (int): Antal dagar gammal data att behålla
        
        Returns:
            bool: True om rensning lyckades
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Rensa gamla sökningar
            cursor.execute('''
                DELETE FROM search_history 
                WHERE search_timestamp < datetime('now', '-{} days')
            '''.format(days_old))
            
            # Rensa gamla matchningar
            cursor.execute('''
                DELETE FROM search_matches 
                WHERE search_id NOT IN (
                    SELECT search_id FROM search_history
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info(f"Rensade sökningar äldre än {days_old} dagar")
            return True
            
        except Exception as e:
            logger.error(f"Fel vid rensning av gamla sökningar: {str(e)}")
            return False
