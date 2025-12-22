from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any, Dict, List, Optional

from django.contrib.auth.models import User
from django.db.models import Count, Sum, FloatField
from django.db.models.functions import Coalesce
from django.db.models import Q, Value

from ghg.models import EmissionRecord, MaterialRequest


@dataclass(frozen=True)
class InventoryFilters:
    user: User
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    scope: Optional[str] = None
    country: Optional[str] = None


def _to_tonnes(kg: float) -> float:
    return kg / 1000.0


def get_inventory_queryset(filters: InventoryFilters):
    qs = EmissionRecord.objects.filter(user=filters.user)
    
    if filters.date_from:
        qs = qs.filter(created_at__date__gte=filters.date_from)
    if filters.date_to:
        qs = qs.filter(created_at__date__lte=filters.date_to)
    
    if filters.scope:
        qs = qs.filter(scope=filters.scope)
    
    if filters.country:
        qs = qs.filter(country=filters.country)
    
    return qs


def compute_inventory_summary(filters: InventoryFilters) -> Dict[str, Any]:
    qs = get_inventory_queryset(filters)
    
    totals = qs.aggregate(
        total_kg=Coalesce(Sum("emissions_kg"), Value(0.0, output_field=FloatField())),
        records=Coalesce(Count("id"), Value(0)),
    )
    total_t = _to_tonnes(totals["total_kg"])
    
    by_scope = list(
        qs.values("scope")
        .annotate(value_kg=Coalesce(Sum("emissions_kg"), Value(0.0, output_field=FloatField())))
        .order_by("scope")
    )
    by_scope_out = []
    for row in by_scope:
        value_t = _to_tonnes(row["value_kg"])
        pct = (value_t / total_t * 100) if total_t > 0 else 0.0
        by_scope_out.append(
            {"scope": f"Scope {row['scope']}", "value_t": value_t, "percentage": pct}
        )
    
    by_category = list(
        qs.values("scope", "category")
        .annotate(value_kg=Coalesce(Sum("emissions_kg"), Value(0.0, output_field=FloatField())))
        .order_by("scope", "category")
    )
    by_category_out = []
    for row in by_category:
        value_t = _to_tonnes(row["value_kg"])
        pct = (value_t / total_t * 100) if total_t > 0 else 0.0
        by_category_out.append(
            {
                "scope": f"Scope {row['scope']}",
                "category": row["category"],
                "value_t": value_t,
                "percentage": pct,
            }
        )
    
    top_sources = list(
        qs.values("scope", "category", "source_name")
        .annotate(value_kg=Coalesce(Sum("emissions_kg"), Value(0.0, output_field=FloatField())))
        .order_by("-value_kg")[:10]
    )
    top_sources_out = []
    for row in top_sources:
        value_t = _to_tonnes(row["value_kg"])
        pct = (value_t / total_t * 100) if total_t > 0 else 0.0
        top_sources_out.append(
            {
                "scope": f"Scope {row['scope']}",
                "category": row["category"],
                "source_name": row["source_name"],
                "value_t": value_t,
                "percentage": pct,
            }
        )
    
    custom_factor_records = qs.filter(
        Q(reference__icontains="custom")
        | Q(reference__icontains="supplier")
        | Q(reference__icontains="certificate")
        | Q(supplier__isnull=False)
    ).count()
    
    pending_other_items = MaterialRequest.objects.filter(user=filters.user, status="pending").count()
    
    return {
        "filters": {
            "date_from": filters.date_from.isoformat() if filters.date_from else None,
            "date_to": filters.date_to.isoformat() if filters.date_to else None,
            "scope": filters.scope,
            "country": filters.country,
        },
        "totals": {
            "total_kg": totals["total_kg"],
            "total_t": total_t,
            "records": totals["records"],
        },
        "by_scope": by_scope_out,
        "by_category": by_category_out,
        "top_sources": top_sources_out,
        "flags": {
            "custom_factor_records": custom_factor_records,
            "pending_other_items": pending_other_items,
        },
    }


def get_inventory_records(filters: InventoryFilters) -> List[Dict[str, Any]]:
    qs = (
        get_inventory_queryset(filters)
        .select_related("supplier")
        .order_by("created_at", "scope", "category", "source_name")
    )
    
    rows: List[Dict[str, Any]] = []
    for r in qs.iterator():
        supplier_name = ""
        if r.supplier_id and r.supplier:
            supplier_name = r.supplier.name
        elif r.supplier_old:
            supplier_name = r.supplier_old
        
        rows.append(
            {
                "created_date": r.created_at.date().isoformat(),
                "scope": f"Scope {r.scope}",
                "category": r.category,
                "source": r.source,
                "source_name": r.source_name,
                "supplier": supplier_name,
                "activity_data": r.activity_data,
                "unit": r.unit,
                "emission_factor": r.emission_factor,
                "country": r.country,
                "reference": (r.reference or ""),
                "emissions_kg": r.emissions_kg,
                "emissions_t": _to_tonnes(r.emissions_kg),
            }
        )
    
    return rows