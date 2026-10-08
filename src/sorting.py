"""Parcel prioritization helpers for the Mini Courier Planner."""

PRIORITY_SCORE = {
    "High": 3,
    "Medium": 2,
    "Low": 1,
}


def priority_score(parcel):
    """Return the numeric score for a parcel priority label."""
    return PRIORITY_SCORE[parcel.priority]


def parcel_benefit(parcel):
    """Calculate the benefit score used by package selection."""
    urgency_bonus = max(0, 6 - parcel.deadline) * 5
    priority_bonus = priority_score(parcel) * 20
    return parcel.value + priority_bonus + urgency_bonus


def sort_parcels_by_priority_and_deadline(parcels):
    """Sort parcels by higher priority first, then earlier deadline."""
    return sorted(
        parcels,
        key=lambda parcel: (-priority_score(parcel), parcel.deadline),
    )

