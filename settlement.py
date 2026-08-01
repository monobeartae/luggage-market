"""
Business logic for calculating revenue and settlements.
"""

from collections import defaultdict


def calculate_items_sold(sale_items):
    """
    Returns:
    {
        member_id: total_quantity_sold
    }
    """

    totals = defaultdict(int)

    for item in sale_items:

        totals[item["member_id"]] += item["quantity"]

    return dict(totals)


def calculate_money_received(sales):
    """
    Returns:
    {
        payment_source_id: total_money_received
    }
    """

    totals = defaultdict(float)

    for sale in sales:
        totals[sale["payment_source_id"]] += sale["sale_price"]

    return dict(totals)


def calculate_revenue(sales, sale_items):
    """
    Calculates how much money each member earned.

    Revenue is split according to quantity.

    Example:

    Sale
        $9

    Charlie 1
    Bob     2

    Charlie earns $3
    Bob earns $6
    """

    revenue = defaultdict(float)

    # Group sale items by sale
    grouped = defaultdict(list)

    for item in sale_items:

        grouped[item["sale_id"]].append(item)

    for sale in sales:

        items = grouped[sale["id"]]

        total_quantity = sum(
            item["quantity"]
            for item in items
        )

        if total_quantity == 0:
            continue

        value_per_item = sale["sale_price"] / total_quantity

        for item in items:

            revenue[item["member_id"]] += (
                value_per_item *
                item["quantity"]
            )

    return dict(revenue)


def calculate_transfers(
    revenue,
    received,
):
    """
    Returns

    [
        {
            "from": payment_source_id,
            "to": member_id,
            "amount": 10.50
        }
    ]
    """

    total_received = round(sum(received.values()), 2)
    total_revenue = round(sum(revenue.values()), 2)

    if abs(total_received - total_revenue) > 0.01:
        raise ValueError(
            "Revenue does not match money received."
        )

    transfers = []

    remaining = revenue.copy()

    for payment_source_id, available in received.items():

        available = round(available, 2)

        for member_id in list(remaining.keys()):

            if available < 0.01:
                break

            amount = min(
                available,
                remaining[member_id]
            )

            if amount <= 0:
                continue

            transfers.append({
                "from": payment_source_id,
                "to": member_id,
                "amount": round(amount, 2)
            })

            available -= amount
            remaining[member_id] -= amount

    return transfers


def build_summary(
    members,
    payment_sources,
    sales,
    sale_items,
):
    """
    Builds a summary using MEMBER NAMES instead of IDs.
    """

    id_to_name = {
        member["id"]: member["name"]
        for member in members
    }

    payment_source_to_name = {
        ps["id"]: ps["name"]
        for ps in payment_sources
    }

    revenue = calculate_revenue(
        sales,
        sale_items,
    )

    received = calculate_money_received(
        sales,
    )

    items = calculate_items_sold(
        sale_items,
    )

    transfers = calculate_transfers(
        revenue,
        received,
    )

    revenue = {
        id_to_name[member_id]: amount
        for member_id, amount in revenue.items()
    }

    received = {
        payment_source_to_name[source_id]: amount
        for source_id, amount in received.items()
    }

    items = {
        id_to_name[member_id]: quantity
        for member_id, quantity in items.items()
    }

    transfers = [
        {
            "from": payment_source_to_name[t["from"]],
            "to": id_to_name[t["to"]],
            "amount": t["amount"],
        }
        for t in transfers
    ]
    
    return (items, revenue, received, transfers)
