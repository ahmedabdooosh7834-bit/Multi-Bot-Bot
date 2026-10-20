import os
import re
import random
import zipfile
import threading
from flask import Flask
from colorama import init, Fore, Style
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

init(autoreset=True)

TOKEN = "7946580929:AAFOWq2gREmKfZmrNsRMqBOqpdFLZp97oB4"
ALLOWED_USERNAME = "Akk_Taiyou_Asano"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NETFLIX_ZIP = os.path.join(BASE_DIR, "x4015_Netflix_COOKIES.zip")
CRUNCHYROLL_FILE = os.path.join(BASE_DIR, "crunchyroll_accounts.txt")
MINECRAFT_FILE = os.path.join(BASE_DIR, "minecraft_accounts.txt")
HOTMAIL_FILE = os.path.join(BASE_DIR, "hotmail_accounts.txt")
IPTV_FILE = os.path.join(BASE_DIR, "iptv_accounts.txt")
STEAM_FILE = os.path.join(BASE_DIR, "steam_accounts.txt")
SPOTIFY_FILE = os.path.join(BASE_DIR, "spotify_accounts.txt")
KICK_FILE = os.path.join(BASE_DIR, "kick_accounts.txt")
G2A_FILE = os.path.join(BASE_DIR, "g2a_accounts.txt")
CODES_FILE = os.path.join(BASE_DIR, "codes_db.txt")
USERS_FILE = os.path.join(BASE_DIR, "users_db.txt")

EPIC_GIF_ID = "CgACAgQAAxkBAAID8GrWUp6oFYRL0wXnz84eY-dpMu9uAAItIAACYEq5Unt0oPSbvFyUPQQ"

# --- خادم الويب المستقر باستخدام Flask لإرضاء منصة Railway ---
app_flask = Flask(__name__)

@app_flask.route('/')
def health_check():
    return "Bot is alive and running!", 200

def run_flask_server():
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def is_authorized(update: Update) -> bool:
    user = update.effective_user
    if user and user.username:
        return user.username.lower() == ALLOWED_USERNAME.lower()
    return False

def save_user(user_id):
    try:
        users = set()
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                users = set(line.strip() for line in f if line.strip())
        if str(user_id) not in users:
            with open(USERS_FILE, "a", encoding="utf-8") as f:
                f.write(f"{user_id}\n")
    except Exception:
        pass

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.animation:
        file_id = update.message.animation.file_id
        await update.message.reply_text(f"✨ **GIF File ID:**\n{file_id}", parse_mode="Markdown")

def get_random_netflix():
    if not os.path.exists(NETFLIX_ZIP):
        return None
    try:
        with zipfile.ZipFile(NETFLIX_ZIP, 'r') as archive:
            file_list = [f for f in archive.infolist() if not f.is_dir() and f.filename.endswith('.txt')]
            if not file_list:
                return None
            selected_file = random.choice(file_list)
            filename = os.path.basename(selected_file.filename)
            tags = re.findall(r'\[(.*?)\]', filename)
            plan = tags[0].strip() if len(tags) >= 1 and tags[0].strip() else "Netflix Premium VIP"
            region = tags[3].strip() if len(tags) >= 4 else "Global"
            email = tags[4].strip() if len(tags) >= 5 else "netflix_user@vip.com"

            with archive.open(selected_file) as f:
                cookie_content = f.read().decode('utf-8', errors='ignore').strip()

            return {
                "platform": "Netflix",
                "email": email,
                "password": "🔐 Secure Session Cookie",
                "plan": plan,
                "region": region,
                "data": cookie_content,
                "login": "https://www.netflix.com/login"
            }
    except Exception as e:
        print(f"Netflix Error: {e}")
        return None

def get_random_text_account(file_path, platform_name):
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
        if not lines:
            return None
        
        selected_line = random.choice(lines)
        parts = selected_line.split("|")
        
        email = parts[0].strip() if len(parts) > 0 else "user@vip.com"
        password = parts[1].strip() if len(parts) > 1 else "N/A"
        plan = parts[2].strip() if len(parts) > 2 else "VIP Access"
        region = parts[3].strip() if len(parts) > 3 else "Global"
        data = parts[4].strip() if len(parts) > 4 else ""

        login_urls = {
            "Crunchyroll": "https://www.crunchyroll.com/login",
            "Minecraft": "https://www.minecraft.net/en-us/login",
            "Hotmail": "https://outlook.live.com",
            "IPTV": "http://vpn.silver-iptval.store",
            "Steam": "https://store.steampowered.com/login/",
            "Spotify": "https://accounts.spotify.com/en/login",
            "Kick": "https://kick.com/",
            "G2A": "https://www.g2a.com/"
        }

        return {
            "platform": platform_name,
            "email": email,
            "password": password,
            "plan": plan,
            "region": region,
            "data": data,
            "login": login_urls.get(platform_name, "https://www.g2a.com/")
        }
    except Exception as e:
        print(f"Error reading {platform_name}: {e}")
        return None

def fetch_account_by_platform(platform_name):
    p = platform_name.lower()
    if "net" in p:
        return get_random_netflix()
    elif "crunchy" in p:
        return get_random_text_account(CRUNCHYROLL_FILE, "Crunchyroll")
    elif "mine" in p:
        return get_random_text_account(MINECRAFT_FILE, "Minecraft")
    elif "iptv" in p:
        return get_random_text_account(IPTV_FILE, "IPTV")
    elif "hot" in p:
        return get_random_text_account(HOTMAIL_FILE, "Hotmail")
    elif "steam" in p:
        return get_random_text_account(STEAM_FILE, "Steam")
    elif "spotify" in p:
        return get_random_text_account(SPOTIFY_FILE, "Spotify")
    elif "kick" in p:
        return get_random_text_account(KICK_FILE, "Kick")
    elif "g2a" in p:
        return get_random_text_account(G2A_FILE, "G2A")
    else:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user:
        save_user(user.id)

    welcome_text = (
        "✨ ════════════════════════════ ✨\n"
        "🔥 **WELCOME TO THE ULTIMATE VIP VAULT** 🔥\n"
        "✨ ════════════════════════════ ✨\n\n"
        "🛡 **System Status:** Online & Secured\n"
        "⚡ **Master Controller:** @Akk_Taiyou_Asano\n\n"
        "🎯 **Available Commands:**\n"
        "🎁 /redeem <CODE> — Redeem your VIP access code to instantly get a random account from stock!\n\n"
    )

    if is_authorized(update):
        welcome_text += (
            "👑 **Admin Commands & Features:**\n"
            "🍿 /netflix  |  🌸 /crunchyroll  |  ⛏️ /minecraft\n"
            "📺 /iptv     |  📧 /hotmail     |  🎮 /steam\n"
            "🎧 /spotify  |  🟣 /kick        |  🛒 /g2a\n\n"
            "📥 /addstock <platform> — Auto-sort & add stock files\n"
            "➕ /addcode <code> <platform> — Link a code to stock\n"
            "🔄 /check — Clean & validate all stock databases\n"
            "📊 /stock — Live inventory stock statistics\n"
            "🗑️ /clearstock <platform> — Reset platform stock\n"
            "📢 /broadcast <message> — Broadcast message to users\n\n"
        )
    
    welcome_text += "✨ ════════════════════════════ ✨"

    keyboard = [
        [InlineKeyboardButton("🎁 How to Redeem", callback_data="help_redeem")],
        [InlineKeyboardButton("💎 Bot Channel / Support", url="https://t.me/Akk_M_Bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_animation(
        animation=EPIC_GIF_ID,
        caption=welcome_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def check_stock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    files_to_check = {
        "Crunchyroll": CRUNCHYROLL_FILE,
        "Minecraft": MINECRAFT_FILE,
        "Hotmail": HOTMAIL_FILE,
        "IPTV": IPTV_FILE,
        "Steam": STEAM_FILE,
        "Spotify": SPOTIFY_FILE,
        "Kick": KICK_FILE,
        "G2A": G2A_FILE
    }

    report = "🔄 **Stock Health Check & Cleanup Report:**\n\n"
    total_valid = 0
    total_removed = 0

    for name, filepath in files_to_check.items():
        if not os.path.exists(filepath):
            report += f"• **{name}:** File not found\n"
            continue

        valid_lines = []
        removed = 0
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            for line in lines:
                clean = line.strip()
                if clean and not clean.startswith("#") and ":" in clean:
                    valid_lines.append(clean + "\n")
                else:
                    removed += 1

            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(valid_lines)

            total_valid += len(valid_lines)
            total_removed += removed
            report += f"• **{name}:** 🟢 Valid: {len(valid_lines)} | 🔴 Cleaned: {removed}\n"
        except Exception:
            report += f"• **{name}:** Error\n"

    report += f"\n📊 **Total Valid Accounts:** {total_valid}\n"
    report += f"🧹 **Total Junk Removed:** {total_removed}"
    await update.message.reply_text(report, parse_mode="Markdown")

async def stock_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    platforms = {
        "Netflix (ZIP)": NETFLIX_ZIP,
        "Crunchyroll": CRUNCHYROLL_FILE,
        "Minecraft": MINECRAFT_FILE,
        "Hotmail": HOTMAIL_FILE,
        "IPTV": IPTV_FILE,
        "Steam": STEAM_FILE,
        "Spotify": SPOTIFY_FILE,
        "Kick": KICK_FILE,
        "G2A": G2A_FILE
    }

    msg = "📊 **VIP Vault Live Stock Inventory:**\n\n"
    for name, path in platforms.items():
        count = 0
        if os.path.exists(path):
            if name.startswith("Netflix"):
                try:
                    with zipfile.ZipFile(path, 'r') as arch:
                        count = len([f for f in arch.infolist() if not f.is_dir() and f.filename.endswith('.txt')])
                except:
                    count = 0
            else:
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        count = len([l for l in f if l.strip() and not l.startswith("#")])
                except:
                    count = 0
        msg += f"• **{name}:** {count} accounts available\n"

    await update.message.reply_text(msg, parse_mode="Markdown")

async def clear_stock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("⚠️ **Usage:** /clearstock <platform>\nPlatforms: crunchyroll, minecraft, iptv, hotmail, steam, spotify, kick, g2a", parse_mode="Markdown")
        return

    platform = args[0].lower().strip()
    file_map = {
        "crunchyroll": CRUNCHYROLL_FILE,
        "minecraft": MINECRAFT_FILE,
        "hotmail": HOTMAIL_FILE,
        "iptv": IPTV_FILE,
        "steam": STEAM_FILE,
        "spotify": SPOTIFY_FILE,
        "kick": KICK_FILE,
        "g2a": G2A_FILE
    }

    if platform not in file_map:
        await update.message.reply_text(f"⚠️ **Invalid platform!** Choose from: {', '.join(file_map.keys())}")
        return

    target_file = file_map[platform]
    try:
        with open(target_file, "w", encoding="utf-8") as f:
            f.write("")
        await update.message.reply_text(f"🗑️ **Success!** Stock file for {platform.upper()} has been completely cleared and reset.", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error clearing stock: {e}")

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("⚠️ **Usage:** /broadcast <your announcement message>", parse_mode="Markdown")
        return

    if not os.path.exists(USERS_FILE):
        await update.message.reply_text("⚠️ No user records found yet.")
        return

    success = 0
    failed = 0
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        user_ids = [line.strip() for line in f if line.strip()]

    status_msg = await update.message.reply_text(f"📢 Broadcasting to {len(user_ids)} users...", parse_mode="Markdown")

    for uid in user_ids:
        try:
            await context.bot.send_message(chat_id=int(uid), text=f"📢 **Announcement:**\n\n{text}", parse_mode="Markdown")
            success += 1
        except Exception:
            failed += 1

    await status_msg.edit_text(f"✅ **Broadcast Complete!**\n\nSent: {success}\nFailed: {failed}", parse_mode="Markdown")

async def add_stock_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("⚠️ **Usage Error!**\nSend a .txt or .zip file with the command: /addstock <platform>\nPlatforms: 
etflix, crunchyroll, minecraft, iptv, hotmail, steam, spotify, kick, g2a", parse_mode="Markdown")
        return

    platform = args[0].strip().lower()
    valid_platforms = ["netflix", "crunchyroll", "minecraft", "iptv", "hotmail", "steam", "spotify", "kick", "g2a"]
    
    if platform not in valid_platforms:
        await update.message.reply_text(f"⚠️ **Invalid Platform!** Choose from: {', '.join(valid_platforms)}")
        return

    message = update.message
    document = message.document or (message.reply_to_message and message.reply_to_message.document)

    if not document:
        await update.message.reply_text("⚠️ **Please attach a file (.txt or .zip)** or reply to a file with /addstock <platform>")
        return

    file_name = document.file_name.lower()
    file_path = os.path.join(BASE_DIR, document.file_name)

    try:
        new_file = await context.bot.get_file(document.file_id)
        await new_file.download_to_drive(file_path)

        target_file_map = {
            "crunchyroll": CRUNCHYROLL_FILE,
            "minecraft": MINECRAFT_FILE,
            "hotmail": HOTMAIL_FILE,
            "iptv": IPTV_FILE,
            "steam": STEAM_FILE,
            "spotify": SPOTIFY_FILE,
            "kick": KICK_FILE,
            "g2a": G2A_FILE
        }

        added_lines = 0

        if file_name.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as archive:
                for z_info in archive.infolist():
                    if z_info.is_dir() or not z_info.filename.endswith('.txt'):
                        continue
                    with archive.open(z_info) as z_f:
                        content = z_f.read().decode('utf-8', errors='ignore')
                        lines = content.splitlines()
                        
                        if platform == "netflix":
                            pass
                        else:
                            target_file = target_file_map.get(platform)
                            if target_file:
                                with open(target_file, "a", encoding="utf-8") as out:
                                    for line in lines:
                                        clean_line = line.strip()
                                        if clean_line and not clean_line.startswith("#"):
                                            if "|" not in clean_line:
                                                clean_line = f"{clean_line}|VIP|Global|Active"
                                            out.write(clean_line + "\n")
                                            added_lines += 1
            os.remove(file_path)
            await update.message.reply_text(f"✅ **Success!** Processed ZIP archive and added *{added_lines}* accounts to *{platform.upper()}* stock.", parse_mode="Markdown")

        elif file_name.endswith('.txt'):
            target_file = target_file_map.get(platform)
            if target_file:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as src:
                    lines = src.readlines()
                
                with open(target_file, "a", encoding="utf-8") as out:
                    for line in lines:
                        clean_line = line.strip()
                        if clean_line and not clean_line.startswith("#"):
                            if "|" not in clean_line:
                                clean_line = f"{clean_line}|VIP|Global|Active"
                            out.write(clean_line + "\n")
                            added_lines += 1
            os.remove(file_path)
            await update.message.reply_text(f"✅ **Success!** Added *{added_lines}* organized accounts to *{platform.upper()}* stock.", parse_mode="Markdown")
        else:
            os.remove(file_path)
            await update.message.reply_text("❌ **Unsupported format:** Please upload only .txt or .zip files.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error processing stock file: {e}")

async def add_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    args = context.args
    if len(args) < 2:
        await update.message.reply_text("⚠️ **Usage Error!**\nFormat: /addcode <code> <platform>\nPlatforms: 
etflix, crunchyroll, minecraft, iptv, hotmail, steam, spotify, kick, g2a", parse_mode="Markdown")
        return

    code = args[0].strip()
    platform = args[1].strip().lower()

    valid_platforms = ["netflix", "crunchyroll", "minecraft", "iptv", "hotmail", "steam", "spotify", "kick", "g2a"]
    if platform not in valid_platforms:
        await update.message.reply_text(f"⚠️ **Invalid Platform!** Choose from: {', '.join(valid_platforms)}")
        return

    try:
        if os.path.exists(CODES_FILE):
            with open(CODES_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith(code + "|"):
                        await update.message.reply_text("⚠️ **Error:** This code already exists!")
                        return

        with open(CODES_FILE, "a", encoding="utf-8") as f:
            f.write(f"{code}|{platform}|active\n")

        await update.message.reply_text(f"✅ **Success!** Code {code} linked to platform stock: *{platform.upper()}*", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error saving code: {e}")

async def redeem_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user:
        save_user(user.id)
    username_str = f"@{user.username}" if user.username else user.first_name
    user_id = user.id

    args = context.args
    if not args:
        await update.message.reply_text("⚠️ **Please provide a code!**\nUsage: /redeem <code>", parse_mode="Markdown")
        return

    user_code = args[0].strip()
    
    if not os.path.exists(CODES_FILE):
        await update.message.reply_text("❌ **Vault Error:** No redeem codes available in the system.")
        return

    codes_lines = []
    found_platform = None
    updated_lines = []

    try:
        with open(CODES_FILE, "r", encoding="utf-8") as f:
            codes_lines = f.readlines()

        for line in codes_lines:
            parts = line.strip().split("|")
            if len(parts) >= 3:
                c, plat, status = parts[0], parts[1], parts[2]
                if c == user_code and status == "active":
                    found_platform = plat
                    updated_lines.append(f"{c}|{plat}|used\n")
                else:
                    updated_lines.append(line)

        with open(CODES_FILE, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)

        if found_platform:
            print(f"[REDEEM ALERT] User {username_str} (ID: {user_id}) successfully used code '{user_code}' for platform: {found_platform.upper()}")
            
            account = fetch_account_by_platform(found_platform)
            if not account:
                await update.message.reply_text(f"⚠️ **Stock Empty:** The code was valid for *{found_platform.upper()}*, but the stock is currently empty!", parse_mode="Markdown")
                return

            caption = (
                "🎉 ════════════════════════════ 🎉\n"
                f"   🎁 **REDEEMED: {found_platform.upper()} VIP** 🎁   \n"
                "🎉 ════════════════════════════ 🎉\n\n"
                f"💎 **Plan / Tier:** {account['plan']}\n"
                f"🌍 **Region:** {account['region']}\n"
                f"📧 **Username / Email:** {account['email']}\n"
                f"🔑 **Password / Details:** {account['password']}\n\n"
                "🔥 _Enjoy your premium drop from the vault!_"
            )

            keyboard = [
                [InlineKeyboardButton(f"🔗 Open {account['platform']} Portal", url=account["login"])],
                [InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]
            ]
            
            await update.message.reply_animation(
                animation=EPIC_GIF_ID,
                caption=caption,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

            if account.get("data") and len(str(account["data"])) > 10:
                await update.message.reply_text(f"🛡 **SESSION DATA / COOKIE:**\n`{account['data']}`", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ **Invalid or Already Used Code:** Please check your code and try again.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error processing code: {e}")

async def get_netflix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_netflix()
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🎬 **NETFLIX VIP**\n📧 {account['email']}\n🔑 {account['password']}"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    await update.message.reply_text(f"`{account['data']}`", parse_mode="Markdown")

async def get_crunchyroll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(CRUNCHYROLL_FILE, "Crunchyroll")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🌸 **CRUNCHYROLL VIP**\n📧 {account['email']}\n🔑 {account['password']}"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_minecraft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(MINECRAFT_FILE, "Minecraft")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"⛏️ **MINECRAFT VIP**\n👤 {account['email']}\n🔑 {account['password']}"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    if account.get("data"):
        await update.message.reply_text(f"`{account['data']}`", parse_mode="Markdown")

async def get_iptv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(IPTV_FILE, "IPTV")
    if not account:
        account = {"email": "crackhed01", "password": "dca2002a", "plan": "Silver", "region": "http://vpn.silver-iptval.store", "data": "http://vpn.silver-iptval.store/get.php?username=crackhed01&password=dca2002a&type=m3u_plus&output=ts"}
    caption = f"📺 **IPTV STREAM**\n👤 {account['email']}\n🔑 {account['password']}\n🔗 {account['data']}"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_hotmail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(HOTMAIL_FILE, "Hotmail")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"📧 **HOTMAIL VIP**\n📧 {account['email']}\n🔑 {account['password']}"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_steam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(STEAM_FILE, "Steam")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty:** Steam database is empty.")
        return
    caption = f"🎮 **STEAM VIP ACCOUNT**\n👤 {account['email']}\n🔑 {account['password']}"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_spotify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(SPOTIFY_FILE, "Spotify")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty:** Spotify database is empty.")
        return
    caption = f"🎧 **SPOTIFY PREMIUM VIP**\n📧 {account['email']}\n🔑 {account['password']}"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(KICK_FILE, "Kick")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty:** Kick database is empty.")
        return
    caption = f"🟣 **KICK VIP ACCOUNT**\n📧 {account['email']}\n🔑 {account['password']}"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_g2a(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(G2A_FILE, "G2A")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty:** G2A database is empty.")
        return
    caption = f"🛒 **G2A VIP ACCOUNT / KEY**\n📧 {account['email']}\n🔑 {account['password']}"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    username_str = f"@{user.username}" if user.username else user.first_name
    await query.answer()
    
    if query.data == "report_broken":
        print(f"[REPORT] User {username_str} reported a broken account!")
        await query.message.reply_text("🚨 **Report Received:** This account has been flagged as non-working and logged for replacement!")
    elif query.data == "help_redeem":
        await query.message.reply_text(
            "💡 **How to use Redeem Codes:**\n\n"
            "1. Type /redeem CODE or /reedem CODE in the chat.\n"
            "2. The bot will automatically verify your code.\n"
            "3. You will receive a random VIP account instantly from the stock!",
            parse_mode="Markdown"
        )

def run_telegram_bot():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def start_bot():
            request_settings = HTTPXRequest(read_timeout=30.0, write_timeout=30.0, connect_timeout=30.0, pool_timeout=30.0)
            app = Application.builder().token(TOKEN).request(request_settings).build()
            
            app.add_handler(CommandHandler("start", start))
            app.add_handler(CommandHandler("netflix", get_netflix))
            app.add_handler(CommandHandler("crunchyroll", get_crunchyroll))
            app.add_handler(CommandHandler("minecraft", get_minecraft))
            app.add_handler(CommandHandler("iptv", get_iptv))
            app.add_handler(CommandHandler("hotmail", get_hotmail))
            app.add_handler(CommandHandler("steam", get_steam))
            app.add_handler(CommandHandler("spotify", get_spotify))
            app.add_handler(CommandHandler("kick", get_kick))
            app.add_handler(CommandHandler("g2a", get_g2a))
            
            app.add_handler(CommandHandler("addstock", add_stock_file))
            app.add_handler(CommandHandler("addcode", add_code))
            app.add_handler(CommandHandler("redeem", redeem_code))
            app.add_handler(CommandHandler("reedem", redeem_code))

            app.add_handler(CommandHandler("check", check_stock_command))
            app.add_handler(CommandHandler("stock", stock_dashboard))
            app.add_handler(CommandHandler("clearstock", clear_stock_command))
            app.add_handler(CommandHandler("broadcast", broadcast_command))

            app.add_handler(MessageHandler(filters.ANIMATION, get_file_id))
            app.add_handler(CallbackQueryHandler(button_handler))

            await app.initialize()
            await app.start()
            await app.updater.start_polling()
            print("Telegram Bot started successfully in background loop!")
            
            await asyncio.Event().wait()

        loop.run_until_complete(start_bot())
    except Exception as e:
        print(f"Bot thread error: {e}")

def main():
    print("="*65)
    print("    🎁 ULTIMATE G2A & AUTO-STOCK BOT - RUNNING 🎁")
    print("="*65)
    print(f" [🛡] Security Shield Active: Locked exclusively to @{ALLOWED_USERNAME}")
    print("="*65)

    # تشغيل بوت تيليجرام في خيط منفصل
    threading.Thread(target=run_telegram_bot, daemon=True).start()

    # تشغيل خادم Flask على العملية الرئيسية لضمان الاستجابة الفورية لبورت Railway
    port = int(os.environ.get("PORT", 8080))
    print(f"Flask Web Server running on port {port}...")
    app_flask.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    main()
