#!/usr/bin/env python3
"""
Test för att verifiera att installationen fungerar
"""

import sys
import os
from pathlib import Path

# Lägg till src-katalogen i Python-sökvägen
sys.path.append(str(Path(__file__).parent / "src"))

def test_imports():
    """Testa att alla moduler kan importeras"""
    print("Testar imports...")
    
    try:
        from src.main import DigitalIdentityResearch
        print("✓ DigitalIdentityResearch importerad")
    except ImportError as e:
        print(f"✗ Fel vid import av DigitalIdentityResearch: {e}")
        return False
    
    try:
        from src.face_recognition.face_detector import FaceDetector
        print("✓ FaceDetector importerad")
    except ImportError as e:
        print(f"✗ Fel vid import av FaceDetector: {e}")
        return False
    
    try:
        from src.social_media_apis.social_media_manager import SocialMediaManager
        print("✓ SocialMediaManager importerad")
    except ImportError as e:
        print(f"✗ Fel vid import av SocialMediaManager: {e}")
        return False
    
    try:
        from src.analysis.identity_analyzer import IdentityAnalyzer
        print("✓ IdentityAnalyzer importerad")
    except ImportError as e:
        print(f"✗ Fel vid import av IdentityAnalyzer: {e}")
        return False
    
    try:
        from src.data_processing.data_manager import DataManager
        print("✓ DataManager importerad")
    except ImportError as e:
        print(f"✗ Fel vid import av DataManager: {e}")
        return False
    
    try:
        from src.visualization.report_generator import ReportGenerator
        print("✓ ReportGenerator importerad")
    except ImportError as e:
        print(f"✗ Fel vid import av ReportGenerator: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Testa grundläggande funktionalitet"""
    print("\nTestar grundläggande funktionalitet...")
    
    try:
        from src.main import DigitalIdentityResearch
        
        # Initiera forskningsprojektet
        research = DigitalIdentityResearch()
        print("✓ DigitalIdentityResearch initierad")
        
        # Testa att hämta statistik
        stats = research.get_search_statistics()
        print(f"✓ Sökstatistik hämtad: {len(stats)} poster")
        
        return True
        
    except Exception as e:
        print(f"✗ Fel vid test av grundfunktionalitet: {e}")
        return False

def test_file_structure():
    """Testa att filstrukturen är korrekt"""
    print("\nTestar filstruktur...")
    
    required_files = [
        "src/main.py",
        "src/face_recognition/face_detector.py",
        "src/face_recognition/reverse_image_search.py",
        "src/social_media_apis/social_media_manager.py",
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
    print("=== Test av Digital Identitetsforskning Installation ===")
    print()
    
    # Testa filstruktur
    if not test_file_structure():
        print("\n❌ Filstrukturstest misslyckades")
        return False
    
    # Testa imports
    if not test_imports():
        print("\n❌ Importtest misslyckades")
        return False
    
    # Testa grundfunktionalitet
    if not test_basic_functionality():
        print("\n❌ Funktionalitetstest misslyckades")
        return False
    
    print("\n✅ Alla tester godkända!")
    print("Projektet är redo att användas.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
