"""0/1 knapsack parcel selection for the Mini Courier Planner."""

from src.sorting import parcel_benefit


def knapsack_select_parcels(parcels, capacity):
    """Select the parcel subset with maximum benefit within capacity."""
    n = len(parcels)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        parcel = parcels[i - 1]
        weight = parcel.weight
        benefit = parcel_benefit(parcel)

        for current_capacity in range(capacity + 1):
            without_parcel = dp[i - 1][current_capacity]
            with_parcel = 0

            if weight <= current_capacity:
                with_parcel = benefit + dp[i - 1][current_capacity - weight]

            dp[i][current_capacity] = max(without_parcel, with_parcel)

    selected = []
    remaining_capacity = capacity

    for i in range(n, 0, -1):
        if dp[i][remaining_capacity] != dp[i - 1][remaining_capacity]:
            parcel = parcels[i - 1]
            selected.append(parcel)
            remaining_capacity -= parcel.weight

    selected.reverse()
    return dp[n][capacity], selected, dp

