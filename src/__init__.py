"""
Digital Identitetsforskning - Huvudmodul
"""

__version__ = "1.0.0"
__author__ = "Forskningsteam"
__description__ = "Forskning om digital identitet och sociala medier med ansiktsigenkänning"

# Importera huvudklasser för enkel användning
from .main import DigitalIdentityResearch
from .face_recognition.face_detector import FaceDetector
from .face_recognition.reverse_image_search import ReverseImageSearch
from .social_media_apis.social_media_manager import SocialMediaManager
from .analysis.identity_analyzer import IdentityAnalyzer
from .data_processing.data_manager import DataManager
from .data_processing.search_manager import SearchManager
from .visualization.report_generator import ReportGenerator

__all__ = [
    'DigitalIdentityResearch',
    'FaceDetector',
    'ReverseImageSearch',
    'SocialMediaManager',
    'IdentityAnalyzer',
    'DataManager',
    'SearchManager',
    'ReportGenerator'
]
