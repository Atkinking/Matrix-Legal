#!/usr/bin/env python3
"""
Exempel på grundläggande användning av Digital Identitetsforskning
"""

import sys
from pathlib import Path

# Lägg till src-katalogen i Python-sökvägen
sys.path.append(str(Path(__file__).parent.parent / "src"))

from face_recognition.face_detector import FaceDetector
from social_media_apis.social_media_manager import SocialMediaManager
from analysis.identity_analyzer import IdentityAnalyzer
from data_processing.data_manager import DataManager
from visualization.report_generator import ReportGenerator

def main():
    """Exempel på grundläggande användning"""
    print("=== Digital Identitetsforskning - Exempel ===")
    print()
    
    # 1. Initiera komponenter
    print("1. Initierar komponenter...")
    face_detector = FaceDetector()
    social_manager = SocialMediaManager()
    analyzer = IdentityAnalyzer()
    data_manager = DataManager()
    report_generator = ReportGenerator()
    
    print("✓ Alla komponenter initierade")
    print()
    
    # 2. Simulera ansiktsigenkänning
    print("2. Simulerar ansiktsigenkänning...")
    
    # Skapa enkla testdata
    test_images = [
        "data/raw/test_image1.jpg",
        "data/raw/test_image2.jpg"
    ]
    
    # Simulera ansiktsanalys
    face_features = {
        'twitter': {
            'total_images': 2,
            'total_faces': 2,
            'faces': [
                {
                    'face_id': 0,
                    'location': {'top': 100, 'right': 200, 'bottom': 300, 'left': 50},
                    'encoding': [0.1, 0.2, 0.3, 0.4, 0.5],
                    'confidence': 0.85,
                    'image_path': 'data/raw/test_image1.jpg'
                }
            ],
            'analysis': {
                'consistency_score': 0.8,
                'quality_metrics': {
                    'average_confidence': 0.85,
                    'high_quality_count': 1
                }
            }
        }
    }
    
    print("✓ Ansiktsanalys simulerad")
    print()
    
    # 3. Simulera social media data
    print("3. Simulerar social media data...")
    
    social_data = {
        'twitter': {
            'platform': 'twitter',
            'username': 'test_user',
            'user_info': {
                'username': 'test_user',
                'display_name': 'Test User',
                'followers_count': 1000,
                'following_count': 500
            },
            'images': [
                {
                    'url': 'https://example.com/image1.jpg',
                    'timestamp': '2024-01-01T12:00:00Z',
                    'type': 'profile'
                }
            ],
            'timestamp': '2024-01-01T12:00:00Z'
        }
    }
    
    print("✓ Social media data simulerad")
    print()
    
    # 4. Analysera identitet
    print("4. Analyserar digital identitet...")
    
    analysis_results = analyzer.analyze_identity_patterns(social_data, face_features)
    
    print("✓ Identitetsanalys slutförd")
    print(f"  - Identitetspoäng: {analysis_results.get('overall_identity_score', 0):.2f}")
    print()
    
    # 5. Generera rapport
    print("5. Genererar rapport...")
    
    report = report_generator.generate_report(analysis_results)
    
    print("✓ Rapport genererad")
    print(f"  - Sammanfattning: {report.get('summary', {}).get('overall_identity_score', 0):.2f}")
    print()
    
    # 6. Spara data
    print("6. Sparar data...")
    
    # Spara användardata
    data_manager.save_user_data('test_user', 'twitter', social_data['twitter'])
    
    # Spara ansiktsanalys
    for platform, features in face_features.items():
        for face in features.get('faces', []):
            data_manager.save_face_analysis(
                'test_user', 
                face['image_path'], 
                face['encoding'], 
                {'confidence': face['confidence']}
            )
    
    # Spara analysresultat
    data_manager.save_analysis_results('test_user', analysis_results)
    
    print("✓ Data sparad")
    print()
    
    # 7. Visa statistik
    print("7. Data statistik:")
    stats = data_manager.get_statistics()
    for key, value in stats.items():
        print(f"  - {key}: {value}")
    
    print()
    print("=== Exempel slutfört ===")
    print("Kontrollera 'data/' mappen för resultat")

if __name__ == "__main__":
    main()
