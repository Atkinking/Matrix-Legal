#!/bin/bash

echo "🔧 Fixar befintliga GitHub Pages filer"
echo "======================================"

# Kontrollera om vi är i rätt repo
if [ ! -d ".git" ]; then
    echo "❌ Inte i ett git-repo. Initialisera först:"
    echo "   git init"
    echo "   git remote add origin git@github.com:Atkinking/facebook-legal-pages.git"
    exit 1
fi

echo "📋 Kontrollerar git-status..."
git status

echo ""
echo "🔧 Lägger till alla filer..."
git add .

echo "📝 Committar ändringar..."
git commit -m "Fix GitHub Pages - Add privacy and data-deletion pages"

echo "🚀 Pushar till GitHub..."
git push origin main

echo ""
echo "✅ Filer uppladdade till GitHub!"
echo ""
echo "📋 Nästa steg:"
echo "1. Gå till https://github.com/Atkinking/facebook-legal-pages"
echo "2. Klicka Settings → Pages"
echo "3. Välj 'Deploy from a branch' → 'main' → '/ (root)'"
echo "4. Spara och vänta 5-10 minuter"
echo ""
echo "🔗 Testa sedan:"
echo "https://atkinking.github.io/facebook-legal-pages/privacy.html"
echo "https://atkinking.github.io/facebook-legal-pages/data-deletion.html"
