<<<<<<< HEAD
# Digital Identitet och Sociala Medier - Forskning med Ansiktsigenkänning

## Projektöversikt

Detta forskningsprojekt fokuserar på att analysera hur människor presenteras online genom avancerad ansiktsigenkänningsteknik. Verktyget identifierar unika ansiktsdrag från bilder och matchar dem mot offentligt tillgänglig data från sociala medier för att studera trender i digital identitet.

**Ny funktion: Reverse Image Search** - Användare kan ladda upp en bild och verktyget söker efter matchande ansikten på sociala medier för att förstå hur ofta samma person förekommer på olika plattformar.

## Målsättning

- Analysera hur individer representerar sig själva på olika sociala medieplattformar
- Utforska trender i digital identitet och självpresentation
- **Reverse Image Search**: Matcha ansikten över plattformar för att studera identitetskonsistens
- Utveckla verktyg för akademiker och marknadsforskare
- Bidra till forskningen om digital identitet och sociala medier

## Funktioner

### Grundläggande Funktioner
- **Ansiktsigenkänning**: Identifiera och extrahera ansiktsdrag från bilder
- **Social Media Integration**: Hämta data från Twitter, Instagram, Facebook
- **Dataanalys**: Analysera mönster i digital identitet
- **Visualisering**: Presentera resultat på ett begripligt sätt
- **Lokal databehandling**: All datahantering sker lokalt för integritet

### Reverse Image Search
- **Bilduppladdning**: Ladda upp en bild för att söka efter matchningar
- **Korsplattformssökning**: Sök efter samma person på olika sociala medier
- **Similaritetsanalys**: Beräkna hur lika ansikten är mellan plattformar
- **Matchningskonfidens**: Bedöm sannolikheten för att det är samma person
- **Sökhistorik**: Håll koll på tidigare sökningar och resultat

## Projektstruktur

```
digital_identity_research/
├── src/
│   ├── face_recognition/     # Ansiktsigenkänning moduler
│   │   ├── face_detector.py           # Grundläggande ansiktsdetektering
│   │   └── reverse_image_search.py    # Reverse image search funktionalitet
│   ├── data_processing/     # Datahantering och rensning
│   │   ├── data_manager.py           # Huvuddatahantering
│   │   └── search_manager.py         # Sökhantering och indexering
│   ├── social_media_apis/   # API-integrationer
│   ├── analysis/            # Analysalgoritmer
│   └── visualization/       # Visualiseringsverktyg
├── data/
│   ├── raw/                # Rådata från sociala medier
│   ├── processed/          # Bearbetad data
│   └── results/            # Analysresultat
├── config/                 # Konfigurationsfiler
├── docs/                   # Dokumentation
├── tests/                  # Testfiler
├── examples/               # Exempelanvändning
│   ├── basic_usage.py              # Grundläggande användning
│   └── reverse_image_search_example.py  # Reverse image search exempel
└── requirements/           # Kravspecifikationer
```

## Teknisk Stack

- **Python 3.8+**
- **OpenCV** för bildbehandling
- **Face Recognition** bibliotek
- **TensorFlow/PyTorch** för maskinlärning
- **Pandas/NumPy** för dataanalys
- **Matplotlib/Seaborn** för visualisering
- **Requests** för API-anrop
- **SQLite** för lokal databas

## Installation

1. Klona projektet
2. Installera beroenden: `pip install -r requirements.txt`
3. Konfigurera API-nycklar i `config/api_keys.json`
4. Kör huvudprogrammet: `python src/main.py`

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
print(f"Bästa matchning: {best_match['similarity_score']:.2f} similaritet")
```

### Kommandorad

```bash
# Kör huvudprogrammet
python src/main.py

# Kör exempel
python examples/basic_usage.py
python examples/reverse_image_search_example.py
```

## Reverse Image Search - Detaljerad Guide

### 1. Förberedelse
- Indexera befintliga ansikten från sociala medier
- Konfigurera similaritetströsklar
- Ställ in plattformar att söka på

### 2. Sökprocess
- Ladda upp en bild med ansikte
- Verktyget analyserar ansiktsdrag
- Jämför med indexerade ansikten
- Beräknar similaritetspoäng

### 3. Resultatanalys
- **Similaritetspoäng**: Hur lika ansikten är (0-1)
- **Matchningskonfidens**: Sannolikhet för korrekt matchning
- **Plattformsfördelning**: Var matchningar hittades
- **Insikter**: Automatiska rekommendationer

### 4. Användningsfall
- **Identitetsverifiering**: Kontrollera om samma person finns på flera plattformar
- **Forskning**: Studera hur människor presenterar sig olika på olika plattformar
- **Marknadsanalys**: Förstå användarrepresentation över plattformar
- **Säkerhet**: Identifiera potentiella identitetsbedrägerier

## Dataintegritet

- All data lagras lokalt
- Ingen data delas med tredje part
- GDPR-kompatibel hantering
- Krypterad lagring av känslig data
- **Reverse Image Search**: Endast offentligt tillgänglig data används

## Etiska överväganden

### Reverse Image Search
- **Transparens**: Användare informeras om sökfunktionalitet
- **Integritet**: Endast offentligt tillgänglig data används
- **Ansvar**: Användare ansvarar för etisk användning
- **Säkerhet**: Data krypteras och lagras lokalt

### Forskning
- **Samtycke**: Endast data från användare som samtyckt
- **Anonymisering**: Känslig data anonymiseras
- **Transparens**: Öppen källkod för granskning
- **Etik**: Följer etiska riktlinjer för forskning

## Bidrag

Detta är ett forskningsprojekt. För att bidra:

1. Forka projektet
2. Skapa en feature branch
3. Commita dina ändringar
4. Skapa en Pull Request

## Licens

MIT License - se LICENSE fil för detaljer

## Kontakt

För frågor om projektet, kontakta projektledaren.

## Viktiga överväganden

- **Etik**: Projektet följer etiska riktlinjer för forskning
- **Integritet**: Respekterar användarnas integritet
- **Transparens**: Öppen källkod för granskning
- **Ansvar**: Ansvarstagande för dataanvändning
- **Reverse Image Search**: Används endast för forskning och etiska ändamål
=======
# Matrix-Legal

Detta repo innehåller de juridiska dokument som krävs för Meta/Facebook-apparna:

- **Privacy Policy:** [privacy.html](https://atinking.github.io/Matrix-Legal/privacy.html)  
- **Data Deletion Instructions:** [data-deletion.html](https://atinking.github.io/Matrix-Legal/data-deletion.html)  

## Syfte
Repon används för att tillhandahålla öppet tillgängliga länkar för Meta Developer Console, så att vår app **Matrix** kan godkännas för inloggning via Facebook/Instagram.

## Kontakt
För frågor kring data eller integritet:  
📧 lunsat14@gmail.com
>>>>>>> fffcdc084d7c3904d17464b35881276618aecc6d
