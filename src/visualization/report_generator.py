"""
Rapportgenereringsmodul för digital identitetsforskning
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import json
import os
from datetime import datetime
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Klass för generering av rapporter och visualiseringar"""
    
    def __init__(self, output_dir: str = "data/results/reports"):
        """
        Initiera rapportgenerator
        
        Args:
            output_dir (str): Mapp för rapporter
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Konfigurera matplotlib
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        logger.info("ReportGenerator initierad")
    
    def generate_report(self, analysis_results: Dict) -> Dict:
        """
        Generera rapport från analysresultat
        
        Args:
            analysis_results (Dict): Analysresultat
        
        Returns:
            Dict: Genererad rapport
        """
        logger.info("Genererar rapport från analysresultat")
        
        try:
            # Skapa rapportstruktur
            report = {
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'analysis_type': 'digital_identity',
                    'version': '1.0'
                },
                'summary': self._generate_summary(analysis_results),
                'face_analysis': self._generate_face_analysis_report(analysis_results),
                'platform_analysis': self._generate_platform_analysis_report(analysis_results),
                'temporal_analysis': self._generate_temporal_analysis_report(analysis_results),
                'content_analysis': self._generate_content_analysis_report(analysis_results),
                'insights': self._generate_insights(analysis_results),
                'recommendations': self._generate_recommendations(analysis_results)
            }
            
            # Spara rapport
            self._save_report(report)
            
            logger.info("Rapport genererad")
            return report
            
        except Exception as e:
            logger.error(f"Fel vid generering av rapport: {str(e)}")
            return {'error': str(e)}
    
    def generate_summary_report(self, batch_results: Dict) -> Dict:
        """
        Generera sammanfattningsrapport för batch-analys
        
        Args:
            batch_results (Dict): Resultat från batch-analys
        
        Returns:
            Dict: Sammanfattningsrapport
        """
        logger.info("Genererar sammanfattningsrapport")
        
        try:
            # Analysera alla resultat
            all_scores = []
            platform_stats = {}
            consistency_scores = []
            
            for username, results in batch_results.items():
                if 'error' in results:
                    continue
                
                # Samla poäng
                identity_score = results.get('overall_identity_score', 0)
                all_scores.append(identity_score)
                
                # Analysera plattformar
                platform_rep = results.get('platform_representation', {})
                for platform in platform_rep.keys():
                    if platform not in platform_stats:
                        platform_stats[platform] = 0
                    platform_stats[platform] += 1
                
                # Samla konsistenspoäng
                face_consistency = results.get('face_consistency', {})
                consistency = face_consistency.get('overall_consistency', 0)
                consistency_scores.append(consistency)
            
            # Generera sammanfattning
            summary_report = {
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'analysis_type': 'batch_summary',
                    'total_users': len(batch_results),
                    'successful_analyses': len([r for r in batch_results.values() if 'error' not in r])
                },
                'statistics': {
                    'average_identity_score': np.mean(all_scores) if all_scores else 0,
                    'median_identity_score': np.median(all_scores) if all_scores else 0,
                    'std_identity_score': np.std(all_scores) if all_scores else 0,
                    'average_consistency': np.mean(consistency_scores) if consistency_scores else 0
                },
                'platform_distribution': platform_stats,
                'score_distribution': self._analyze_score_distribution(all_scores),
                'insights': self._generate_batch_insights(batch_results),
                'recommendations': self._generate_batch_recommendations(batch_results)
            }
            
            # Spara sammanfattningsrapport
            self._save_summary_report(summary_report)
            
            logger.info("Sammanfattningsrapport genererad")
            return summary_report
            
        except Exception as e:
            logger.error(f"Fel vid generering av sammanfattningsrapport: {str(e)}")
            return {'error': str(e)}
    
    def _generate_summary(self, analysis_results: Dict) -> Dict:
        """Generera sammanfattning av analysresultat"""
        return {
            'overall_identity_score': analysis_results.get('overall_identity_score', 0),
            'analysis_quality': self._assess_analysis_quality(analysis_results),
            'key_findings': self._extract_key_findings(analysis_results)
        }
    
    def _generate_face_analysis_report(self, analysis_results: Dict) -> Dict:
        """Generera ansiktsanalysrapport"""
        face_consistency = analysis_results.get('face_consistency', {})
        
        return {
            'overall_consistency': face_consistency.get('overall_consistency', 0),
            'platform_consistency': face_consistency.get('platform_consistency', {}),
            'cross_platform_comparison': face_consistency.get('cross_platform_comparison', {}),
            'quality_assessment': self._assess_face_quality(face_consistency)
        }
    
    def _generate_platform_analysis_report(self, analysis_results: Dict) -> Dict:
        """Generera plattformsanalysrapport"""
        platform_rep = analysis_results.get('platform_representation', {})
        
        return {
            'platforms_analyzed': list(platform_rep.keys()),
            'platform_activity': {p: data.get('activity_level', 0) for p, data in platform_rep.items()},
            'profile_completeness': {p: data.get('profile_completeness', 0) for p, data in platform_rep.items()},
            'image_quality': {p: data.get('image_quality', {}) for p, data in platform_rep.items()}
        }
    
    def _generate_temporal_analysis_report(self, analysis_results: Dict) -> Dict:
        """Generera tidsanalysrapport"""
        temporal_patterns = analysis_results.get('temporal_patterns', {})
        
        return {
            'platforms_analyzed': list(temporal_patterns.keys()),
            'posting_frequency': {p: data.get('posting_frequency', 0) for p, data in temporal_patterns.items()},
            'peak_activity': {p: data.get('peak_activity_hours', []) for p, data in temporal_patterns.items()},
            'seasonal_patterns': {p: data.get('seasonal_patterns', {}) for p, data in temporal_patterns.items()}
        }
    
    def _generate_content_analysis_report(self, analysis_results: Dict) -> Dict:
        """Generera innehållsanalysrapport"""
        content_patterns = analysis_results.get('content_patterns', {})
        
        return {
            'platforms_analyzed': list(content_patterns.keys()),
            'image_types': {p: data.get('image_types', {}) for p, data in content_patterns.items()},
            'content_themes': {p: data.get('content_themes', []) for p, data in content_patterns.items()},
            'visual_style': {p: data.get('visual_style', {}) for p, data in content_patterns.items()},
            'diversity_scores': {p: data.get('diversity_score', 0) for p, data in content_patterns.items()}
        }
    
    def _generate_insights(self, analysis_results: Dict) -> List[str]:
        """Generera insikter från analysresultat"""
        insights = []
        
        # Ansiktskonsistens
        face_consistency = analysis_results.get('face_consistency', {})
        overall_consistency = face_consistency.get('overall_consistency', 0)
        
        if overall_consistency > 0.8:
            insights.append("Hög konsistens i ansiktsrepresentation över plattformar")
        elif overall_consistency < 0.4:
            insights.append("Låg konsistens i ansiktsrepresentation - möjlig identitetsvariation")
        
        # Plattformsrepresentation
        platform_rep = analysis_results.get('platform_representation', {})
        if len(platform_rep) > 1:
            insights.append(f"Aktiv på {len(platform_rep)} olika plattformar")
        
        # Identitetspoäng
        identity_score = analysis_results.get('overall_identity_score', 0)
        if identity_score > 0.8:
            insights.append("Stark och konsekvent digital identitet")
        elif identity_score < 0.4:
            insights.append("Varierande digital identitet över plattformar")
        
        return insights
    
    def _generate_recommendations(self, analysis_results: Dict) -> List[str]:
        """Generera rekommendationer baserat på analysresultat"""
        recommendations = []
        
        # Ansiktskonsistens
        face_consistency = analysis_results.get('face_consistency', {})
        overall_consistency = face_consistency.get('overall_consistency', 0)
        
        if overall_consistency < 0.5:
            recommendations.append("Överväg att använda liknande bilder över plattformar för bättre konsistens")
        
        # Plattformsrepresentation
        platform_rep = analysis_results.get('platform_representation', {})
        for platform, data in platform_rep.items():
            activity_level = data.get('activity_level', 0)
            if activity_level < 0.3:
                recommendations.append(f"Överväg att öka aktivitet på {platform}")
        
        # Identitetspoäng
        identity_score = analysis_results.get('overall_identity_score', 0)
        if identity_score < 0.6:
            recommendations.append("Fokusera på att skapa en mer konsekvent digital identitet")
        
        return recommendations
    
    def _assess_analysis_quality(self, analysis_results: Dict) -> str:
        """Bedöm analyskvalitet"""
        # Enkel heuristik för kvalitetsbedömning
        if 'error' in analysis_results:
            return 'low'
        
        required_keys = ['face_consistency', 'platform_representation', 'temporal_patterns', 'content_patterns']
        present_keys = sum(1 for key in required_keys if key in analysis_results)
        
        if present_keys >= 3:
            return 'high'
        elif present_keys >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _extract_key_findings(self, analysis_results: Dict) -> List[str]:
        """Extrahera nyckelfynd från analysresultat"""
        findings = []
        
        # Ansiktskonsistens
        face_consistency = analysis_results.get('face_consistency', {})
        if face_consistency.get('overall_consistency', 0) > 0.7:
            findings.append("Hög ansiktskonsistens över plattformar")
        
        # Plattformsrepresentation
        platform_rep = analysis_results.get('platform_representation', {})
        if len(platform_rep) > 2:
            findings.append("Aktiv på flera plattformar")
        
        return findings
    
    def _assess_face_quality(self, face_consistency: Dict) -> str:
        """Bedöm ansiktskvalitet"""
        overall_consistency = face_consistency.get('overall_consistency', 0)
        
        if overall_consistency > 0.8:
            return 'high'
        elif overall_consistency > 0.5:
            return 'medium'
        else:
            return 'low'
    
    def _analyze_score_distribution(self, scores: List[float]) -> Dict:
        """Analysera poängfördelning"""
        if not scores:
            return {'error': 'Inga poäng att analysera'}
        
        return {
            'min': min(scores),
            'max': max(scores),
            'mean': np.mean(scores),
            'median': np.median(scores),
            'std': np.std(scores),
            'quartiles': np.percentile(scores, [25, 50, 75]).tolist()
        }
    
    def _generate_batch_insights(self, batch_results: Dict) -> List[str]:
        """Generera insikter för batch-analys"""
        insights = []
        
        # Analysera alla resultat
        all_scores = [r.get('overall_identity_score', 0) for r in batch_results.values() if 'error' not in r]
        
        if all_scores:
            avg_score = np.mean(all_scores)
            if avg_score > 0.7:
                insights.append("Hög genomsnittlig identitetspoäng i gruppen")
            elif avg_score < 0.4:
                insights.append("Låg genomsnittlig identitetspoäng i gruppen")
        
        return insights
    
    def _generate_batch_recommendations(self, batch_results: Dict) -> List[str]:
        """Generera rekommendationer för batch-analys"""
        recommendations = []
        
        # Analysera alla resultat
        all_scores = [r.get('overall_identity_score', 0) for r in batch_results.values() if 'error' not in r]
        
        if all_scores:
            avg_score = np.mean(all_scores)
            if avg_score < 0.6:
                recommendations.append("Gruppen skulle dra nytta av identitetskonsistensutbildning")
        
        return recommendations
    
    def _save_report(self, report: Dict):
        """Spara rapport"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"identity_analysis_report_{timestamp}.json"
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Rapport sparad: {filepath}")
            
        except Exception as e:
            logger.error(f"Fel vid sparande av rapport: {str(e)}")
    
    def _save_summary_report(self, report: Dict):
        """Spara sammanfattningsrapport"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"batch_summary_report_{timestamp}.json"
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Sammanfattningsrapport sparad: {filepath}")
            
        except Exception as e:
            logger.error(f"Fel vid sparande av sammanfattningsrapport: {str(e)}")
    
    def export_to_html(self, output_path: str = "data/results/reports/identity_analysis.html") -> bool:
        """
        Exportera rapport som HTML
        
        Args:
            output_path (str): Sökväg för HTML-export
        
        Returns:
            bool: True om export lyckades
        """
        try:
            # Skapa mapp om den inte finns
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Generera HTML-innehåll
            html_content = self._generate_html_report()
            
            # Spara HTML
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Rapport exporterad som HTML: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Fel vid HTML-export: {str(e)}")
            return False
    
    def _generate_html_report(self) -> str:
        """Generera HTML-rapport"""
        return """
        <!DOCTYPE html>
        <html lang="sv">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Digital Identitetsanalys - Rapport</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
                .section { margin: 20px 0; }
                .metric { background-color: #e8f4f8; padding: 10px; margin: 10px 0; border-radius: 3px; }
                .insight { background-color: #fff3cd; padding: 10px; margin: 10px 0; border-radius: 3px; }
                .recommendation { background-color: #d1ecf1; padding: 10px; margin: 10px 0; border-radius: 3px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Digital Identitetsanalys</h1>
                <p>Rapport genererad: {timestamp}</p>
            </div>
            
            <div class="section">
                <h2>Sammanfattning</h2>
                <p>Denna rapport analyserar digital identitet och ansiktsrepresentation över sociala medieplattformar.</p>
            </div>
            
            <div class="section">
                <h2>Insikter</h2>
                <div class="insight">
                    <p>Analysen visar mönster i hur individer representerar sig online.</p>
                </div>
            </div>
            
            <div class="section">
                <h2>Rekommendationer</h2>
                <div class="recommendation">
                    <p>Fokusera på konsistens i digital identitet över plattformar.</p>
                </div>
            </div>
        </body>
        </html>
        """.format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
