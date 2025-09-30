#!/usr/bin/env python3
"""
Exempel på Reverse Image Search för digital identitetsforskning
"""

import sys
from pathlib import Path

# Lägg till src-katalogen i Python-sökvägen
sys.path.append(str(Path(__file__).parent.parent / "src"))

from face_recognition.face_detector import FaceDetector
from face_recognition.reverse_image_search import ReverseImageSearch
from social_media_apis.social_media_manager import SocialMediaManager
from data_processing.data_manager import DataManager
from data_processing.search_manager import SearchManager

def main():
    """Exempel på Reverse Image Search"""
    print("=== Reverse Image Search - Exempel ===")
    print()
    
    # 1. Initiera komponenter
    print("1. Initierar komponenter...")
    face_detector = FaceDetector()
    social_manager = SocialMediaManager()
    data_manager = DataManager()
    search_manager = SearchManager()
    
    # Initiera reverse image search
    reverse_search = ReverseImageSearch(face_detector, social_manager, data_manager)
    
    print("✓ Alla komponenter initierade")
    print()
    
    # 2. Simulera indexering av befintliga ansikten
    print("2. Indexerar befintliga ansikten...")
    
    # Simulera befintliga ansikten från olika plattformar
    sample_faces = [
        {
            'face_id': 'twitter_user1_face1',
            'platform': 'twitter',
            'user_id': 'user1',
            'encoding': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            'quality_score': 0.85
        },
        {
            'face_id': 'instagram_user1_face1',
            'platform': 'instagram',
            'user_id': 'user1',
            'encoding': [0.11, 0.21, 0.31, 0.41, 0.51, 0.61, 0.71, 0.81, 0.91, 1.01],
            'quality_score': 0.90
        },
        {
            'face_id': 'facebook_user2_face1',
            'platform': 'facebook',
            'user_id': 'user2',
            'encoding': [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
            'quality_score': 0.75
        }
    ]
    
    # Indexera ansikten
    for face in sample_faces:
        search_manager.add_face_to_index(
            face['face_id'],
            face['platform'],
            face['user_id'],
            face['encoding'],
            face['quality_score']
        )
    
    print(f"✓ Indexerade {len(sample_faces)} ansikten")
    print()
    
    # 3. Simulera reverse image search
    print("3. Simulerar reverse image search...")
    
    # Skapa en testbild (simulerad)
    test_image_path = "data/raw/test_search_image.jpg"
    
    # Simulera ansiktsanalys av testbilden
    test_face_features = [
        {
            'face_id': 0,
            'location': {'top': 100, 'right': 200, 'bottom': 300, 'left': 50},
            'encoding': [0.12, 0.22, 0.32, 0.42, 0.52, 0.62, 0.72, 0.82, 0.92, 1.02],
            'confidence': 0.88,
            'image_path': test_image_path
        }
    ]
    
    # Simulera sökresultat
    search_results = {
        'total_matches': 2,
        'platform_stats': {
            'twitter': {'matches_found': 1, 'total_searched': 1, 'best_match': None},
            'instagram': {'matches_found': 1, 'total_searched': 1, 'best_match': None}
        },
        'all_matches': [
            {
                'similarity_score': 0.85,
                'uploaded_face_id': 0,
                'existing_face': sample_faces[0],
                'platform': 'twitter',
                'match_confidence': 0.82
            },
            {
                'similarity_score': 0.78,
                'uploaded_face_id': 0,
                'existing_face': sample_faces[1],
                'platform': 'instagram',
                'match_confidence': 0.75
            }
        ],
        'best_overall_match': {
            'similarity_score': 0.85,
            'platform': 'twitter',
            'match_confidence': 0.82
        },
        'analysis': {
            'average_similarity': 0.815,
            'max_similarity': 0.85,
            'platform_distribution': {'twitter': 1, 'instagram': 1},
            'insights': ['Hög sannolikhet för identisk person'],
            'recommendation': 'Hög sannolikhet för matchning - rekommenderar manuell verifiering'
        },
        'search_timestamp': '2024-01-01T12:00:00Z'
    }
    
    print("✓ Reverse image search simulerad")
    print(f"  - Totalt antal matchningar: {search_results['total_matches']}")
    print(f"  - Bästa similaritet: {search_results['best_overall_match']['similarity_score']:.2f}")
    print(f"  - Bästa plattform: {search_results['best_overall_match']['platform']}")
    print()
    
    # 4. Analysera resultat
    print("4. Analyserar sökresultat...")
    
    analysis = search_results['analysis']
    print(f"  - Genomsnittlig similaritet: {analysis['average_similarity']:.2f}")
    print(f"  - Maximal similaritet: {analysis['max_similarity']:.2f}")
    print(f"  - Plattformsfördelning: {analysis['platform_distribution']}")
    print(f"  - Rekommendation: {analysis['recommendation']}")
    print()
    
    # 5. Visa matchningar
    print("5. Detaljerade matchningar:")
    for i, match in enumerate(search_results['all_matches'], 1):
        print(f"  Match {i}:")
        print(f"    - Plattform: {match['platform']}")
        print(f"    - Similaritet: {match['similarity_score']:.2f}")
        print(f"    - Konfidens: {match['match_confidence']:.2f}")
        print(f"    - Användar-ID: {match['existing_face']['user_id']}")
        print()
    
    # 6. Spara sökresultat
    print("6. Sparar sökresultat...")
    
    # Simulera sparande av sökresultat
    search_id = "search_12345"
    search_manager.save_search_result(search_id, test_image_path, search_results)
    
    print("✓ Sökresultat sparade")
    print()
    
    # 7. Visa sökhistorik
    print("7. Sökhistorik:")
    history = search_manager.get_search_history(5)
    for search in history:
        print(f"  - {search['search_id']}: {search['total_matches']} matchningar")
    print()
    
    # 8. Visa statistik
    print("8. Sökstatistik:")
    stats = search_manager.get_search_statistics()
    for key, value in stats.items():
        print(f"  - {key}: {value}")
    
    print()
    print("=== Reverse Image Search Exempel Slutfört ===")
    print("Kontrollera 'data/' mappen för resultat")

if __name__ == "__main__":
    main()
