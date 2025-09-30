#!/bin/bash

echo "🚀 GitHub Pages Setup Script"
echo "=============================="

# Kontrollera om git är konfigurerat
echo "📋 Kontrollerar git-konfiguration..."
git config --global user.name "Atkinking"
git config --global user.email "lunsat14@gmail.com"

# Skapa en enkel test-fil
echo "📝 Skapar test-fil för GitHub Pages..."
cat > index.html << 'HTML'
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Pages Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; text-align: center; }
        .success { color: green; font-size: 24px; }
    </style>
</head>
<body>
    <h1 class="success">✅ GitHub Pages fungerar!</h1>
    <p>Om du ser denna sida, så fungerar GitHub Pages.</p>
    <p>Nu kan du använda privacy.html och data-deletion.html</p>
</body>
</html>
HTML

echo "✅ Test-fil skapad: index.html"
echo ""
echo "📋 Nästa steg:"
echo "1. Ladda upp denna fil till ditt GitHub repo"
echo "2. Gå till repo → Settings → Pages"
echo "3. Aktivera Pages (Deploy from a branch → main → / (root))"
echo "4. Vänta 5-10 minuter"
echo "5. Testa: https://atkinking.github.io/facebook-legal-pages/"
echo ""
echo "🔧 Om du vill, kan jag hjälpa dig med git-kommandon:"
echo "   git add ."
echo "   git commit -m 'Add GitHub Pages files'"
echo "   git push origin main"
