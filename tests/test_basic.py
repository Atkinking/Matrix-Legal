"""
Grundläggande tester för Digital Identitetsforskning
"""

import unittest
import sys
import os
from pathlib import Path

# Lägg till src-katalogen i Python-sökvägen
sys.path.append(str(Path(__file__).parent.parent / "src"))

from face_recognition.face_detector import FaceDetector
from social_media_apis.social_media_manager import SocialMediaManager
from analysis.identity_analyzer import IdentityAnalyzer
from data_processing.data_manager import DataManager
from visualization.report_generator import ReportGenerator

class TestBasicFunctionality(unittest.TestCase):
    """Testa grundläggande funktionalitet"""
    
    def test_face_detector_init(self):
        """Testa att FaceDetector kan initieras"""
        detector = FaceDetector()
        self.assertIsNotNone(detector)
        self.assertEqual(detector.model, 'hog')
    
    def test_social_media_manager_init(self):
        """Testa att SocialMediaManager kan initieras"""
        manager = SocialMediaManager()
        self.assertIsNotNone(manager)
        self.assertIsInstance(manager.api_keys, dict)
    
    def test_identity_analyzer_init(self):
        """Testa att IdentityAnalyzer kan initieras"""
        analyzer = IdentityAnalyzer()
        self.assertIsNotNone(analyzer)
        self.assertIsInstance(analyzer.analysis_results, dict)
    
    def test_data_manager_init(self):
        """Testa att DataManager kan initieras"""
        manager = DataManager()
        self.assertIsNotNone(manager)
        self.assertTrue(manager.data_dir.exists())
    
    def test_report_generator_init(self):
        """Testa att ReportGenerator kan initieras"""
        generator = ReportGenerator()
        self.assertIsNotNone(generator)
        self.assertTrue(generator.output_dir.exists())
    
    def test_face_detector_confidence_calculation(self):
        """Testa konfidensberäkning för ansiktsdetektor"""
        detector = FaceDetector()
        
        # Testa med enkla encodingar
        encoding1 = [0.1, 0.2, 0.3, 0.4, 0.5]
        encoding2 = [0.1, 0.2, 0.3, 0.4, 0.5]
        
        similarity = detector.compare_faces(encoding1, encoding2)
        self.assertEqual(similarity, 1.0)  # Identiska encodingar
    
    def test_identity_analyzer_insights(self):
        """Testa insiktsgenerering"""
        analyzer = IdentityAnalyzer()
        
        # Testa med tomma data
        empty_results = {}
        insights = analyzer.generate_insights(empty_results)
        self.assertIsInstance(insights, list)
    
    def test_data_manager_statistics(self):
        """Testa datahanteringsstatistik"""
        manager = DataManager()
        stats = manager.get_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn('users', stats)

if __name__ == '__main__':
    unittest.main()
