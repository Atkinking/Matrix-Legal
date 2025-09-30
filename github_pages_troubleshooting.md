# 🔧 GitHub Pages Felsökning

## Vanliga problem och lösningar:

### 1. **Pages inte aktiverat**
- Gå till ditt repo på GitHub
- Klicka "Settings" (höger sida)
- Scrolla ner till "Pages" (vänster meny)
- Under "Source" välj "Deploy from a branch"
- Välj "main" branch och "/ (root)" folder
- Klicka "Save"

### 2. **Felaktigt filnamn**
Kontrollera att filerna heter exakt:
- `privacy.html` (inte privacy.htm eller Privacy.html)
- `data-deletion.html` (inte data_deletion.html)

### 3. **Filerna ligger i root-mappen**
Strukturen ska vara:
```
ditt-repo/
├── privacy.html
├── data-deletion.html
└── README.md
```

### 4. **GitHub Pages tar tid**
- Det kan ta 5-10 minuter att aktiveras
- Vänta och försök igen

### 5. **Kontrollera URL-format**
Rätt format:
```
https://dittnamn.github.io/repo-namn/privacy.html
https://dittnamn.github.io/repo-namn/data-deletion.html
```

### 6. **Testa lokalt först**
```bash
# Öppna filerna i webbläsaren lokalt
open privacy.html
open data-deletion.html
```

## 🚀 Snabb fix:

### Steg 1: Kontrollera repo-struktur
```
ditt-repo/
├── privacy.html ✅
├── data-deletion.html ✅
└── README.md ✅
```

### Steg 2: Aktivera Pages
1. Gå till repo → Settings
2. Vänster meny → Pages
3. Source: "Deploy from a branch"
4. Branch: "main"
5. Folder: "/ (root)"
6. Save

### Steg 3: Vänta 5-10 minuter
GitHub behöver tid att bygga sidorna.

### Steg 4: Testa URL:erna
```
https://dittnamn.github.io/repo-namn/privacy.html
https://dittnamn.github.io/repo-namn/data-deletion.html
```

## 🔍 Debug-steg:

### Kontrollera att Pages är aktiverat:
1. Gå till repo → Settings → Pages
2. Du ska se: "Your site is published at https://dittnamn.github.io/repo-namn/"

### Kontrollera filer:
1. Gå till repo → Code
2. Du ska se privacy.html och data-deletion.html i root

### Kontrollera commits:
1. Gå till repo → Actions
2. Kolla att Pages build lyckades

## 📞 Om det fortfarande inte fungerar:

1. **Dubbelkolla repo-namnet** - det måste matcha URL:en
2. **Kontrollera att filerna är committed** - de måste vara i main branch
3. **Vänta längre** - GitHub kan vara långsam
4. **Prova att byta namn** - vissa namn kan vara reserverade

## 🎯 Snabb test:
Skapa en enkel index.html först:
```html
<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body><h1>GitHub Pages fungerar!</h1></body>
</html>
```

Om index.html fungerar, så fungerar Pages!
