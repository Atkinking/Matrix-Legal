"""
Ansiktsigenkänningsmodul för digital identitetsforskning
"""

import cv2
import face_recognition
import numpy as np
from PIL import Image
import logging
from typing import List, Dict, Tuple, Optional
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class FaceDetector:
    """Klass för ansiktsigenkänning och analys"""
    
    def __init__(self, model='hog'):
        """
        Initiera ansiktsdetektor
        
        Args:
            model (str): Modell att använda ('hog' eller 'cnn')
        """
        self.model = model
        self.known_faces = {}
        self.face_encodings = {}
        
        logger.info(f"FaceDetector initierad med modell: {model}")
    
    def detect_faces(self, image_path: str) -> List[Dict]:
        """
        Detektera ansikten i en bild
        
        Args:
            image_path (str): Sökväg till bildfil
        
        Returns:
            List[Dict]: Lista över detekterade ansikten med metadata
        """
        try:
            # Ladda bild
            image = face_recognition.load_image_file(image_path)
            
            # Hitta ansiktsplatser
            face_locations = face_recognition.face_locations(image, model=self.model)
            
            # Hitta ansiktsencodingar
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            faces = []
            for i, (face_location, face_encoding) in enumerate(zip(face_locations, face_encodings)):
                top, right, bottom, left = face_location
                
                face_data = {
                    'face_id': i,
                    'location': {
                        'top': top,
                        'right': right,
                        'bottom': bottom,
                        'left': left
                    },
                    'encoding': face_encoding.tolist(),
                    'confidence': self._calculate_confidence(face_encoding),
                    'image_path': image_path
                }
                
                faces.append(face_data)
            
            logger.info(f"Detekterade {len(faces)} ansikten i {image_path}")
            return faces
            
        except Exception as e:
            logger.error(f"Fel vid ansiktsdetektering i {image_path}: {str(e)}")
            return []
    
    def analyze_images(self, image_paths: List[str]) -> Dict:
        """
        Analysera flera bilder för ansiktsdrag
        
        Args:
            image_paths (List[str]): Lista över bildsökvägar
        
        Returns:
            Dict: Analysresultat för alla bilder
        """
        logger.info(f"Analyserar {len(image_paths)} bilder")
        
        all_faces = []
        face_encodings = []
        
        for image_path in image_paths:
            if not os.path.exists(image_path):
                logger.warning(f"Bildfil finns inte: {image_path}")
                continue
            
            faces = self.detect_faces(image_path)
            all_faces.extend(faces)
            
            # Samla encodingar för jämförelse
            for face in faces:
                face_encodings.append(face['encoding'])
        
        # Analysera mönster
        analysis = self._analyze_face_patterns(all_faces, face_encodings)
        
        return {
            'total_images': len(image_paths),
            'total_faces': len(all_faces),
            'faces': all_faces,
            'analysis': analysis
        }
    
    def _analyze_face_patterns(self, faces: List[Dict], encodings: List[List[float]]) -> Dict:
        """
        Analysera mönster i ansiktsdrag
        
        Args:
            faces (List[Dict]): Lista över ansikten
            encodings (List[List[float]]): Ansiktsencodingar
        
        Returns:
            Dict: Analysresultat
        """
        if not encodings:
            return {'error': 'Inga ansiktsencodingar att analysera'}
        
        # Konvertera till numpy array
        encodings_array = np.array(encodings)
        
        # Beräkna genomsnittlig encoding
        mean_encoding = np.mean(encodings_array, axis=0)
        
        # Beräkna variation
        variance = np.var(encodings_array, axis=0)
        
        # Hitta unika ansikten (baserat på encoding-similaritet)
        unique_faces = self._find_unique_faces(encodings_array)
        
        # Analysera kvalitet
        quality_metrics = self._analyze_face_quality(faces)
        
        return {
            'mean_encoding': mean_encoding.tolist(),
            'variance': variance.tolist(),
            'unique_faces_count': len(unique_faces),
            'quality_metrics': quality_metrics,
            'consistency_score': self._calculate_consistency_score(encodings_array)
        }
    
    def _find_unique_faces(self, encodings: np.ndarray, threshold: float = 0.6) -> List[int]:
        """
        Hitta unika ansikten baserat på encoding-similaritet
        
        Args:
            encodings (np.ndarray): Ansiktsencodingar
            threshold (float): Tröskelvärde för similaritet
        
        Returns:
            List[int]: Index för unika ansikten
        """
        if len(encodings) <= 1:
            return list(range(len(encodings)))
        
        unique_indices = [0]  # Första ansiktet är alltid unikt
        
        for i in range(1, len(encodings)):
            is_unique = True
            for j in unique_indices:
                # Beräkna avstånd mellan encodingar
                distance = np.linalg.norm(encodings[i] - encodings[j])
                if distance < threshold:
                    is_unique = False
                    break
            
            if is_unique:
                unique_indices.append(i)
        
        return unique_indices
    
    def _analyze_face_quality(self, faces: List[Dict]) -> Dict:
        """
        Analysera kvalitet på ansiktsbilder
        
        Args:
            faces (List[Dict]): Lista över ansikten
        
        Returns:
            Dict: Kvalitetsmått
        """
        if not faces:
            return {'error': 'Inga ansikten att analysera'}
        
        confidences = [face['confidence'] for face in faces]
        
        return {
            'average_confidence': np.mean(confidences),
            'min_confidence': np.min(confidences),
            'max_confidence': np.max(confidences),
            'high_quality_count': sum(1 for c in confidences if c > 0.8),
            'medium_quality_count': sum(1 for c in confidences if 0.5 <= c <= 0.8),
            'low_quality_count': sum(1 for c in confidences if c < 0.5)
        }
    
    def _calculate_confidence(self, encoding: np.ndarray) -> float:
        """
        Beräkna konfidensgrad för ansiktsencoding
        
        Args:
            encoding (np.ndarray): Ansiktsencoding
        
        Returns:
            float: Konfidensgrad (0-1)
        """
        # Enkel heuristik baserad på encoding-storlek och värden
        norm = np.linalg.norm(encoding)
        confidence = min(1.0, norm / 10.0)  # Normalisera till 0-1
        return confidence
    
    def _calculate_consistency_score(self, encodings: np.ndarray) -> float:
        """
        Beräkna konsistenspoäng för ansiktsencodingar
        
        Args:
            encodings (np.ndarray): Ansiktsencodingar
        
        Returns:
            float: Konsistenspoäng (0-1)
        """
        if len(encodings) <= 1:
            return 1.0
        
        # Beräkna genomsnittlig avstånd mellan alla par
        distances = []
        for i in range(len(encodings)):
            for j in range(i + 1, len(encodings)):
                distance = np.linalg.norm(encodings[i] - encodings[j])
                distances.append(distance)
        
        if not distances:
            return 1.0
        
        # Konsistens är omvändt proportionell mot genomsnittligt avstånd
        mean_distance = np.mean(distances)
        consistency = max(0.0, 1.0 - mean_distance)
        
        return consistency
    
    def compare_faces(self, encoding1: List[float], encoding2: List[float]) -> float:
        """
        Jämför två ansiktsencodingar
        
        Args:
            encoding1 (List[float]): Första encodingen
            encoding2 (List[float]): Andra encodingen
        
        Returns:
            float: Similaritetspoäng (0-1)
        """
        try:
            # Konvertera till numpy arrays
            enc1 = np.array(encoding1)
            enc2 = np.array(encoding2)
            
            # Beräkna avstånd
            distance = np.linalg.norm(enc1 - enc2)
            
            # Konvertera till similaritetspoäng
            similarity = max(0.0, 1.0 - distance)
            
            return similarity
            
        except Exception as e:
            logger.error(f"Fel vid ansiktsjämförelse: {str(e)}")
            return 0.0
    
    def save_face_encoding(self, face_id: str, encoding: List[float]):
        """
        Spara ansiktsencoding för framtida användning
        
        Args:
            face_id (str): Unikt ID för ansiktet
            encoding (List[float]): Ansiktsencoding
        """
        self.face_encodings[face_id] = encoding
        logger.info(f"Sparade encoding för ansikt {face_id}")
    
    def load_known_faces(self, faces_file: str):
        """
        Ladda kända ansikten från fil
        
        Args:
            faces_file (str): Sökväg till fil med kända ansikten
        """
        try:
            import json
            with open(faces_file, 'r') as f:
                self.known_faces = json.load(f)
            logger.info(f"Laddade {len(self.known_faces)} kända ansikten")
        except Exception as e:
            logger.error(f"Fel vid laddning av kända ansikten: {str(e)}")
    
    def save_known_faces(self, faces_file: str):
        """
        Spara kända ansikten till fil
        
        Args:
            faces_file (str): Sökväg till fil att spara till
        """
        try:
            import json
            with open(faces_file, 'w') as f:
                json.dump(self.known_faces, f, indent=2)
            logger.info(f"Sparade {len(self.known_faces)} kända ansikten")
        except Exception as e:
            logger.error(f"Fel vid sparande av kända ansikten: {str(e)}")
