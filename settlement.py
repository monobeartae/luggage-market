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
        member_id: total_money_received
    }
    """

    totals = defaultdict(float)

    for sale in sales:

        totals[sale["payer_member_id"]] += sale["sale_price"]

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


def calculate_transfers(revenue, received):
    """
    Computes who should pay whom.

    Returns

    [
        {
            "from": member_id,
            "to": member_id,
            "amount": 15.50
        }
    ]
    """

    balances = {}

    members = set(revenue.keys()) | set(received.keys())

    for member in members:

        balances[member] = (
            received.get(member, 0)
            -
            revenue.get(member, 0)
        )

    creditors = []
    debtors = []

    for member, balance in balances.items():

        if balance > 0.01:

            creditors.append(
                [member, balance]
            )

        elif balance < -0.01:

            debtors.append(
                [member, -balance]
            )

    transfers = []

    creditor_index = 0
    debtor_index = 0

    while (
        creditor_index < len(creditors)
        and
        debtor_index < len(debtors)
    ):

        creditor = creditors[creditor_index]
        debtor = debtors[debtor_index]

        amount = min(
            creditor[1],
            debtor[1]
        )

        transfers.append({

            "from": debtor[0],

            "to": creditor[0],

            "amount": round(amount, 2)

        })

        creditor[1] -= amount
        debtor[1] -= amount

        if creditor[1] < 0.01:

            creditor_index += 1

        if debtor[1] < 0.01:

            debtor_index += 1

    return transfers


def build_summary(
    members,
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
        id_to_name[member_id]: amount
        for member_id, amount in received.items()
    }

    items = {
        id_to_name[member_id]: quantity
        for member_id, quantity in items.items()
    }

    transfers = [
        {
            "from": id_to_name[t["from"]],
            "to": id_to_name[t["to"]],
            "amount": t["amount"],
        }
        for t in transfers
    ]

    return (items, revenue, received, transfers)
