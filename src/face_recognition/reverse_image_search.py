"""
Reverse Image Search för digital identitetsforskning
"""

import cv2
import face_recognition
import numpy as np
import requests
import hashlib
import os
from typing import List, Dict, Tuple, Optional
import logging
from pathlib import Path
import json
from datetime import datetime
import time

logger = logging.getLogger(__name__)

class ReverseImageSearch:
    """Klass för reverse image search över sociala medier"""
    
    def __init__(self, face_detector, social_manager, data_manager):
        """
        Initiera reverse image search
        
        Args:
            face_detector: FaceDetector instans
            social_manager: SocialMediaManager instans
            data_manager: DataManager instans
        """
        self.face_detector = face_detector
        self.social_manager = social_manager
        self.data_manager = data_manager
        self.search_cache = {}
        self.similarity_threshold = 0.6
        
        logger.info("ReverseImageSearch initierad")
    
    def search_face_in_social_media(self, image_path: str, platforms: List[str] = None) -> Dict:
        """
        Sök efter ansikte i sociala medier
        
        Args:
            image_path (str): Sökväg till bild att söka efter
            platforms (List[str]): Lista över plattformar att söka på
        
        Returns:
            Dict: Sökresultat
        """
        logger.info(f"Börjar reverse image search för {image_path}")
        
        if platforms is None:
            platforms = ['twitter', 'instagram', 'facebook']
        
        try:
            # Analysera uppladdad bild
            uploaded_face_features = self._analyze_uploaded_image(image_path)
            
            if not uploaded_face_features:
                return {'error': 'Inga ansikten hittades i uppladdad bild'}
            
            # Sök på varje plattform
            search_results = {}
            for platform in platforms:
                logger.info(f"Söker på {platform}")
                platform_results = self._search_on_platform(
                    uploaded_face_features, platform
                )
                search_results[platform] = platform_results
            
            # Kombinera och analysera resultat
            combined_results = self._combine_search_results(search_results)
            
            # Spara sökresultat
            self._save_search_results(image_path, combined_results)
            
            logger.info("Reverse image search slutförd")
            return combined_results
            
        except Exception as e:
            logger.error(f"Fel vid reverse image search: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_uploaded_image(self, image_path: str) -> List[Dict]:
        """
        Analysera uppladdad bild för ansiktsdrag
        
        Args:
            image_path (str): Sökväg till bild
        
        Returns:
            List[Dict]: Ansiktsdrag från bilden
        """
        try:
            # Kontrollera att bilden finns
            if not os.path.exists(image_path):
                logger.error(f"Bildfil finns inte: {image_path}")
                return []
            
            # Detektera ansikten
            faces = self.face_detector.detect_faces(image_path)
            
            if not faces:
                logger.warning("Inga ansikten hittades i bilden")
                return []
            
            # Förbättra ansiktsdrag med maskinlärning
            enhanced_faces = self._enhance_face_features(faces)
            
            logger.info(f"Analyserade {len(enhanced_faces)} ansikten i uppladdad bild")
            return enhanced_faces
            
        except Exception as e:
            logger.error(f"Fel vid analys av uppladdad bild: {str(e)}")
            return []
    
    def _enhance_face_features(self, faces: List[Dict]) -> List[Dict]:
        """
        Förbättra ansiktsdrag med maskinlärning
        
        Args:
            faces (List[Dict]): Grundläggande ansiktsdrag
        
        Returns:
            List[Dict]: Förbättrade ansiktsdrag
        """
        enhanced_faces = []
        
        for face in faces:
            # Lägg till förbättrade funktioner
            enhanced_face = face.copy()
            
            # Beräkna ansiktsvinklar
            enhanced_face['face_angle'] = self._calculate_face_angle(face)
            
            # Analysera ansiktskvalitet
            enhanced_face['quality_score'] = self._calculate_face_quality(face)
            
            # Extrahera ansiktslandmärken
            enhanced_face['landmarks'] = self._extract_face_landmarks(face)
            
            # Beräkna ansiktsproportioner
            enhanced_face['proportions'] = self._calculate_face_proportions(face)
            
            enhanced_faces.append(enhanced_face)
        
        return enhanced_faces
    
    def _search_on_platform(self, face_features: List[Dict], platform: str) -> Dict:
        """
        Sök på specifik plattform
        
        Args:
            face_features (List[Dict]): Ansiktsdrag att söka efter
            platform (str): Plattform att söka på
        
        Returns:
            Dict: Sökresultat från plattformen
        """
        try:
            # Hämta befintliga ansiktsencodingar från databasen
            existing_faces = self._get_existing_faces_from_platform(platform)
            
            if not existing_faces:
                logger.warning(f"Inga befintliga ansikten hittades för {platform}")
                return {'matches': [], 'total_searched': 0}
            
            # Jämför med befintliga ansikten
            matches = []
            for uploaded_face in face_features:
                for existing_face in existing_faces:
                    similarity = self._calculate_face_similarity(
                        uploaded_face, existing_face
                    )
                    
                    if similarity > self.similarity_threshold:
                        match = {
                            'similarity_score': similarity,
                            'uploaded_face_id': uploaded_face.get('face_id', 0),
                            'existing_face': existing_face,
                            'platform': platform,
                            'match_confidence': self._calculate_match_confidence(
                                uploaded_face, existing_face, similarity
                            )
                        }
                        matches.append(match)
            
            # Sortera efter similaritet
            matches.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            return {
                'matches': matches,
                'total_searched': len(existing_faces),
                'best_match': matches[0] if matches else None
            }
            
        except Exception as e:
            logger.error(f"Fel vid sökning på {platform}: {str(e)}")
            return {'error': str(e)}
    
    def _get_existing_faces_from_platform(self, platform: str) -> List[Dict]:
        """
        Hämta befintliga ansikten från plattform
        
        Args:
            platform (str): Plattform att hämta från
        
        Returns:
            List[Dict]: Befintliga ansikten
        """
        try:
            # Hämta från databas
            existing_faces = self.data_manager.get_faces_by_platform(platform)
            return existing_faces
            
        except Exception as e:
            logger.error(f"Fel vid hämtning av befintliga ansikten: {str(e)}")
            return []
    
    def _calculate_face_similarity(self, face1: Dict, face2: Dict) -> float:
        """
        Beräkna similaritet mellan två ansikten
        
        Args:
            face1 (Dict): Första ansiktet
            face2 (Dict): Andra ansiktet
        
        Returns:
            float: Similaritetspoäng (0-1)
        """
        try:
            # Grundläggande encoding-jämförelse
            encoding1 = np.array(face1.get('encoding', []))
            encoding2 = np.array(face2.get('encoding', []))
            
            if len(encoding1) == 0 or len(encoding2) == 0:
                return 0.0
            
            # Beräkna avstånd
            distance = np.linalg.norm(encoding1 - encoding2)
            
            # Konvertera till similaritetspoäng
            similarity = max(0.0, 1.0 - distance)
            
            # Justera baserat på ansiktskvalitet
            quality1 = face1.get('quality_score', 0.5)
            quality2 = face2.get('quality_score', 0.5)
            quality_factor = (quality1 + quality2) / 2
            
            # Justera baserat på ansiktsvinklar
            angle1 = face1.get('face_angle', 0)
            angle2 = face2.get('face_angle', 0)
            angle_factor = 1.0 - abs(angle1 - angle2) / 180.0
            
            # Kombinera faktorer
            final_similarity = similarity * quality_factor * angle_factor
            
            return min(1.0, max(0.0, final_similarity))
            
        except Exception as e:
            logger.error(f"Fel vid beräkning av ansiktssimilaritet: {str(e)}")
            return 0.0
    
    def _calculate_face_angle(self, face: Dict) -> float:
        """
        Beräkna ansiktsvinkel
        
        Args:
            face (Dict): Ansiktsdata
        
        Returns:
            float: Ansiktsvinkel i grader
        """
        # Simulerad beräkning av ansiktsvinkel
        # I en riktig implementation skulle detta använda ansiktslandmärken
        return 0.0  # Framåtvänd ansikte
    
    def _calculate_face_quality(self, face: Dict) -> float:
        """
        Beräkna ansiktskvalitet
        
        Args:
            face (Dict): Ansiktsdata
        
        Returns:
            float: Kvalitetspoäng (0-1)
        """
        # Använd befintlig confidence som grund
        base_confidence = face.get('confidence', 0.5)
        
        # Justera baserat på ansiktsstorlek
        location = face.get('location', {})
        width = location.get('right', 0) - location.get('left', 0)
        height = location.get('bottom', 0) - location.get('top', 0)
        
        size_factor = min(1.0, (width * height) / (100 * 100))  # Normalisera
        
        return base_confidence * size_factor
    
    def _extract_face_landmarks(self, face: Dict) -> Dict:
        """
        Extrahera ansiktslandmärken
        
        Args:
            face (Dict): Ansiktsdata
        
        Returns:
            Dict: Ansiktslandmärken
        """
        # Simulerad extraktion av landmärken
        return {
            'eyes': {'left': [0, 0], 'right': [0, 0]},
            'nose': [0, 0],
            'mouth': [0, 0],
            'chin': [0, 0]
        }
    
    def _calculate_face_proportions(self, face: Dict) -> Dict:
        """
        Beräkna ansiktsproportioner
        
        Args:
            face (Dict): Ansiktsdata
        
        Returns:
            Dict: Ansiktsproportioner
        """
        # Simulerad beräkning av proportioner
        return {
            'eye_distance': 0.5,
            'nose_width': 0.3,
            'mouth_width': 0.4,
            'face_width': 1.0
        }
    
    def _calculate_match_confidence(self, face1: Dict, face2: Dict, similarity: float) -> float:
        """
        Beräkna matchningskonfidens
        
        Args:
            face1 (Dict): Första ansiktet
            face2 (Dict): Andra ansiktet
            similarity (float): Similaritetspoäng
        
        Returns:
            float: Matchningskonfidens
        """
        # Kombinera similaritet med kvalitetsfaktorer
        quality1 = face1.get('quality_score', 0.5)
        quality2 = face2.get('quality_score', 0.5)
        
        # Viktad konfidens
        confidence = similarity * (quality1 + quality2) / 2
        
        return min(1.0, max(0.0, confidence))
    
    def _combine_search_results(self, search_results: Dict) -> Dict:
        """
        Kombinera sökresultat från alla plattformar
        
        Args:
            search_results (Dict): Sökresultat från alla plattformar
        
        Returns:
            Dict: Kombinerade resultat
        """
        all_matches = []
        platform_stats = {}
        
        for platform, results in search_results.items():
            if 'error' in results:
                continue
            
            matches = results.get('matches', [])
            all_matches.extend(matches)
            
            platform_stats[platform] = {
                'matches_found': len(matches),
                'total_searched': results.get('total_searched', 0),
                'best_match': results.get('best_match')
            }
        
        # Sortera alla matchningar efter similaritet
        all_matches.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        # Analysera resultat
        analysis = self._analyze_search_results(all_matches, platform_stats)
        
        return {
            'total_matches': len(all_matches),
            'platform_stats': platform_stats,
            'all_matches': all_matches,
            'best_overall_match': all_matches[0] if all_matches else None,
            'analysis': analysis,
            'search_timestamp': datetime.now().isoformat()
        }
    
    def _analyze_search_results(self, matches: List[Dict], platform_stats: Dict) -> Dict:
        """
        Analysera sökresultat
        
        Args:
            matches (List[Dict]): Alla matchningar
            platform_stats (Dict): Plattformsstatistik
        
        Returns:
            Dict: Analysresultat
        """
        if not matches:
            return {'conclusion': 'Inga matchningar hittades'}
        
        # Beräkna statistik
        similarities = [match['similarity_score'] for match in matches]
        confidences = [match['match_confidence'] for match in matches]
        
        # Analysera plattformsfördelning
        platform_distribution = {}
        for match in matches:
            platform = match['platform']
            if platform not in platform_distribution:
                platform_distribution[platform] = 0
            platform_distribution[platform] += 1
        
        # Generera insikter
        insights = []
        if max(similarities) > 0.9:
            insights.append("Hög sannolikhet för identisk person")
        elif max(similarities) > 0.7:
            insights.append("Möjlig matchning - kräver manuell verifiering")
        else:
            insights.append("Låg sannolikhet för matchning")
        
        return {
            'average_similarity': np.mean(similarities),
            'max_similarity': max(similarities),
            'average_confidence': np.mean(confidences),
            'platform_distribution': platform_distribution,
            'insights': insights,
            'recommendation': self._generate_search_recommendation(matches)
        }
    
    def _generate_search_recommendation(self, matches: List[Dict]) -> str:
        """
        Generera rekommendation baserat på sökresultat
        
        Args:
            matches (List[Dict]): Sökresultat
        
        Returns:
            str: Rekommendation
        """
        if not matches:
            return "Inga matchningar hittades - personen kanske inte finns på dessa plattformar"
        
        best_match = matches[0]
        similarity = best_match['similarity_score']
        confidence = best_match['match_confidence']
        
        if similarity > 0.9 and confidence > 0.8:
            return "Hög sannolikhet för matchning - rekommenderar manuell verifiering"
        elif similarity > 0.7:
            return "Möjlig matchning - rekommenderar ytterligare analys"
        else:
            return "Låg sannolikhet för matchning - överväg andra sökstrategier"
    
    def _save_search_results(self, image_path: str, results: Dict):
        """
        Spara sökresultat
        
        Args:
            image_path (str): Sökväg till ursprungsbild
            results (Dict): Sökresultat
        """
        try:
            # Skapa unikt ID för sökningen
            search_id = hashlib.md5(f"{image_path}_{datetime.now()}".encode()).hexdigest()[:8]
            
            # Spara i databas
            self.data_manager.save_search_result(search_id, image_path, results)
            
            logger.info(f"Sparade sökresultat med ID: {search_id}")
            
        except Exception as e:
            logger.error(f"Fel vid sparande av sökresultat: {str(e)}")
    
    def get_search_history(self, limit: int = 10) -> List[Dict]:
        """
        Hämta sökhistorik
        
        Args:
            limit (int): Max antal sökningar att hämta
        
        Returns:
            List[Dict]: Sökhistorik
        """
        try:
            return self.data_manager.get_search_history(limit)
        except Exception as e:
            logger.error(f"Fel vid hämtning av sökhistorik: {str(e)}")
            return []
    
    def export_search_results(self, search_id: str, format: str = 'json') -> str:
        """
        Exportera sökresultat
        
        Args:
            search_id (str): ID för sökning
            format (str): Exportformat
        
        Returns:
            str: Sökväg till exporterad fil
        """
        try:
            return self.data_manager.export_search_result(search_id, format)
        except Exception as e:
            logger.error(f"Fel vid export av sökresultat: {str(e)}")
            return ""
