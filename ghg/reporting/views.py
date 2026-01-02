from __future__ import annotations

from datetime import datetime
from typing import Optional
import io

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.views.decorators.http import require_GET

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.tableofcontents import TableOfContents

from .services import InventoryFilters, compute_inventory_summary, get_inventory_records


def _parse_date(value: Optional[str]):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


@login_required
@require_GET
def inventory_preview(request: HttpRequest) -> HttpResponse:
    date_from = _parse_date(request.GET.get("from"))
    date_to = _parse_date(request.GET.get("to"))
    scope = request.GET.get("scope") or None
    country = request.GET.get("country") or None
    
    filters = InventoryFilters(
        user=request.user, date_from=date_from, date_to=date_to, scope=scope, country=country
    )
    
    summary = compute_inventory_summary(filters)
    records = get_inventory_records(filters)
    
    ctx = {
        "user": request.user,  # Add user to context
        "report_title": "ISO 14064-1 Emissions Inventory Report",
        "generated_at": now(),
        "standard": "ISO 14064-1",
        "summary": summary,
        "records": records,
        "active_menu": "reporting",  # Set active menu
        "methodology": {
            "formula": "Emissions (kgCO2e) = Activity Data × Emission Factor",
            "unit_notes": [
                "All calculations are stored in kgCO2e and presented in tCO2e where applicable.",
                "tCO2e = kgCO2e / 1000",
                "Emission factors may be sourced from DEFRA/IPCC/Turkey Inventory or company-provided references.",
                "Supplier-provided or user-provided factors should be documented in the reference field.",
            ],
        },
    }
    
    return render(request, "reporting/inventory.html", ctx)


@login_required
@require_GET
def inventory_pdf(request: HttpRequest) -> HttpResponse:
    date_from = _parse_date(request.GET.get("from"))
    date_to = _parse_date(request.GET.get("to"))
    scope = request.GET.get("scope") or None
    country = request.GET.get("country") or None
    
    filters = InventoryFilters(
        user=request.user, date_from=date_from, date_to=date_to, scope=scope, country=country
    )
    
    summary = compute_inventory_summary(filters)
    records = get_inventory_records(filters)
    
    # Create PDF buffer
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch, bottomMargin=1*inch)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Center
        textColor=colors.HexColor('#2c5530')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#2c5530')
    )
    
    # Build PDF content
    story = []
    
    # Title
    story.append(Paragraph("ISO 14064-1 Emissions Inventory Report", title_style))
    story.append(Paragraph(f"Generated on {now().strftime('%B %d, %Y at %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Filters
    if any([date_from, date_to, scope, country]):
        filter_text = "Filters Applied: "
        filters_list = []
        if date_from:
            filters_list.append(f"From: {date_from}")
        if date_to:
            filters_list.append(f"To: {date_to}")
        if scope:
            filters_list.append(f"Scope: {scope}")
        if country:
            filters_list.append(f"Country: {country}")
        filter_text += ", ".join(filters_list)
        story.append(Paragraph(filter_text, styles['Normal']))
        story.append(Spacer(1, 12))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    summary_data = [
        ['Metric', 'Value'],
        ['Total Emissions (tCO₂e)', f"{summary['totals']['total_t']:.3f}"],
        ['Total Emissions (kgCO₂e)', f"{summary['totals']['total_kg']:.0f}"],
        ['Total Records', str(summary['totals']['records'])],
        ['Custom Factor Records', str(summary['flags']['custom_factor_records'])],
        ['Standard', 'ISO 14064-1'],
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5530')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 20))
    
    # Emissions by Scope
    if summary['by_scope']:
        story.append(Paragraph("Emissions by Scope", heading_style))
        scope_data = [['Scope', 'Emissions (tCO₂e)', 'Percentage']]
        for item in summary['by_scope']:
            scope_data.append([
                item['scope'],
                f"{item['value_t']:.3f}",
                f"{item['percentage']:.1f}%"
            ])
        
        scope_table = Table(scope_data, colWidths=[2*inch, 2*inch, 1.5*inch])
        scope_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5530')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(scope_table)
        story.append(Spacer(1, 20))
    
    # Top Sources
    if summary['top_sources']:
        story.append(Paragraph("Top Emission Sources", heading_style))
        sources_data = [['Scope', 'Category', 'Source', 'tCO₂e', '%']]
        for item in summary['top_sources'][:10]:  # Limit to top 10
            sources_data.append([
                item['scope'],
                item['category'][:15] + '...' if len(item['category']) > 15 else item['category'],
                item['source_name'][:20] + '...' if len(item['source_name']) > 20 else item['source_name'],
                f"{item['value_t']:.3f}",
                f"{item['percentage']:.1f}%"
            ])
        
        sources_table = Table(sources_data, colWidths=[1*inch, 1.5*inch, 2*inch, 1*inch, 0.8*inch])
        sources_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5530')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(sources_table)
        story.append(Spacer(1, 20))
    
    # Methodology
    story.append(Paragraph("Methodology & Notes", heading_style))
    methodology_text = """
    <b>Calculation Formula:</b> Emissions (kgCO2e) = Activity Data × Emission Factor<br/><br/>
    <b>Notes:</b><br/>
    • All calculations are stored in kgCO2e and presented in tCO2e where applicable<br/>
    • tCO2e = kgCO2e / 1000<br/>
    • Emission factors may be sourced from DEFRA/IPCC/Turkey Inventory or company-provided references<br/>
    • Supplier-provided or user-provided factors should be documented in the reference field
    """
    story.append(Paragraph(methodology_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    
    # Return response
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.pdf"'
    buffer.close()
    
    return response