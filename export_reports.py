"""
ProofLens AI - Report Export Module
Generate PDF, JSON, and CSV reports for verification results
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
from datetime import datetime
import json
import pandas as pd
from io import BytesIO
from typing import Dict, Any


class ReportExporter:
    """Export verification results to various formats"""
    
    def __init__(self):
        self.app_name = "ProofLens AI"
        self.app_tagline = "Truth Through Technology"
    
    def export_to_pdf(self, verification_data: Dict[str, Any]) -> bytes:
        """
        Generate PDF report for verification results
        
        Args:
            verification_data: Dictionary containing verification results
            
        Returns:
            PDF file as bytes
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#6366f1'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#4f46e5'),
            spaceAfter=12
        )
        
        # Title
        story.append(Paragraph(self.app_name, title_style))
        story.append(Paragraph(self.app_tagline, styles['Normal']))
        story.append(Spacer(1, 0.5 * inch))
        
        # Report Info
        story.append(Paragraph("Verification Report", heading_style))
        report_info = [
            ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Report ID:', str(verification_data.get('id', 'N/A'))],
            ['Verification Type:', verification_data.get('type', 'Text Verification')]
        ]
        
        info_table = Table(report_info, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Authenticity Score
        if 'authenticity_score' in verification_data:
            story.append(Paragraph("Authenticity Score", heading_style))
            score = verification_data['authenticity_score']
            score_color = self._get_score_color(score)
            
            score_text = f'<font size="24" color="{score_color}"><b>{score}/100</b></font>'
            story.append(Paragraph(score_text, styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))
        
        # Key Findings
        if 'key_findings' in verification_data and verification_data['key_findings']:
            story.append(Paragraph("Key Findings", heading_style))
            for finding in verification_data['key_findings']:
                story.append(Paragraph(f"• {finding}", styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))
        
        # Differences
        if 'differences' in verification_data and verification_data['differences']:
            story.append(Paragraph("Identified Differences", heading_style))
            for diff in verification_data['differences']:
                story.append(Paragraph(f"• {diff}", styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))
        
        # Score Breakdown
        if 'score_breakdown' in verification_data:
            story.append(Paragraph("Score Breakdown", heading_style))
            breakdown = verification_data['score_breakdown']
            breakdown_data = [
                ['Category', 'Score'],
                ['Factual Accuracy', f"{breakdown.get('factual_accuracy', 0)}/40"],
                ['Source Consistency', f"{breakdown.get('source_consistency', 0)}/30"],
                ['Detail Accuracy', f"{breakdown.get('detail_accuracy', 0)}/20"],
                ['Context Accuracy', f"{breakdown.get('context_accuracy', 0)}/10"]
            ]
            
            breakdown_table = Table(breakdown_data, colWidths=[3*inch, 2*inch])
            breakdown_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(breakdown_table)
            story.append(Spacer(1, 0.3 * inch))
        
        # Original Content
        if 'original_text' in verification_data:
            story.append(Paragraph("Original Content", heading_style))
            content = verification_data['original_text'][:500]  # Limit length
            if len(verification_data['original_text']) > 500:
                content += "..."
            story.append(Paragraph(content, styles['Normal']))
            story.append(Spacer(1, 0.3 * inch))
        
        # Footer
        story.append(Spacer(1, 0.5 * inch))
        footer_text = f"<i>This report was generated by {self.app_name}. For more information, visit our website.</i>"
        story.append(Paragraph(footer_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def export_to_json(self, verification_data: Dict[str, Any]) -> str:
        """
        Export verification results to JSON format
        
        Args:
            verification_data: Dictionary containing verification results
            
        Returns:
            JSON string
        """
        # Add metadata
        export_data = {
            'export_info': {
                'app_name': self.app_name,
                'export_date': datetime.now().isoformat(),
                'format': 'json',
                'version': '1.0'
            },
            'verification_data': verification_data
        }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    
    def export_to_csv(self, verification_data: Dict[str, Any]) -> bytes:
        """
        Export verification results to CSV format
        
        Args:
            verification_data: Dictionary containing verification results
            
        Returns:
            CSV file as bytes
        """
        # Flatten the verification data for CSV
        rows = []
        
        # Basic info
        basic_info = {
            'Report ID': verification_data.get('id', 'N/A'),
            'Type': verification_data.get('type', 'Text Verification'),
            'Authenticity Score': verification_data.get('authenticity_score', 0),
            'Verified At': verification_data.get('verified_at', datetime.now().isoformat()),
        }
        rows.append(basic_info)
        
        # Score breakdown
        if 'score_breakdown' in verification_data:
            breakdown = verification_data['score_breakdown']
            rows.append({
                'Category': 'Factual Accuracy',
                'Score': breakdown.get('factual_accuracy', 0)
            })
            rows.append({
                'Category': 'Source Consistency',
                'Score': breakdown.get('source_consistency', 0)
            })
            rows.append({
                'Category': 'Detail Accuracy',
                'Score': breakdown.get('detail_accuracy', 0)
            })
            rows.append({
                'Category': 'Context Accuracy',
                'Score': breakdown.get('context_accuracy', 0)
            })
        
        # Create DataFrame
        df = pd.DataFrame(rows)
        
        # Convert to CSV
        buffer = BytesIO()
        df.to_csv(buffer, index=False, encoding='utf-8')
        buffer.seek(0)
        return buffer.getvalue()
    
    def _get_score_color(self, score: int) -> str:
        """Get color based on authenticity score"""
        if score >= 80:
            return '#10b981'  # Green
        elif score >= 60:
            return '#f59e0b'  # Orange
        elif score >= 40:
            return '#ef4444'  # Red
        else:
            return '#7f1d1d'  # Dark Red


def export_verification_report(verification_data: Dict[str, Any], format: str = 'pdf') -> bytes:
    """
    Convenience function to export verification report
    
    Args:
        verification_data: Dictionary containing verification results
        format: Export format ('pdf', 'json', 'csv')
        
    Returns:
        Exported report as bytes (or str for JSON)
    """
    exporter = ReportExporter()
    
    if format.lower() == 'pdf':
        return exporter.export_to_pdf(verification_data)
    elif format.lower() == 'json':
        json_str = exporter.export_to_json(verification_data)
        return json_str.encode('utf-8')
    elif format.lower() == 'csv':
        return exporter.export_to_csv(verification_data)
    else:
        raise ValueError(f"Unsupported format: {format}")
