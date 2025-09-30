#!/usr/bin/env python3
"""
Enkel demo av Digital Identitetsforskning
Fungerar direkt utan API:er eller användarnamn
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
import os
import sqlite3

class SimpleDigitalIdentityDemo:
    """Enkel demo av forskningsprojektet"""
    
    def __init__(self):
        """Initiera demo"""
        self.data = {}
        self.search_history = []
        self.db_path = "data/demo.db"
        
        # Skapa mappar
        os.makedirs("data", exist_ok=True)
        os.makedirs("data/export", exist_ok=True)
        
        # Initiera databas
        self._init_database()
        
        print("Digital Identity Research Demo initierad!")
    
    def _init_database(self):
        """Initiera databas"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS demo_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    data_json TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Databasfel: {e}")
    
    def demo_identity_analysis(self):
        """Demo av identitetsanalys"""
        print("\n=== DEMO: Identitetsanalys ===")
        
        # Simulera användardata
        users = ["Alice", "Bob", "Charlie"]
        platforms = ["Twitter", "Instagram", "Facebook"]
        
        results = {}
        
        for user in users:
            print(f"\nAnalyserar {user}...")
            
            # Simulera analys
            identity_score = np.random.uniform(0.4, 0.9)
            consistency = np.random.uniform(0.3, 0.8)
            
            user_data = {
                'username': user,
                'platforms': platforms,
                'identity_score': identity_score,
                'consistency': consistency,
                'face_analysis': {
                    'total_faces': np.random.randint(1, 5),
                    'average_quality': np.random.uniform(0.6, 0.9),
                    'consistency_score': consistency
                },
                'platform_activity': {
                    platform: {
                        'posts': np.random.randint(10, 100),
                        'followers': np.random.randint(100, 5000),
                        'engagement': np.random.uniform(0.1, 0.5)
                    } for platform in platforms
                },
                'insights': [
                    f"{user} har {'hög' if identity_score > 0.7 else 'låg'} identitetspoäng",
                    f"Ansiktskonsistens: {'bra' if consistency > 0.6 else 'varierande'}",
                    f"Aktiv på {len(platforms)} plattformar"
                ],
                'timestamp': datetime.now().isoformat()
            }
            
            results[user] = user_data
            
            print(f"  - Identitetspoäng: {identity_score:.2f}")
            print(f"  - Konsistens: {consistency:.2f}")
            print(f"  - Ansikten: {user_data['face_analysis']['total_faces']}")
        
        # Spara resultat
        self.data.update(results)
        self._save_to_database("identity_analysis", results)
        
        print(f"\n✅ Analys slutförd för {len(users)} användare")
        return results
    
    def demo_reverse_image_search(self):
        """Demo av reverse image search"""
        print("\n=== DEMO: Reverse Image Search ===")
        
        # Simulera sökning
        test_images = [
            "test_image_1.jpg",
            "profile_photo.png", 
            "selfie.jpg"
        ]
        
        search_results = {}
        
        for image in test_images:
            print(f"\nSöker efter {image}...")
            
            # Simulera matchningar
            matches = []
            platforms = ["Twitter", "Instagram", "Facebook"]
            
            for platform in platforms:
                if np.random.random() > 0.3:  # 70% chans för matchning
                    similarity = np.random.uniform(0.6, 0.95)
                    match = {
                        'platform': platform,
                        'similarity': similarity,
                        'confidence': similarity * 0.9,
                        'user': f"user_{np.random.randint(1, 10)}",
                        'image_url': f"https://example.com/{platform}_match.jpg"
                    }
                    matches.append(match)
            
            # Sortera efter similaritet
            matches.sort(key=lambda x: x['similarity'], reverse=True)
            
            result = {
                'image_path': image,
                'total_matches': len(matches),
                'best_match': matches[0] if matches else None,
                'all_matches': matches,
                'analysis': {
                    'average_similarity': np.mean([m['similarity'] for m in matches]) if matches else 0,
                    'insights': [
                        f"Hittade {len(matches)} matchningar" if matches else "Inga matchningar",
                        f"Bästa similaritet: {matches[0]['similarity']:.2f}" if matches else "Inga matchningar"
                    ]
                },
                'timestamp': datetime.now().isoformat()
            }
            
            search_results[image] = result
            self.search_history.append(result)
            
            print(f"  - Matchningar: {len(matches)}")
            if matches:
                print(f"  - Bästa similaritet: {matches[0]['similarity']:.2f}")
                print(f"  - Plattform: {matches[0]['platform']}")
        
        print(f"\n✅ Reverse image search slutförd för {len(test_images)} bilder")
        return search_results
    
    def demo_statistics(self):
        """Demo av statistik"""
        print("\n=== DEMO: Statistik ===")
        
        # Beräkna statistik
        if self.data:
            identity_scores = [user['identity_score'] for user in self.data.values()]
            consistencies = [user['consistency'] for user in self.data.values()]
            
            stats = {
                'total_users': len(self.data),
                'average_identity_score': np.mean(identity_scores),
                'average_consistency': np.mean(consistencies),
                'total_searches': len(self.search_history),
                'high_identity_users': sum(1 for score in identity_scores if score > 0.7),
                'consistent_users': sum(1 for cons in consistencies if cons > 0.6)
            }
            
            print(f"Totalt antal användare: {stats['total_users']}")
            print(f"Genomsnittlig identitetspoäng: {stats['average_identity_score']:.2f}")
            print(f"Genomsnittlig konsistens: {stats['average_consistency']:.2f}")
            print(f"Totalt antal sökningar: {stats['total_searches']}")
            print(f"Användare med hög identitetspoäng: {stats['high_identity_users']}")
            print(f"Konsekventa användare: {stats['consistent_users']}")
            
            return stats
        else:
            print("Ingen data att analysera än")
            return {}
    
    def demo_visualization(self):
        """Demo av visualisering"""
        print("\n=== DEMO: Visualisering ===")
        
        if not self.data:
            print("Ingen data att visualisera")
            return
        
        # Förbered data
        users = list(self.data.keys())
        identity_scores = [self.data[user]['identity_score'] for user in users]
        consistencies = [self.data[user]['consistency'] for user in users]
        
        # Skapa visualisering
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # Identitetspoäng
        ax1.bar(users, identity_scores, color='skyblue')
        ax1.set_title('Identitetspoäng per användare')
        ax1.set_ylabel('Poäng')
        ax1.set_ylim(0, 1)
        
        # Konsistens
        ax2.bar(users, consistencies, color='lightcoral')
        ax2.set_title('Ansiktskonsistens per användare')
        ax2.set_ylabel('Konsistens')
        ax2.set_ylim(0, 1)
        
        # Scatter plot
        ax3.scatter(identity_scores, consistencies, s=100, alpha=0.7)
        ax3.set_xlabel('Identitetspoäng')
        ax3.set_ylabel('Konsistens')
        ax3.set_title('Identitetspoäng vs Konsistens')
        
        # Histogram
        ax4.hist(identity_scores, bins=5, alpha=0.7, color='lightgreen')
        ax4.set_title('Fördelning av identitetspoäng')
        ax4.set_xlabel('Identitetspoäng')
        ax4.set_ylabel('Antal användare')
        
        plt.tight_layout()
        
        # Spara visualisering
        output_path = "data/export/demo_visualization.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Visualisering sparad som: {output_path}")
    
    def demo_export(self):
        """Demo av export"""
        print("\n=== DEMO: Export ===")
        
        if not self.data:
            print("Ingen data att exportera")
            return
        
        # JSON export
        json_path = "data/export/demo_results.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        print(f"JSON export: {json_path}")
        
        # CSV export
        csv_data = []
        for user, data in self.data.items():
            csv_data.append({
                'user': user,
                'identity_score': data['identity_score'],
                'consistency': data['consistency'],
                'platforms': ', '.join(data['platforms']),
                'faces': data['face_analysis']['total_faces']
            })
        
        df = pd.DataFrame(csv_data)
        csv_path = "data/export/demo_results.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"CSV export: {csv_path}")
        
        # HTML export
        html_path = "data/export/demo_results.html"
        html_content = f"""
        <!DOCTYPE html>
        <html lang="sv">
        <head>
            <meta charset="UTF-8">
            <title>Digital Identitetsanalys - Demo</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .user {{ background-color: #e8f4f8; padding: 15px; margin: 10px 0; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Digital Identitetsanalys - Demo</h1>
                <p>Genererad: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
        """
        
        for user, data in self.data.items():
            html_content += f"""
            <div class="user">
                <h3>{user}</h3>
                <p>Identitetspoäng: {data['identity_score']:.2f}</p>
                <p>Konsistens: {data['consistency']:.2f}</p>
                <p>Plattformar: {', '.join(data['platforms'])}</p>
                <p>Ansikten: {data['face_analysis']['total_faces']}</p>
            </div>
            """
        
        html_content += "</body></html>"
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML export: {html_path}")
    
    def _save_to_database(self, analysis_type, data):
        """Spara data i databas"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            data_json = json.dumps(data, ensure_ascii=False)
            cursor.execute('''
                INSERT INTO demo_data (name, data_json)
                VALUES (?, ?)
            ''', (analysis_type, data_json))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Databasfel: {e}")
    
    def run_full_demo(self):
        """Kör fullständig demo"""
        print("🚀 Startar fullständig demo av Digital Identitetsforskning")
        print("=" * 60)
        
        # 1. Identitetsanalys
        self.demo_identity_analysis()
        
        # 2. Reverse Image Search
        self.demo_reverse_image_search()
        
        # 3. Statistik
        self.demo_statistics()
        
        # 4. Visualisering
        self.demo_visualization()
        
        # 5. Export
        self.demo_export()
        
        print("\n" + "=" * 60)
        print("✅ Demo slutförd!")
        print("Kontrollera 'data/export/' mappen för resultat")

def main():
    """Huvudfunktion"""
    print("=== Digital Identitetsforskning - DEMO ===")
    print("Enkel demo utan API:er eller användarnamn")
    print()
    
    demo = SimpleDigitalIdentityDemo()
    
    print("Välj demo:")
    print("1. Kör fullständig demo")
    print("2. Bara identitetsanalys")
    print("3. Bara reverse image search")
    print("4. Bara statistik")
    print("5. Bara visualisering")
    print("6. Bara export")
    print("7. Avsluta")
    print()
    
    choice = input("Välj alternativ (1-7): ")
    
    if choice == "1":
        demo.run_full_demo()
    elif choice == "2":
        demo.demo_identity_analysis()
    elif choice == "3":
        demo.demo_reverse_image_search()
    elif choice == "4":
        demo.demo_statistics()
    elif choice == "5":
        demo.demo_visualization()
    elif choice == "6":
        demo.demo_export()
    elif choice == "7":
        print("Tack för att du testade demon!")
    else:
        print("Ogiltigt val")

if __name__ == "__main__":
    main()
