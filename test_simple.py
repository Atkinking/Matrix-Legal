#!/usr/bin/env python3
"""
Enkel test för att verifiera att projektstrukturen fungerar
"""

import sys
import os
from pathlib import Path

# Lägg till src-katalogen i Python-sökvägen
sys.path.append(str(Path(__file__).parent / "src"))

def test_simple_imports():
    """Testa att enkla moduler kan importeras"""
    print("Testar enkla imports...")
    
    try:
        from src.face_recognition.face_detector_simple import FaceDetector
        print("✓ FaceDetector (enkel) importerad")
        
        # Testa initiering
        detector = FaceDetector()
        print("✓ FaceDetector initierad")
        
    except ImportError as e:
        print(f"✗ Fel vid import av FaceDetector: {e}")
        return False
    except Exception as e:
        print(f"✗ Fel vid initiering av FaceDetector: {e}")
        return False
    
    try:
        from src.social_media_apis.social_media_manager_simple import SocialMediaManager
        print("✓ SocialMediaManager (enkel) importerad")
        
        # Testa initiering
        manager = SocialMediaManager()
        print("✓ SocialMediaManager initierad")
        
    except ImportError as e:
        print(f"✗ Fel vid import av SocialMediaManager: {e}")
        return False
    except Exception as e:
        print(f"✗ Fel vid initiering av SocialMediaManager: {e}")
        return False
    
    return True

def test_main_simple():
    """Testa enkel huvudklass"""
    print("\nTestar enkel huvudklass...")
    
    try:
        from src.main_simple import DigitalIdentityResearch
        
        # Initiera forskningsprojektet
        research = DigitalIdentityResearch()
        print("✓ DigitalIdentityResearch (enkel) initierad")
        
        # Testa grundfunktionalitet
        results = research.analyze_user_identity("test_user", ["twitter"])
        print(f"✓ Användaranalys testad: {results['username']}")
        
        # Testa reverse image search
        search_results = research.reverse_image_search("test_image.jpg", ["twitter"])
        print(f"✓ Reverse image search testad: {search_results['total_matches']} matchningar")
        
        # Testa statistik
        stats = research.get_search_statistics()
        print(f"✓ Statistik hämtad: {stats['total_searches']} sökningar")
        
        return True
        
    except Exception as e:
        print(f"✗ Fel vid test av huvudklass: {e}")
        return False

def test_basic_functionality():
    """Testa grundläggande funktionalitet"""
    print("\nTestar grundläggande funktionalitet...")
    
    try:
        from src.face_recognition.face_detector_simple import FaceDetector
        from src.social_media_apis.social_media_manager_simple import SocialMediaManager
        
        # Testa ansiktsdetektering
        detector = FaceDetector()
        faces = detector.detect_faces("test_image.jpg")
        print(f"✓ Ansiktsdetektering testad: {len(faces)} ansikten")
        
        # Testa social media manager
        manager = SocialMediaManager()
        data = manager.get_user_data("test_user", "twitter")
        print(f"✓ Social media data hämtad: {data['username']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Fel vid test av grundfunktionalitet: {e}")
        return False

def test_file_structure():
    """Testa att filstrukturen är korrekt"""
    print("\nTestar filstruktur...")
    
    required_files = [
        "src/main.py",
        "src/main_simple.py",
        "src/face_recognition/face_detector.py",
        "src/face_recognition/face_detector_simple.py",
        "src/social_media_apis/social_media_manager.py",
        "src/social_media_apis/social_media_manager_simple.py",
        "src/analysis/identity_analyzer.py",
        "src/data_processing/data_manager.py",
        "src/data_processing/search_manager.py",
        "src/visualization/report_generator.py",
        "config/settings.yaml",
        "config/api_keys.json",
        "requirements.txt",
        "README.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✓ {file_path} finns")
    
    if missing_files:
        print(f"✗ Saknade filer: {missing_files}")
        return False
    
    return True

def main():
    """Huvudtestfunktion"""
    print("=== Enkel Test av Digital Identitetsforskning ===")
    print()
    
    # Testa filstruktur
    if not test_file_structure():
        print("\n❌ Filstrukturstest misslyckades")
        return False
    
    # Testa imports
    if not test_simple_imports():
        print("\n❌ Importtest misslyckades")
        return False
    
    # Testa huvudklass
    if not test_main_simple():
        print("\n❌ Huvudklassstest misslyckades")
        return False
    
    # Testa grundfunktionalitet
    if not test_basic_functionality():
        print("\n❌ Funktionalitetstest misslyckades")
        return False
    
    print("\n✅ Alla enkla tester godkända!")
    print("Projektstrukturen fungerar korrekt.")
    print("\nFör full funktionalitet, installera beroenden med:")
    print("pip install -r requirements.txt")
    print("\nFör att köra enkel version:")
    print("python3 src/main_simple.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
