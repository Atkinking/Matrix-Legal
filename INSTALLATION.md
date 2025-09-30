# Installation och Setup

## Förutsättningar

- Python 3.8 eller senare
- pip (Python package manager)
- Git (valfritt, för versionshantering)

## Installation

### 1. Klona eller ladda ner projektet

```bash
# Om du använder Git
git clone <repository-url>
cd digital_identity_research

# Eller ladda ner och extrahera ZIP-filen
```

### 2. Skapa virtuell miljö (rekommenderat)

```bash
# Skapa virtuell miljö
python -m venv venv

# Aktivera virtuell miljö
# På macOS/Linux:
source venv/bin/activate

# På Windows:
# venv\Scripts\activate
```

### 3. Installera beroenden

```bash
pip install -r requirements.txt
```

### 4. Konfigurera API-nycklar

Kopiera `config/api_keys.json.example` till `config/api_keys.json` och fyll i dina API-nycklar:

```json
{
  "twitter": {
    "api_key": "din_twitter_api_key",
    "api_secret": "din_twitter_api_secret",
    "access_token": "din_twitter_access_token",
    "access_token_secret": "din_twitter_access_token_secret"
  },
  "instagram": {
    "access_token": "din_instagram_access_token",
    "client_id": "din_instagram_client_id",
    "client_secret": "din_instagram_client_secret"
  },
  "facebook": {
    "access_token": "din_facebook_access_token",
    "app_id": "din_facebook_app_id",
    "app_secret": "din_facebook_app_secret"
  }
}
```

### 5. Testa installationen

```bash
# Kör grundläggande tester
python -m pytest tests/test_basic.py -v

# Kör exempel
python examples/basic_usage.py
python examples/reverse_image_search_example.py
```

## Användning

### Grundläggande användning

```python
from src.main import DigitalIdentityResearch

# Initiera forskningsprojektet
research = DigitalIdentityResearch()

# Analysera en användare
results = research.analyze_user_identity("användarnamn", ["twitter", "instagram"])

# Exportera resultat
research.export_results("json")
```

### Reverse Image Search

```python
# Utför reverse image search
search_results = research.reverse_image_search(
    "path/to/image.jpg", 
    ["twitter", "instagram", "facebook"]
)

# Visa resultat
print(f"Totalt antal matchningar: {search_results['total_matches']}")
best_match = search_results['best_overall_match']
if best_match:
    print(f"Bästa matchning: {best_match['similarity_score']:.2f} similaritet")
    print(f"Plattform: {best_match['platform']}")
```

### Kommandorad

```bash
# Kör huvudprogrammet
python src/main.py

# Kör exempel
python examples/basic_usage.py
python examples/reverse_image_search_example.py
```

## Reverse Image Search - Setup

### 1. Förberedelse

```python
# Indexera befintliga ansikten
research = DigitalIdentityResearch()

# Analysera användare för att bygga index
usernames = ["user1", "user2", "user3"]
platforms = ["twitter", "instagram", "facebook"]

for username in usernames:
    results = research.analyze_user_identity(username, platforms)
    # Ansikten indexeras automatiskt
```

### 2. Konfiguration

```yaml
# config/settings.yaml
face_recognition:
  model: "hog"  # eller "cnn" för bättre precision
  tolerance: 0.6
  max_faces: 10
  image_size: 150

reverse_image_search:
  similarity_threshold: 0.6
  confidence_threshold: 0.7
  max_results: 50
```

### 3. Sökprocess

```python
# Utför sökning
search_results = research.reverse_image_search(
    "path/to/uploaded_image.jpg",
    ["twitter", "instagram", "facebook"]
)

# Analysera resultat
if search_results['total_matches'] > 0:
    best_match = search_results['best_overall_match']
    print(f"Bästa matchning: {best_match['similarity_score']:.2f}")
    print(f"Plattform: {best_match['platform']}")
    print(f"Konfidens: {best_match['match_confidence']:.2f}")
else:
    print("Inga matchningar hittades")
```

## Felsökning

### Vanliga problem

1. **ImportError**: Kontrollera att alla beroenden är installerade
2. **API-fel**: Kontrollera att API-nycklar är korrekt konfigurerade
3. **Databasfel**: Kontrollera att SQLite är installerat
4. **Bildfel**: Kontrollera att bildfiler är i rätt format (JPG, PNG)

### Reverse Image Search specifika problem

1. **Inga matchningar**: Kontrollera att ansikten är indexerade
2. **Låg similaritet**: Justera similaritetströskel i konfiguration
3. **Långsam sökning**: Överväg att använda CNN-modell för bättre precision

### Loggar

Loggar sparas i `research.log` för felsökning.

## Utveckling

### Utvecklingsmiljö

```bash
# Installera utvecklingsberoenden
pip install -r requirements.txt

# Kör tester
python -m pytest tests/ -v

# Kör med coverage
python -m pytest tests/ --cov=src
```

### Reverse Image Search utveckling

```python
# Testa reverse image search
from src.face_recognition.reverse_image_search import ReverseImageSearch
from src.face_recognition.face_detector import FaceDetector
from src.social_media_apis.social_media_manager import SocialMediaManager
from src.data_processing.data_manager import DataManager

# Initiera komponenter
face_detector = FaceDetector()
social_manager = SocialMediaManager()
data_manager = DataManager()
reverse_search = ReverseImageSearch(face_detector, social_manager, data_manager)

# Testa sökning
results = reverse_search.search_face_in_social_media("test_image.jpg", ["twitter"])
```

### Bidrag

1. Forka projektet
2. Skapa en feature branch
3. Commita dina ändringar
4. Skapa en Pull Request

## Support

För frågor och support, kontakta projektledaren eller skapa en issue i projektet.

## Etiska riktlinjer

### Reverse Image Search
- Använd endast för forskning och etiska ändamål
- Respektera användarnas integritet
- Följ plattformens användarvillkor
- Använd endast offentligt tillgänglig data

### Forskning
- Följ etiska riktlinjer för forskning
- Respektera användarnas integritet
- Använd data ansvarsfullt
- Transparens i metodik
