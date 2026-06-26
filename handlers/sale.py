from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from copy import deepcopy

from models import get_member, get_members, create_sale, get_sales_count


# =========================
# ENTRY POINT
# =========================

async def open_sale_ui(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    members = get_members(chat_id)
    if len(members) == 0:
        await update.message.reply_text(
            "❌ No members found. Add members first using /addmember"
        )
        return

    # Parse price from command
    args = context.args

    if not args:
        await update.message.reply_text("Usage: /sale <price>")
        return

    try:
        price = float(args[0])
        if price <= 0:
            raise ValueError()
    except:
        await update.message.reply_text("Invalid price. Example: /sale 12")
        return

    # Init state
    context.user_data["sale"] = {
        "payee": members[0]["id"] if members else None,
        "price": price,
        "items": {m["id"]: 0 for m in members},
    }

    await update.message.reply_text(
        render_ui(context.user_data["sale"], members),
        reply_markup=build_keyboard(members, context.user_data["sale"]),
    )

# =========================
# MAIN CALLBACK ROUTER
# =========================

async def handle_sale_ui(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    sale = context.user_data.get("sale")
    prev = deepcopy(sale)

    if not sale:
        await query.edit_message_text("Session expired.")
        return

    chat_id = query.message.chat.id
    members = get_members(chat_id)

    # -------------------------
    # payee SELECT
    # -------------------------
    if data.startswith("sale_payee_"):
        sale["payee"] = int(data.split("_")[-1])

    # -------------------------
    # PLUS
    # -------------------------
    elif data.startswith("sale_plus_"):
        mid = int(data.split("_")[-1])
        sale["items"][mid] += 1

    # -------------------------
    # MINUS
    # -------------------------
    elif data.startswith("sale_minus_"):
        mid = int(data.split("_")[-1])
        sale["items"][mid] = max(0, sale["items"][mid] - 1)

    # -------------------------
    # SAVE
    # -------------------------
    elif data == "sale_save":
        return await save_sale(query, context, sale)

    # -------------------------
    # CANCEL
    # -------------------------
    elif data == "sale_cancel":
        context.user_data.pop("sale", None)
        await query.edit_message_text("Cancelled")
        return

    if sale == prev: # prevent re-render
        return
    # re-render after action
    await query.edit_message_text(
        render_ui(sale, members),
        reply_markup=build_keyboard(members, sale),
    )


# =========================
# UI RENDERING
# =========================

def render_ui(sale, members):

    id_to_name = {m["id"]: m["name"] for m in members}

    text = "💰 *Sale Builder*\n\n"

    text += "payee:\n"
    for m in members:
        selected = "✅" if m["id"] == sale["payee"] else ""
        text += f"{selected} {m['name']}\n"

    text += f"\nPrice: {sale['price']:.2f}\n\n"

    text += "Items:\n"

    total = sum(sale["items"].values()) or 1

    for mid, qty in sale["items"].items():

        name = id_to_name[mid]
        share = (qty / total) * sale["price"] if total else 0

        text += f"{name}: {qty} (${share:.2f})\n"

    return text


# =========================
# KEYBOARD
# =========================

def build_keyboard(members, sale):

    keyboard = []

    # payee row (segmented control)
    keyboard.append([
        InlineKeyboardButton(
            m["name"],
            callback_data=f"sale_payee_{m['id']}"
        )
        for m in members
    ])

    # item controls
    for m in members:
        keyboard.append([
            InlineKeyboardButton("➖", callback_data=f"sale_minus_{m['id']}"),
            InlineKeyboardButton(m["name"], callback_data="ignore"),
            InlineKeyboardButton("➕", callback_data=f"sale_plus_{m['id']}"),
        ])

    keyboard.append([
        InlineKeyboardButton("💾 Save", callback_data="sale_save"),
        InlineKeyboardButton("❌ Cancel", callback_data="sale_cancel"),
    ])

    return InlineKeyboardMarkup(keyboard)


# =========================
# SAVE
# =========================

async def save_sale(query, context, sale):

    chat_id = query.message.chat.id

    items = [
        (mid, qty)
        for mid, qty in sale["items"].items()
        if qty > 0
    ]

    if not items:
        await query.answer("⚠️ Add at least 1 item before saving", show_alert=True)
        return

    sale_id = create_sale(
        chat_id=chat_id,
        payee_member_id=sale["payee"],
        sale_price=sale["price"],
        sale_datetime=datetime.now(),
        items=items,
    )

    context.user_data.pop("sale", None)
    text = f"✅ Saved sale #{get_sales_count(chat_id)}"
    text += f"\n ${sale['price']:.2f} paid to {get_member(sale['payee'])['name']}"
    for owner, qty in sale["items"].items():
        if qty > 0:
            text += f"\n -> {get_member(owner)['name']}: {qty} item(s)"

    await query.edit_message_text(text)

async def handle_sale_text(update: Update, context):

    sale = context.user_data.get("sale")

    if not sale:
        return

    if context.user_data.get("sale_state") != "awaiting_price":
        return

    try:
        price = float(update.message.text)

        if price <= 0:
            raise ValueError()

    except ValueError:
        await update.message.reply_text("Invalid price. Try again.")
        return

    sale["price"] = price
    context.user_data["sale_state"] = None

    chat_id = update.effective_chat.id
    members = get_members(chat_id)

    await update.message.reply_text(
        render_ui(sale, members),
        reply_markup=build_keyboard(members, sale),
    )
