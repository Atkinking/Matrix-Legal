# 🚀 Snabbaste sättet att fixa Facebook API

## B) GitHub Pages (REKOMMENDERAT - Gratis & snabbt)

### 1. Skapa GitHub repo
```bash
# Gå till GitHub.com
# Skapa nytt repo: "facebook-legal-pages"
# Välj "Public"
# Lägg till README
```

### 2. Skapa privacy.html
```html
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy - Digital Identity Research</title>
</head>
<body>
    <h1>Privacy Policy</h1>
    <p>Denna app samlar in och använder personuppgifter enligt GDPR.</p>
    <p>Vi samlar in: bilder, ansiktsdata, användarinformation.</p>
    <p>Kontakt: din-email@example.com</p>
</body>
</html>
```

### 3. Skapa data-deletion.html
```html
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Deletion - Digital Identity Research</title>
</head>
<body>
    <h1>Data Deletion Policy</h1>
    <p>Användare kan begära radering av sina data.</p>
    <p>Kontakt: din-email@example.com</p>
    <p>Vi raderar data inom 30 dagar.</p>
</body>
</html>
```

### 4. Aktivera GitHub Pages
- Gå till repo settings
- Scrolla ner till "Pages"
- Välj "Deploy from a branch"
- Välj "main" branch
- Välj "/ (root)" folder
- Klicka "Save"

### 5. Få dina URL:er
```
https://dittnamn.github.io/facebook-legal-pages/privacy.html
https://dittnamn.github.io/facebook-legal-pages/data-deletion.html
```

## 🔧 Facebook App Setup

### 1. Gå till Facebook for Developers
- https://developers.facebook.com/
- Logga in med ditt Facebook-konto

### 2. Skapa ny app
- Klicka "Create App"
- Välj "Consumer" eller "Business"
- App namn: "Digital Identity Research"
- App kontakt email: din-email@example.com

### 3. Lägg till Facebook Login
- Gå till "Add Product"
- Välj "Facebook Login"
- Klicka "Set Up"

### 4. Konfigurera OAuth Redirect URIs
- Gå till "Facebook Login" > "Settings"
- Lägg till Valid OAuth Redirect URIs:
  - http://localhost:8000/auth/facebook/callback
  - https://dittnamn.github.io/facebook-legal-pages/

### 5. Lägg till App Domains
- Gå till "Settings" > "Basic"
- Lägg till App Domains:
  - localhost
  - dittnamn.github.io

### 6. Fyll i Privacy Policy URL
- Privacy Policy URL: https://dittnamn.github.io/facebook-legal-pages/privacy.html
- Data Deletion URL: https://dittnamn.github.io/facebook-legal-pages/data-deletion.html

### 7. Få din access token
- Gå till "Tools" > "Graph API Explorer"
- Välj din app
- Generera access token
- Kopiera token

## 🔑 Uppdatera config/api_keys.json

```json
{
  "facebook": {
    "access_token": "DIN_RIKTIGA_FACEBOOK_TOKEN",
    "app_id": "DIN_RIKTIGA_FACEBOOK_APP_ID",
    "app_secret": "DIN_RIKTIGA_FACEBOOK_APP_SECRET"
  }
}
```

## 🚀 Testa systemet

```bash
python3 real_api_search.py
```

## ⚠️ Viktiga saker

1. **App Review** - Du behöver godkännande för produktion
2. **Rate Limits** - Facebook har begränsningar
3. **Permissions** - Behöver rätt behörigheter
4. **Testing** - Testa med ditt eget konto först

## 📞 Support

Om du behöver hjälp:
- Facebook Developer Docs: https://developers.facebook.com/docs/
- Facebook Community: https://developers.facebook.com/community/
