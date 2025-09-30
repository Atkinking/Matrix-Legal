"""
Datahanteringsmodul för digital identitetsforskning
"""

import os
import json
import sqlite3
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
from pathlib import Path
import hashlib
import shutil

logger = logging.getLogger(__name__)

class DataManager:
    """Klass för hantering av forskningsdata"""
    
    def __init__(self, data_dir: str = "data", db_path: str = "data/research.db"):
        """
        Initiera datahanterare
        
        Args:
            data_dir (str): Huvudmapp för data
            db_path (str): Sökväg till databas
        """
        self.data_dir = Path(data_dir)
        self.db_path = db_path
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.results_dir = self.data_dir / "results"
        
        # Skapa mappar om de inte finns
        self._create_directories()
        
        # Initiera databas
        self._init_database()
        
        logger.info("DataManager initierad")
    
    def _create_directories(self):
        """Skapa nödvändiga mappar"""
        directories = [self.raw_dir, self.processed_dir, self.results_dir]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Skapade mapp: {directory}")
    
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS social_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    platform TEXT NOT NULL,
                    data_json TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS face_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    image_path TEXT,
                    face_encoding TEXT,
                    analysis_json TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
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
            
            conn.commit()
            conn.close()
            
            logger.info("Databas initierad")
            
        except Exception as e:
            logger.error(f"Fel vid initiering av databas: {str(e)}")
    
    def save_user_data(self, username: str, platform: str, data: Dict) -> bool:
        """
        Spara användardata
        
        Args:
            username (str): Användarnamn
            platform (str): Plattform
            data (Dict): Data att spara
        
        Returns:
            bool: True om sparande lyckades
        """
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
            
            # Spara social data
            data_json = json.dumps(data, ensure_ascii=False)
            cursor.execute('''
                INSERT INTO social_data (user_id, platform, data_json)
                VALUES (?, ?, ?)
            ''', (user_id, platform, data_json))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Sparade data för {username} från {platform}")
            return True
            
        except Exception as e:
            logger.error(f"Fel vid sparande av användardata: {str(e)}")
            return False
    
    def save_face_analysis(self, username: str, image_path: str, face_encoding: List[float], 
                          analysis: Dict) -> bool:
        """
        Spara ansiktsanalys
        
        Args:
            username (str): Användarnamn
            image_path (str): Sökväg till bild
            face_encoding (List[float]): Ansiktsencoding
            analysis (Dict): Analysresultat
        
        Returns:
            bool: True om sparande lyckades
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Hitta användare
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_result = cursor.fetchone()
            
            if not user_result:
                logger.error(f"Användare {username} inte hittad")
                return False
            
            user_id = user_result[0]
            
            # Spara ansiktsanalys
            encoding_json = json.dumps(face_encoding)
            analysis_json = json.dumps(analysis, ensure_ascii=False)
            
            cursor.execute('''
                INSERT INTO face_analysis (user_id, image_path, face_encoding, analysis_json)
                VALUES (?, ?, ?, ?)
            ''', (user_id, image_path, encoding_json, analysis_json))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Sparade ansiktsanalys för {username}")
            return True
            
        except Exception as e:
            logger.error(f"Fel vid sparande av ansiktsanalys: {str(e)}")
            return False
    
    def save_analysis_results(self, username: str, results: Dict) -> bool:
        """
        Spara analysresultat
        
        Args:
            username (str): Användarnamn
            results (Dict): Analysresultat
        
        Returns:
            bool: True om sparande lyckades
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Hitta användare
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_result = cursor.fetchone()
            
            if not user_result:
                logger.error(f"Användare {username} inte hittad")
                return False
            
            user_id = user_result[0]
            
            # Spara resultat
            results_json = json.dumps(results, ensure_ascii=False)
            cursor.execute('''
                INSERT INTO analysis_results (user_id, analysis_type, results_json)
                VALUES (?, ?, ?)
            ''', (user_id, 'identity_analysis', results_json))
            
            conn.commit()
            conn.close()
            
            # Spara även som JSON-fil
            self._save_results_to_file(username, results)
            
            logger.info(f"Sparade analysresultat för {username}")
            return True
            
        except Exception as e:
            logger.error(f"Fel vid sparande av analysresultat: {str(e)}")
            return False
    
    def _save_results_to_file(self, username: str, results: Dict):
        """Spara resultat som JSON-fil"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{username}_analysis_{timestamp}.json"
            filepath = self.results_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Sparade resultat till fil: {filepath}")
            
        except Exception as e:
            logger.error(f"Fel vid sparande av resultatfil: {str(e)}")
    
    def get_user_data(self, username: str) -> Dict:
        """
        Hämta användardata
        
        Args:
            username (str): Användarnamn
        
        Returns:
            Dict: Användardata
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Hitta användare
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_result = cursor.fetchone()
            
            if not user_result:
                return {'error': f'Användare {username} inte hittad'}
            
            user_id = user_result[0]
            
            # Hämta social data
            cursor.execute('''
                SELECT platform, data_json, timestamp 
                FROM social_data 
                WHERE user_id = ? 
                ORDER BY timestamp DESC
            ''', (user_id,))
            
            social_data = {}
            for row in cursor.fetchall():
                platform, data_json, timestamp = row
                social_data[platform] = {
                    'data': json.loads(data_json),
                    'timestamp': timestamp
                }
            
            # Hämta ansiktsanalys
            cursor.execute('''
                SELECT image_path, face_encoding, analysis_json, timestamp
                FROM face_analysis 
                WHERE user_id = ? 
                ORDER BY timestamp DESC
            ''', (user_id,))
            
            face_analysis = []
            for row in cursor.fetchall():
                image_path, face_encoding, analysis_json, timestamp = row
                face_analysis.append({
                    'image_path': image_path,
                    'face_encoding': json.loads(face_encoding),
                    'analysis': json.loads(analysis_json),
                    'timestamp': timestamp
                })
            
            # Hämta analysresultat
            cursor.execute('''
                SELECT analysis_type, results_json, timestamp
                FROM analysis_results 
                WHERE user_id = ? 
                ORDER BY timestamp DESC
            ''', (user_id,))
            
            analysis_results = []
            for row in cursor.fetchall():
                analysis_type, results_json, timestamp = row
                analysis_results.append({
                    'type': analysis_type,
                    'results': json.loads(results_json),
                    'timestamp': timestamp
                })
            
            conn.close()
            
            return {
                'username': username,
                'social_data': social_data,
                'face_analysis': face_analysis,
                'analysis_results': analysis_results
            }
            
        except Exception as e:
            logger.error(f"Fel vid hämtning av användardata: {str(e)}")
            return {'error': str(e)}
    
    def export_to_json(self, output_path: str = "data/export/research_data.json") -> bool:
        """
        Exportera all data som JSON
        
        Args:
            output_path (str): Sökväg för export
        
        Returns:
            bool: True om export lyckades
        """
        try:
            # Skapa mapp om den inte finns
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Hämta alla användare
            cursor.execute("SELECT username FROM users")
            usernames = [row[0] for row in cursor.fetchall()]
            
            export_data = {}
            for username in usernames:
                user_data = self.get_user_data(username)
                export_data[username] = user_data
            
            # Spara export
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            conn.close()
            
            logger.info(f"Data exporterad till {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Fel vid JSON-export: {str(e)}")
            return False
    
    def export_to_csv(self, output_path: str = "data/export/research_data.csv") -> bool:
        """
        Exportera data som CSV
        
        Args:
            output_path (str): Sökväg för export
        
        Returns:
            bool: True om export lyckades
        """
        try:
            # Skapa mapp om den inte finns
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            conn = sqlite3.connect(self.db_path)
            
            # Hämta användardata
            users_df = pd.read_sql_query("SELECT * FROM users", conn)
            
            # Hämta social data
            social_df = pd.read_sql_query("SELECT * FROM social_data", conn)
            
            # Hämta ansiktsanalys
            face_df = pd.read_sql_query("SELECT * FROM face_analysis", conn)
            
            # Hämta analysresultat
            results_df = pd.read_sql_query("SELECT * FROM analysis_results", conn)
            
            conn.close()
            
            # Kombinera data
            combined_df = pd.merge(users_df, social_df, on='user_id', how='left')
            combined_df = pd.merge(combined_df, face_df, on='user_id', how='left')
            combined_df = pd.merge(combined_df, results_df, on='user_id', how='left')
            
            # Spara CSV
            combined_df.to_csv(output_path, index=False, encoding='utf-8')
            
            logger.info(f"Data exporterad till {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Fel vid CSV-export: {str(e)}")
            return False
    
    def cleanup_old_data(self, days_old: int = 30) -> bool:
        """
        Rensa gammal data
        
        Args:
            days_old (int): Antal dagar gammal data att behålla
        
        Returns:
            bool: True om rensning lyckades
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Rensa gamla analysresultat
            cursor.execute('''
                DELETE FROM analysis_results 
                WHERE timestamp < datetime('now', '-{} days')
            '''.format(days_old))
            
            # Rensa gamla ansiktsanalyser
            cursor.execute('''
                DELETE FROM face_analysis 
                WHERE timestamp < datetime('now', '-{} days')
            '''.format(days_old))
            
            # Rensa gamla social data
            cursor.execute('''
                DELETE FROM social_data 
                WHERE timestamp < datetime('now', '-{} days')
            '''.format(days_old))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Rensade data äldre än {days_old} dagar")
            return True
            
        except Exception as e:
            logger.error(f"Fel vid rensning av data: {str(e)}")
            return False
    
    def get_statistics(self) -> Dict:
        """
        Hämta statistik över data
        
        Returns:
            Dict: Data statistik
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Räkna användare
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            # Räkna social data
            cursor.execute("SELECT COUNT(*) FROM social_data")
            social_count = cursor.fetchone()[0]
            
            # Räkna ansiktsanalyser
            cursor.execute("SELECT COUNT(*) FROM face_analysis")
            face_count = cursor.fetchone()[0]
            
            # Räkna analysresultat
            cursor.execute("SELECT COUNT(*) FROM analysis_results")
            results_count = cursor.fetchone()[0]
            
            # Plattformsfördelning
            cursor.execute('''
                SELECT platform, COUNT(*) 
                FROM social_data 
                GROUP BY platform
            ''')
            platform_distribution = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                'users': user_count,
                'social_data_entries': social_count,
                'face_analyses': face_count,
                'analysis_results': results_count,
                'platform_distribution': platform_distribution,
                'database_size': os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
            }
            
        except Exception as e:
            logger.error(f"Fel vid hämtning av statistik: {str(e)}")
            return {'error': str(e)}
