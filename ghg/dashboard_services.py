from __future__ import annotations
from decimal import Decimal
from typing import Any, Dict, List, Optional
from datetime import date, datetime, timedelta

from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce

from .models import EmissionRecord, Supplier, MaterialRequest


def _to_decimal(x) -> Decimal:
    """Convert to decimal safely"""
    return Decimal(str(x or 0))


def get_dashboard_metrics(
    user: User,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    country: Optional[str] = None,
) -> Dict[str, Any]:
    """Get comprehensive dashboard metrics for user"""
    
    # Base queryset for user's emission records
    qs = EmissionRecord.objects.filter(user=user)
    
    # Apply filters
    if date_from:
        qs = qs.filter(created_at__date__gte=date_from)
    if date_to:
        qs = qs.filter(created_at__date__lte=date_to)
    if country:
        qs = qs.filter(country=country)
    
    # Calculate totals
    from django.db import models
    totals = qs.aggregate(
        total_t=Coalesce(Sum("emissions_tons", output_field=models.FloatField()), 0.0),
        total_kg=Coalesce(Sum("emissions_kg", output_field=models.FloatField()), 0.0),
        records=Coalesce(Count("id"), 0),
    )
    
    total_t = float(totals["total_t"] or 0)
    
    # Scope breakdown
    by_scope = list(
        qs.values("scope")
        .annotate(value_t=Coalesce(Sum("emissions_tons", output_field=models.FloatField()), 0.0))
        .order_by("scope")
    )
    
    scope_breakdown = []
    for row in by_scope:
        value_t = float(row["value_t"] or 0)
        pct = (value_t / total_t * 100) if total_t > 0 else 0
        scope_breakdown.append(
            {
                "scope": f"Scope {row['scope']}",
                "value_t": value_t,
                "percentage": pct,
            }
        )
    
    # Additional metrics
    suppliers_count = Supplier.objects.filter(user=user).count()
    pending_requests = MaterialRequest.objects.filter(user=user, status="pending").count()
    
    # Latest records for activity
    latest_records = list(
        qs.select_related("supplier")
        .order_by("-created_at")
        .values(
            "created_at",
            "scope",
            "category",
            "source_name",
            "emissions_tons",
            "country",
            "description",
        )[:10]
    )
    
    # Monthly trend (last 6 months)
    six_months_ago = datetime.now() - timedelta(days=180)
    monthly_data = (
        qs.filter(created_at__gte=six_months_ago)
        .extra(select={'month': "strftime('%%Y-%%m', created_at)"})
        .values('month')
        .annotate(total=Sum('emissions_tons', output_field=models.FloatField()))
        .order_by('month')
    )
    
    # Calculate completion percentage (based on having records in all 3 scopes)
    scopes_with_data = set(qs.values_list('scope', flat=True))
    completion_percentage = len(scopes_with_data) * 33.33  # Each scope = ~33%
    
    return {
        "total_emissions_tons": total_t,
        "total_records": int(totals["records"]),
        "suppliers_count": int(suppliers_count),
        "pending_requests": int(pending_requests),
        "scope_breakdown": scope_breakdown,
        "completion_percentage": min(100, completion_percentage),
        "monthly_trends": [
            {
                "month": m["month"],
                "emissions_tons": float(m["total"] or 0),
            }
            for m in monthly_data
        ],
        "latest_records": [
            {
                "created_at": r["created_at"].isoformat(),
                "scope": f"Scope {r['scope']}",
                "category": r["category"],
                "source_name": r["source_name"],
                "emissions_tons": float(r["emissions_tons"] or 0),
                "country": r["country"],
                "description": r["description"] or "",
            }
            for r in latest_records
        ],
    }