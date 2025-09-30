# 🔑 Så här får du riktiga API-nycklar

## 📱 Instagram API

### 1. Gå till Facebook for Developers
- Besök: https://developers.facebook.com/
- Logga in med ditt Facebook-konto

### 2. Skapa en app
- Klicka "Create App"
- Välj "Consumer" eller "Business"
- Fyll i app-information

### 3. Lägg till Instagram Basic Display
- Gå till "Add Product"
- Välj "Instagram Basic Display"
- Klicka "Set Up"

### 4. Få din access token
- Gå till "Instagram Basic Display" > "Basic Display"
- Klicka "Create New App"
- Fyll i OAuth Redirect URIs
- Kopiera din Client ID och Client Secret

### 5. Testa din access token
- Använd Instagram Basic Display API
- URL: https://graph.instagram.com/me?fields=id,username&access_token=YOUR_TOKEN

## 📘 Facebook API

### 1. Gå till Facebook for Developers
- Besök: https://developers.facebook.com/
- Logga in med ditt Facebook-konto

### 2. Skapa en app
- Klicka "Create App"
- Välj "Consumer" eller "Business"
- Fyll i app-information

### 3. Lägg till Facebook Login
- Gå till "Add Product"
- Välj "Facebook Login"
- Klicka "Set Up"

### 4. Få din access token
- Gå till "Facebook Login" > "Settings"
- Lägg till Valid OAuth Redirect URIs
- Kopiera din App ID och App Secret

### 5. Testa din access token
- Använd Facebook Graph API
- URL: https://graph.facebook.com/me?access_token=YOUR_TOKEN

## 🔧 Konfigurera API-nycklar

### 1. Redigera config/api_keys.json
```json
{
  "instagram": {
    "access_token": "DIN_RIKTIGA_INSTAGRAM_TOKEN",
    "client_id": "DIN_RIKTIGA_INSTAGRAM_CLIENT_ID",
    "client_secret": "DIN_RIKTIGA_INSTAGRAM_CLIENT_SECRET"
  },
  "facebook": {
    "access_token": "DIN_RIKTIGA_FACEBOOK_TOKEN",
    "app_id": "DIN_RIKTIGA_FACEBOOK_APP_ID",
    "app_secret": "DIN_RIKTIGA_FACEBOOK_APP_SECRET"
  }
}
```

### 2. Testa API:erna
```bash
python3 real_api_search.py
```

## ⚠️ Viktiga saker att komma ihåg

1. **Tillstånd krävs** - Du behöver tillstånd från användare för att hämta deras data
2. **Rate limits** - API:erna har begränsningar på antal förfrågningar
3. **Sekretess** - Följ GDPR och andra sekretessregler
4. **Användarvillkor** - Läs och följ plattformarnas användarvillkor

## 🚀 Nästa steg

1. Skaffa API-nycklar enligt instruktionerna ovan
2. Fyll i dina riktiga nycklar i config/api_keys.json
3. Kör python3 real_api_search.py
4. Få riktiga matchningar från Instagram och Facebook!
