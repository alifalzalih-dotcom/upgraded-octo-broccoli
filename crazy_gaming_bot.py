"""
╔══════════════════════════════════════════════════════╗
║     FF PANEL STORE BOT - COMPLETE SOURCE CODE     ║
║          with LEADERBOARD Feature Added              ║
╚══════════════════════════════════════════════════════╝

Install:  pip install pyTelegramBotAPI
Run:      python crazy_gaming_bot.py
"""

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import json, os, datetime, random, string

# ─────────────────────────────────────────
#  CONFIG  —  apna token aur UPI yahan dalo
# ─────────────────────────────────────────
BOT_TOKEN  = "YOUR_BOT_TOKEN_HERE"          # @BotFather se lena
ADMIN_ID   = 123456789                       # apna Telegram user ID
UPI_ID     = "alialfaiz550@okicici"
UPI_NAME   = "Alfaiz Ali"
SUPPORT    = "@ffpanelsupport"
CHANNEL    = "t.me/ffpanelstore"

bot = telebot.TeleBot(BOT_TOKEN)

# ─────────────────────────────────────────
#  DATA FILES
# ─────────────────────────────────────────
USERS_FILE   = "users.json"
ORDERS_FILE  = "orders.json"
KEYS_FILE    = "keys.json"

def load(file):
    if os.path.exists(file):
        with open(file) as f:
            return json.load(f)
    return {}

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# ─────────────────────────────────────────
#  PRODUCTS
# ─────────────────────────────────────────
PRODUCTS = {
    "Android": {
        "DRIPCLIENT NONROOT FF": {
            "features": ["NON ROOT", "ESP", "AIM ASSIST", "HIGH DAMAGE"],
            "status": "🟢 SAFE",
            "plans": [
                {"label": "₹90 • 1 DaYS NONROOT",  "price": 90,  "days": 1},
                {"label": "₹180 • 3 DaYS NONROOT", "price": 180, "days": 3},
                {"label": "₹349 • 7 DaYS NONROOT",  "price": 349, "days": 7},
                {"label": "₹599 • 15 DaYS NONROOT", "price": 599, "days": 15},
                {"label": "₹900 • 30 DaYS NONROOT", "price": 900, "days": 30},
            ]
        },
        "HG CHEATS FF NONROOT+ROOT": {
            "features": ["NON ROOT + ROOT", "ESP", "AIMBOT", "SPEED HACK"],
            "status": "🟢 SAFE",
            "plans": [
                {"label": "₹99 • 1 DAY",   "price": 99,  "days": 1},
                {"label": "₹249 • 7 DAYS",  "price": 249, "days": 7},
                {"label": "₹499 • 30 DAYS", "price": 499, "days": 30},
            ]
        },
        "PATO TEAM FF NONROOT+ROOT": {
            "features": ["NON ROOT + ROOT", "WALL HACK", "AIM ASSIST"],
            "status": "🟢 SAFE",
            "plans": [
                {"label": "₹89 • 1 DAY",   "price": 89,  "days": 1},
                {"label": "₹299 • 7 DAYS",  "price": 299, "days": 7},
                {"label": "₹799 • 30 DAYS", "price": 799, "days": 30},
            ]
        },
        "PRIME HOOK FF NONROOT": {
            "features": ["NON ROOT", "ESP", "HIGH DAMAGE"],
            "status": "🟢 SAFE",
            "plans": [
                {"label": "₹79 • 1 DAY",   "price": 79,  "days": 1},
                {"label": "₹199 • 7 DAYS",  "price": 199, "days": 7},
                {"label": "₹599 • 30 DAYS", "price": 599, "days": 30},
            ]
        },
    },
    "iPhone": {
        "IPHONE CHEAT FF": {
            "features": ["iOS SUPPORT", "ESP", "AIM ASSIST"],
            "status": "🟢 SAFE",
            "plans": [
                {"label": "₹149 • 1 DAY",   "price": 149, "days": 1},
                {"label": "₹499 • 7 DAYS",  "price": 499, "days": 7},
                {"label": "₹999 • 30 DAYS", "price": 999, "days": 30},
            ]
        }
    },
    "PC Cheats": {
        "PC HACK FF": {
            "features": ["PC SUPPORT", "FULL ESP", "AIMBOT", "NO RECOIL"],
            "status": "🟢 SAFE",
            "plans": [
                {"label": "₹199 • 1 DAY",    "price": 199,  "days": 1},
                {"label": "₹599 • 7 DAYS",   "price": 599,  "days": 7},
                {"label": "₹1299 • 30 DAYS", "price": 1299, "days": 30},
            ]
        }
    },
    "Root + VPhone": {
        "ROOT VPHONE HACK": {
            "features": ["ROOT + VPHONE", "FULL FEATURES", "UNDETECTABLE"],
            "status": "🟢 SAFE",
            "plans": [
                {"label": "₹129 • 1 DAY",   "price": 129, "days": 1},
                {"label": "₹399 • 7 DAYS",  "price": 399, "days": 7},
                {"label": "₹899 • 30 DAYS", "price": 899, "days": 30},
            ]
        }
    }
}

# ─────────────────────────────────────────
#  KEYBOARDS
# ─────────────────────────────────────────
def main_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🛒 Shop"))
    kb.add(KeyboardButton("👤 My Profile"), KeyboardButton("📄 History"))
    kb.add(KeyboardButton("🎬 How To Use"), KeyboardButton("📞 Helpline"))
    kb.add(KeyboardButton("🏆 Leaderboard"))   # ← NEW BUTTON
    return kb

def back_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("⬅️ Back"))
    return kb

# ─────────────────────────────────────────
#  HELPER – generate order ref
# ─────────────────────────────────────────
def gen_ref():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# ─────────────────────────────────────────
#  /start
# ─────────────────────────────────────────
@bot.message_handler(commands=["start"])
def start(msg):
    uid  = str(msg.from_user.id)
    name = msg.from_user.first_name or "User"
    users = load(USERS_FILE)
    if uid not in users:
        users[uid] = {
            "name": name,
            "username": msg.from_user.username or "",
            "joined": str(datetime.date.today()),
            "total_spent": 0,
            "orders": 0
        }
        save(USERS_FILE, users)
    text = (
        f"✨ WELCOME TO FF PANEL STORE ✨\n"
        f"👋 Hello, {name}!\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"├ 🛍️ Store: Buy premium services. Instant Delivery !!\n"
        f"├ 👤 Profile: Your Account Details.\n"
        f"├ 📅 History: Track your Orders.\n"
        f"├ 🎬 How to Use: How to buy Key\n"
        f"├ 🏆 Leaderboard: Top Buyers Ranking\n"
        f"└ 🔴 Help: Get Support from Owner.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(msg.chat.id, text, reply_markup=main_keyboard())

# ─────────────────────────────────────────
#  🏆 LEADERBOARD  (NEW FEATURE)
# ─────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "🏆 Leaderboard")
def leaderboard(msg):
    users = load(USERS_FILE)
    if not users:
        bot.send_message(msg.chat.id, "🏆 Leaderboard abhi khali hai!", reply_markup=main_keyboard())
        return

    # Sort by total_spent descending
    ranked = sorted(users.items(), key=lambda x: x[1].get("total_spent", 0), reverse=True)

    medals = ["🥇", "🥈", "🥉"]
    lines  = ["🏆 *TOP BUYERS LEADERBOARD* 🏆", "━━━━━━━━━━━━━━━━━━━━━"]

    for i, (uid, info) in enumerate(ranked[:10]):
        medal    = medals[i] if i < 3 else f"#{i+1}"
        uname    = f"@{info['username']}" if info.get("username") else info.get("name", "User")
        spent    = info.get("total_spent", 0)
        orders   = info.get("orders", 0)
        lines.append(f"{medal} *{uname}*\n    💰 ₹{spent} spent | 📦 {orders} orders")

    lines.append("━━━━━━━━━━━━━━━━━━━━━")
    lines.append("🔥 Keep buying to climb the ranks!")

    # Show current user's rank
    my_rank = next((i+1 for i,(k,_) in enumerate(ranked) if k == str(msg.from_user.id)), None)
    if my_rank:
        my_data = users.get(str(msg.from_user.id), {})
        lines.append(f"\n👤 Your Rank: #{my_rank} | ₹{my_data.get('total_spent',0)} spent")

    bot.send_message(msg.chat.id, "\n".join(lines), parse_mode="Markdown", reply_markup=main_keyboard())

# ─────────────────────────────────────────
#  🛒 SHOP
# ─────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "🛒 Shop")
def shop(msg):
    kb = InlineKeyboardMarkup()
    for cat in PRODUCTS:
        kb.add(InlineKeyboardButton(cat, callback_data=f"cat_{cat}"))
    kb.add(InlineKeyboardButton("🔄 Refresh", callback_data="refresh"))
    bot.send_message(
        msg.chat.id,
        "🏪 LICENSE KEY GENERATOR STORE 🏪\n\n"
        "🔑 License Key Generator\n⏳ Instant Delivery\n🔒 Secure Payment\n📞 24/7 Support\n\n"
        "👇 Please Select Your Product 👇",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("cat_"))
def select_category(call):
    cat  = call.data[4:]
    prods = PRODUCTS.get(cat, {})
    kb   = InlineKeyboardMarkup()
    for p in prods:
        kb.add(InlineKeyboardButton(p, callback_data=f"prod_{cat}__{p}"))
    kb.add(InlineKeyboardButton("⬅️ Back", callback_data="back_shop"))
    bot.edit_message_text("📦 Select Product", call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("prod_"))
def select_product(call):
    _, rest = call.data.split("_", 1)
    cat, pname = rest[4:].split("__", 1)
    prod = PRODUCTS[cat][pname]

    feats = "\n".join(f"• {f}" for f in prod["features"])
    text  = f"📦 *{pname}*\n{'─'*30}\n🔥 Features:\n{feats}\n\n⚠️ Status:\n{prod['status']}"

    kb = InlineKeyboardMarkup()
    for plan in prod["plans"]:
        kb.add(InlineKeyboardButton(plan["label"], callback_data=f"plan_{cat}__{pname}__{plan['price']}__{plan['days']}"))
    kb.add(InlineKeyboardButton("🎬 Watch Gameplay", url=CHANNEL))
    kb.add(InlineKeyboardButton("⬅️ Back", callback_data=f"cat_{cat}"))
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=kb, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: c.data.startswith("plan_"))
def select_plan(call):
    parts  = call.data[5:].split("__")
    cat, pname, price, days = parts[0], parts[1], int(parts[2]), int(parts[3])

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("💳 UPI", callback_data=f"pay_upi__{cat}__{pname}__{price}__{days}"))
    kb.add(InlineKeyboardButton("⬅️ Back", callback_data=f"prod_{cat}__{pname}"))
    bot.edit_message_text("💳 Choose payment method:", call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("pay_upi__"))
def pay_upi(call):
    parts = call.data[9:].split("__")
    cat, pname, price, days = parts[0], parts[1], int(parts[2]), int(parts[3])
    ref = gen_ref()

    orders = load(ORDERS_FILE)
    orders[ref] = {
        "user_id":  str(call.from_user.id),
        "product":  pname,
        "price":    price,
        "days":     days,
        "method":   "UPI",
        "status":   "pending",
        "created":  str(datetime.datetime.now())
    }
    save(ORDERS_FILE, orders)

    # QR URL via chart API
    upi_link = f"upi://pay?pa={UPI_ID}&pn={UPI_NAME}&am={price}&cu=INR&tn=Order:{ref}"
    qr_url   = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={upi_link}"

    text = (
        f"🧾 *ORDER CREATED*\n\n"
        f"📦 Product: {pname}\n"
        f"💰 Amount: ₹{price}\n"
        f"⏳ Duration: {days} Day(s)\n\n"
        f"💳 Method: UPI\n"
        f"📌 Details:\n`{UPI_ID}`\n\n"
        f"🧾 Ref:\n`{ref}`\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"Please pay using the above details.\nClick below after payment."
    )
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✅ I Have Paid", callback_data=f"paid_{ref}"))

    bot.send_photo(call.message.chat.id, qr_url, caption=text, parse_mode="Markdown", reply_markup=kb)
    bot.delete_message(call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda c: c.data.startswith("paid_"))
def i_have_paid(call):
    ref    = call.data[5:]
    orders = load(ORDERS_FILE)
    if ref not in orders:
        bot.answer_callback_query(call.id, "❌ Order not found!")
        return

    orders[ref]["status"] = "verification"
    save(ORDERS_FILE, orders)
    o = orders[ref]

    # Notify admin
    bot.send_message(
        ADMIN_ID,
        f"💰 *NEW PAYMENT CLAIM*\n\n"
        f"👤 User: {call.from_user.first_name} (@{call.from_user.username})\n"
        f"🆔 ID: {call.from_user.id}\n"
        f"📦 Product: {o['product']}\n"
        f"💰 Amount: ₹{o['price']}\n"
        f"📅 Duration: {o['days']} Day(s)\n"
        f"🧾 Ref: `{ref}`",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{ref}"),
            InlineKeyboardButton("❌ Reject",  callback_data=f"reject_{ref}")
        ]])
    )
    bot.answer_callback_query(call.id, "✅ Payment submitted! Waiting for verification.")
    bot.send_message(call.message.chat.id,
        "⏳ Payment sent for verification!\nYou'll receive your key shortly. ✅",
        reply_markup=main_keyboard())

# ─────────────────────────────────────────
#  ADMIN – Approve / Reject
# ─────────────────────────────────────────
@bot.callback_query_handler(func=lambda c: c.data.startswith("approve_"))
def approve_order(call):
    if call.from_user.id != ADMIN_ID:
        return
    ref    = call.data[8:]
    orders = load(ORDERS_FILE)
    users  = load(USERS_FILE)
    keys   = load(KEYS_FILE)

    if ref not in orders:
        bot.answer_callback_query(call.id, "Order not found")
        return

    o  = orders[ref]
    o["status"] = "approved"

    # Generate license key
    lic_key = "CG-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    o["key"] = lic_key
    save(ORDERS_FILE, orders)

    # Update user stats for leaderboard
    uid = o["user_id"]
    if uid in users:
        users[uid]["total_spent"] = users[uid].get("total_spent", 0) + o["price"]
        users[uid]["orders"]      = users[uid].get("orders", 0) + 1
        save(USERS_FILE, users)

    # Send key to user
    bot.send_message(
        int(uid),
        f"✅ *Payment Approved!*\n\n"
        f"📦 Product: {o['product']}\n"
        f"⏳ Duration: {o['days']} Day(s)\n\n"
        f"🔑 Your License Key:\n`{lic_key}`\n\n"
        f"📥 Download: {CHANNEL}\n"
        f"📞 Support: {SUPPORT}",
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )
    bot.answer_callback_query(call.id, "✅ Order Approved & Key Sent!")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.send_message(call.message.chat.id, f"✅ Order `{ref}` approved.", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: c.data.startswith("reject_"))
def reject_order(call):
    if call.from_user.id != ADMIN_ID:
        return
    ref    = call.data[7:]
    orders = load(ORDERS_FILE)
    if ref not in orders:
        return
    uid = orders[ref]["user_id"]
    orders[ref]["status"] = "rejected"
    save(ORDERS_FILE, orders)
    bot.send_message(int(uid),
        f"❌ Payment rejected for order `{ref}`.\nContact support: {SUPPORT}",
        parse_mode="Markdown", reply_markup=main_keyboard())
    bot.answer_callback_query(call.id, "❌ Order Rejected")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

# ─────────────────────────────────────────
#  👤 MY PROFILE
# ─────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "👤 My Profile")
def my_profile(msg):
    uid   = str(msg.from_user.id)
    users = load(USERS_FILE)
    u     = users.get(uid, {})
    orders = load(ORDERS_FILE)
    my_orders = [o for o in orders.values() if o.get("user_id") == uid]
    approved  = [o for o in my_orders if o.get("status") == "approved"]

    # Leaderboard rank
    ranked = sorted(users.items(), key=lambda x: x[1].get("total_spent", 0), reverse=True)
    rank   = next((i+1 for i,(k,_) in enumerate(ranked) if k == uid), "N/A")

    text = (
        f"👤 *My Profile*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🪪 Name: {u.get('name','—')}\n"
        f"🆔 User ID: `{uid}`\n"
        f"📅 Joined: {u.get('joined','—')}\n"
        f"📦 Total Orders: {u.get('orders', 0)}\n"
        f"💰 Total Spent: ₹{u.get('total_spent', 0)}\n"
        f"🏆 Leaderboard Rank: #{rank}\n"
        f"━━━━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(msg.chat.id, text, parse_mode="Markdown", reply_markup=main_keyboard())

# ─────────────────────────────────────────
#  📄 HISTORY
# ─────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📄 History")
def history(msg):
    uid    = str(msg.from_user.id)
    orders = load(ORDERS_FILE)
    mine   = [(ref, o) for ref, o in orders.items() if o.get("user_id") == uid]

    if not mine:
        bot.send_message(msg.chat.id, "📄 No orders yet!", reply_markup=main_keyboard())
        return

    lines = ["📄 *Order History*\n━━━━━━━━━━━━━━━━━━━━━"]
    for ref, o in reversed(mine[-10:]):
        status_icon = {"approved": "✅", "rejected": "❌", "pending": "⏳", "verification": "🔍"}.get(o["status"], "❓")
        lines.append(
            f"{status_icon} *{o['product']}*\n"
            f"   💰 ₹{o['price']} | ⏳ {o['days']}d | 🧾 `{ref}`"
        )
    lines.append("━━━━━━━━━━━━━━━━━━━━━")
    bot.send_message(msg.chat.id, "\n".join(lines), parse_mode="Markdown", reply_markup=main_keyboard())

# ─────────────────────────────────────────
#  🎬 HOW TO USE
# ─────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "🎬 How To Use")
def how_to_use(msg):
    text = (
        "🎬 *How To Use*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "1️⃣ Click *Shop* → Select Category\n"
        "2️⃣ Select Product → Choose Plan\n"
        "3️⃣ Pay via UPI using QR or UPI ID\n"
        "4️⃣ Click *I Have Paid*\n"
        "5️⃣ Admin verifies & sends License Key\n"
        "6️⃣ Download file from channel\n"
        "7️⃣ Use key to activate\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"📥 Channel: {CHANNEL}\n"
        f"📞 Support: {SUPPORT}"
    )
    bot.send_message(msg.chat.id, text, parse_mode="Markdown", reply_markup=main_keyboard())

# ─────────────────────────────────────────
#  📞 HELPLINE
# ─────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📞 Helpline")
def helpline(msg):
    text = (
        f"📞 *Helpline*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"👨‍💼 Support: {SUPPORT}\n"
        f"📥 Channel: {CHANNEL}\n"
        f"🕐 Timing: 24/7\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"Click below to contact support 👇"
    )
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("💬 Contact Support", url=f"https://t.me/{SUPPORT[1:]}"))
    bot.send_message(msg.chat.id, text, parse_mode="Markdown", reply_markup=kb)

# ─────────────────────────────────────────
#  MISC CALLBACKS
# ─────────────────────────────────────────
@bot.callback_query_handler(func=lambda c: c.data in ["back_shop", "refresh"])
def back_shop(call):
    shop(call.message)

# ─────────────────────────────────────────
#  ADMIN COMMANDS
# ─────────────────────────────────────────
@bot.message_handler(commands=["stats"])
def admin_stats(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    users  = load(USERS_FILE)
    orders = load(ORDERS_FILE)
    total_revenue = sum(o["price"] for o in orders.values() if o.get("status") == "approved")
    pending = sum(1 for o in orders.values() if o.get("status") in ["pending", "verification"])

    bot.send_message(msg.chat.id,
        f"📊 *Bot Stats*\n"
        f"👥 Total Users: {len(users)}\n"
        f"📦 Total Orders: {len(orders)}\n"
        f"✅ Approved: {sum(1 for o in orders.values() if o.get('status')=='approved')}\n"
        f"⏳ Pending: {pending}\n"
        f"💰 Total Revenue: ₹{total_revenue}",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=["broadcast"])
def broadcast(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    text = msg.text.replace("/broadcast", "").strip()
    if not text:
        bot.send_message(msg.chat.id, "Usage: /broadcast Your message here")
        return
    users = load(USERS_FILE)
    sent = 0
    for uid in users:
        try:
            bot.send_message(int(uid), f"📢 *Announcement*\n\n{text}", parse_mode="Markdown")
            sent += 1
        except:
            pass
    bot.send_message(msg.chat.id, f"✅ Broadcast sent to {sent} users.")

# ─────────────────────────────────────────
#  START POLLING
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 FF PANEL STORE Bot Started!")
    print("🏆 Leaderboard Feature: ACTIVE")
    bot.infinity_polling()
