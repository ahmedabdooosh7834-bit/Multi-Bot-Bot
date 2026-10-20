import os
import re
import random
import zipfile
from colorama import init, Fore, Style
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

# Initialize terminal colors
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

EPIC_GIF_ID = "CgACAgQAAxkBAAID8GrWUp6oFYRL0wXnz84eY-dpMu9uAAItIAACYEq5Unt0oPSbvFyUPQQ"

def is_authorized(update: Update) -> bool:
    user = update.effective_user
    if user and user.username:
        return user.username.lower() == ALLOWED_USERNAME.lower()
    return False

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.animation:
        file_id = update.message.animation.file_id
        await update.message.reply_text(f"✨ **GIF File ID:**\n`{file_id}`", parse_mode="Markdown")

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
        print(f"{Fore.RED}[!] Netflix Error: {e}")
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
        print(f"{Fore.RED}[!] Error reading {platform_name}: {e}")
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
    welcome_text = (
        "✨ ════════════════════════════ ✨\n"
        "🔥 **WELCOME TO THE ULTIMATE VIP VAULT** 🔥\n"
        "✨ ════════════════════════════ ✨\n\n"
        "🛡 **System Status:** `Online & Secured`\n"
        "⚡ **Master Controller:** `@Akk_Taiyou_Asano`\n\n"
        "🎯 **Available Commands:**\n"
        "🎁 `/redeem <CODE>` — Redeem your VIP access code to instantly get a random account from stock!\n\n"
    )

    if is_authorized(update):
        welcome_text += (
            "👑 **Admin Commands (Stock Gen):**\n"
            "🍿 `/netflix`  |  🌸 `/crunchyroll`  |  ⛏️ `/minecraft`\n"
            "📺 `/iptv`     |  📧 `/hotmail`     |  🎮 `/steam`\n"
            "🎧 `/spotify`  |  🟣 `/kick`        |  🛒 `/g2a`\n\n"
            "📥 `/addstock <platform>` — Send a .txt or .zip file with this command to auto-sort & add stock!\n"
            "➕ `/addcode <code> <platform>` — Link a code to stock\n"
            "🔄 `/check` — Clean & validate stock databases\n"
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

# --- أداة الفحص وتطهير الستوك المحلية الآمنة ---
async def check_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    files = {
        "Crunchyroll": CRUNCHYROLL_FILE,
        "Minecraft": MINECRAFT_FILE,
        "Hotmail": HOTMAIL_FILE,
        "IPTV": IPTV_FILE,
        "Steam": STEAM_FILE,
        "Spotify": SPOTIFY_FILE,
        "Kick": KICK_FILE,
        "G2A": G2A_FILE
    }

    report = "🔄 **Stock Cleaning & Check Report:**\n\n"
    total_valid = 0

    for name, path in files.items():
        if not os.path.exists(path):
            continue
        valid_lines = []
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    clean = line.strip()
                    if clean and not clean.startswith("#") and len(clean) > 3:
                        valid_lines.append(clean + "\n")
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(valid_lines)
            total_valid += len(valid_lines)
            report += f"• **{name}:** `{len(valid_lines)}` valid accounts\n"
        except Exception:
            pass

    report += f"\n📊 **Total Active Accounts:** `{total_valid}`"
    await update.message.reply_text(report, parse_mode="Markdown")

async def add_stock_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("⚠️ **Usage Error!**\nSend a `.txt` or `.zip` file with the command: `/addstock <platform>`", parse_mode="Markdown")
        return

    platform = args[0].strip().lower()
    valid_platforms = ["netflix", "crunchyroll", "minecraft", "iptv", "hotmail", "steam", "spotify", "kick", "g2a"]
    
    if platform not in valid_platforms:
        await update.message.reply_text(f"⚠️ **Invalid Platform!** Choose from: {', '.join(valid_platforms)}")
        return

    message = update.message
    document = message.document or (message.reply_to_message and message.reply_to_message.document)

    if not document:
        await update.message.reply_text("⚠️ **Please attach a file (.txt or .zip)** or reply to a file with `/addstock <platform>`")
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
                        
                        if platform != "netflix":
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
            await update.message.reply_text(f"✅ **Success!** Added *{added_lines}* accounts to *{platform.upper()}* stock.", parse_mode="Markdown")

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
            await update.message.reply_text(f"✅ **Success!** Added *{added_lines}* accounts to *{platform.upper()}* stock.", parse_mode="Markdown")
        else:
            os.remove(file_path)
            await update.message.reply_text("❌ **Unsupported format:** Please upload only `.txt` or `.zip` files.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def add_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    args = context.args
    if len(args) < 2:
        await update.message.reply_text("⚠️ **Usage Error!**\nFormat: `/addcode <code> <platform>`", parse_mode="Markdown")
        return

    code = args[0].strip()
    platform = args[1].strip().lower()

    valid_platforms = ["netflix", "crunchyroll", "minecraft", "iptv", "hotmail", "steam", "spotify", "kick", "g2a"]
    if platform not in valid_platforms:
        await update.message.reply_text(f"⚠️ **Invalid Platform!**")
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

        await update.message.reply_text(f"✅ **Success!** Code `{code}` linked to *{platform.upper()}*", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def redeem_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username_str = f"@{user.username}" if user.username else user.first_name
    user_id = user.id

    args = context.args
    if not args:
        await update.message.reply_text("⚠️ **Please provide a code!**\nUsage: `/redeem <code>`", parse_mode="Markdown")
        return

    user_code = args[0].strip()
    
    if not os.path.exists(CODES_FILE):
        await update.message.reply_text("❌ **Vault Error:** No redeem codes available.")
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
            account = fetch_account_by_platform(found_platform)
            if not account:
                await update.message.reply_text(f"⚠️ **Stock Empty** for *{found_platform.upper()}*!", parse_mode="Markdown")
                return

            caption = (
                "🎉 ════════════════════════════ 🎉\n"
                f"   🎁 **REDEEMED: {found_platform.upper()} VIP** 🎁   \n"
                "🎉 ════════════════════════════ 🎉\n\n"
                f"💎 **Plan / Tier:** `{account['plan']}`\n"
                f"🌍 **Region:** `{account['region']}`\n"
                f"📧 **Username / Email:** `{account['email']}`\n"
                f"🔑 **Password / Details:** `{account['password']}`\n\n"
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
                await update.message.reply_text(f"🛡 **SESSION DATA / COOKIE:**\n```{account['data']}```", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ **Invalid or Already Used Code:** Please check your code.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def get_netflix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_netflix()
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🎬 **NETFLIX VIP**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    await update.message.reply_text(f"```{account['data']}```", parse_mode="Markdown")

async def get_crunchyroll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(CRUNCHYROLL_FILE, "Crunchyroll")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🌸 **CRUNCHYROLL VIP**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_minecraft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(MINECRAFT_FILE, "Minecraft")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"⛏️ **MINECRAFT VIP**\n👤 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    if account.get("data"):
        await update.message.reply_text(f"```{account['data']}```", parse_mode="Markdown")

async def get_iptv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(IPTV_FILE, "IPTV")
    if not account:
        account = {"email": "crackhed01", "password": "dca2002a", "plan": "Silver", "region": "http://vpn.silver-iptval.store", "data": "http://vpn.silver-iptval.store/get.php?username=crackhed01&password=dca2002a&type=m3u_plus&output=ts"}
    caption = f"📺 **IPTV STREAM**\n👤 `{account['email']}`\n🔑 `{account['password']}`\n🔗 `{account['data']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_hotmail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(HOTMAIL_FILE, "Hotmail")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"📧 **HOTMAIL VIP**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_steam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(STEAM_FILE, "Steam")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🎮 **STEAM VIP ACCOUNT**\n👤 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID,
$botCode = @'
import os
import re
import random
import zipfile
from colorama import init, Fore, Style
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

# Initialize terminal colors
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

EPIC_GIF_ID = "CgACAgQAAxkBAAID8GrWUp6oFYRL0wXnz84eY-dpMu9uAAItIAACYEq5Unt0oPSbvFyUPQQ"

def is_authorized(update: Update) -> bool:
    user = update.effective_user
    if user and user.username:
        return user.username.lower() == ALLOWED_USERNAME.lower()
    return False

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.animation:
        file_id = update.message.animation.file_id
        await update.message.reply_text(f"✨ **GIF File ID:**\n`{file_id}`", parse_mode="Markdown")

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
        print(f"{Fore.RED}[!] Netflix Error: {e}")
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
        print(f"{Fore.RED}[!] Error reading {platform_name}: {e}")
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
    welcome_text = (
        "✨ ════════════════════════════ ✨\n"
        "🔥 **WELCOME TO THE ULTIMATE VIP VAULT** 🔥\n"
        "✨ ════════════════════════════ ✨\n\n"
        "🛡 **System Status:** `Online & Secured`\n"
        "⚡ **Master Controller:** `@Akk_Taiyou_Asano`\n\n"
        "🎯 **Available Commands:**\n"
        "🎁 `/redeem <CODE>` — Redeem your VIP access code to instantly get a random account from stock!\n\n"
    )

    if is_authorized(update):
        welcome_text += (
            "👑 **Admin Commands (Stock Gen):**\n"
            "🍿 `/netflix`  |  🌸 `/crunchyroll`  |  ⛏️ `/minecraft`\n"
            "📺 `/iptv`     |  📧 `/hotmail`     |  🎮 `/steam`\n"
            "🎧 `/spotify`  |  🟣 `/kick`        |  🛒 `/g2a`\n\n"
            "📥 `/addstock <platform>` — Send a .txt or .zip file with this command to auto-sort & add stock!\n"
            "➕ `/addcode <code> <platform>` — Link a code to stock\n"
            "🔄 `/check` — Clean & validate stock databases\n"
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

# --- أداة الفحص وتطهير الستوك المحلية الآمنة ---
async def check_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    files = {
        "Crunchyroll": CRUNCHYROLL_FILE,
        "Minecraft": MINECRAFT_FILE,
        "Hotmail": HOTMAIL_FILE,
        "IPTV": IPTV_FILE,
        "Steam": STEAM_FILE,
        "Spotify": SPOTIFY_FILE,
        "Kick": KICK_FILE,
        "G2A": G2A_FILE
    }

    report = "🔄 **Stock Cleaning & Check Report:**\n\n"
    total_valid = 0

    for name, path in files.items():
        if not os.path.exists(path):
            continue
        valid_lines = []
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    clean = line.strip()
                    if clean and not clean.startswith("#") and len(clean) > 3:
                        valid_lines.append(clean + "\n")
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(valid_lines)
            total_valid += len(valid_lines)
            report += f"• **{name}:** `{len(valid_lines)}` valid accounts\n"
        except Exception:
            pass

    report += f"\n📊 **Total Active Accounts:** `{total_valid}`"
    await update.message.reply_text(report, parse_mode="Markdown")

async def add_stock_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("⚠️ **Usage Error!**\nSend a `.txt` or `.zip` file with the command: `/addstock <platform>`", parse_mode="Markdown")
        return

    platform = args[0].strip().lower()
    valid_platforms = ["netflix", "crunchyroll", "minecraft", "iptv", "hotmail", "steam", "spotify", "kick", "g2a"]
    
    if platform not in valid_platforms:
        await update.message.reply_text(f"⚠️ **Invalid Platform!** Choose from: {', '.join(valid_platforms)}")
        return

    message = update.message
    document = message.document or (message.reply_to_message and message.reply_to_message.document)

    if not document:
        await update.message.reply_text("⚠️ **Please attach a file (.txt or .zip)** or reply to a file with `/addstock <platform>`")
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
                        
                        if platform != "netflix":
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
            await update.message.reply_text(f"✅ **Success!** Added *{added_lines}* accounts to *{platform.upper()}* stock.", parse_mode="Markdown")

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
            await update.message.reply_text(f"✅ **Success!** Added *{added_lines}* accounts to *{platform.upper()}* stock.", parse_mode="Markdown")
        else:
            os.remove(file_path)
            await update.message.reply_text("❌ **Unsupported format:** Please upload only `.txt` or `.zip` files.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def add_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    args = context.args
    if len(args) < 2:
        await update.message.reply_text("⚠️ **Usage Error!**\nFormat: `/addcode <code> <platform>`", parse_mode="Markdown")
        return

    code = args[0].strip()
    platform = args[1].strip().lower()

    valid_platforms = ["netflix", "crunchyroll", "minecraft", "iptv", "hotmail", "steam", "spotify", "kick", "g2a"]
    if platform not in valid_platforms:
        await update.message.reply_text(f"⚠️ **Invalid Platform!**")
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

        await update.message.reply_text(f"✅ **Success!** Code `{code}` linked to *{platform.upper()}*", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def redeem_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username_str = f"@{user.username}" if user.username else user.first_name
    user_id = user.id

    args = context.args
    if not args:
        await update.message.reply_text("⚠️ **Please provide a code!**\nUsage: `/redeem <code>`", parse_mode="Markdown")
        return

    user_code = args[0].strip()
    
    if not os.path.exists(CODES_FILE):
        await update.message.reply_text("❌ **Vault Error:** No redeem codes available.")
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
            account = fetch_account_by_platform(found_platform)
            if not account:
                await update.message.reply_text(f"⚠️ **Stock Empty** for *{found_platform.upper()}*!", parse_mode="Markdown")
                return

            caption = (
                "🎉 ════════════════════════════ 🎉\n"
                f"   🎁 **REDEEMED: {found_platform.upper()} VIP** 🎁   \n"
                "🎉 ════════════════════════════ 🎉\n\n"
                f"💎 **Plan / Tier:** `{account['plan']}`\n"
                f"🌍 **Region:** `{account['region']}`\n"
                f"📧 **Username / Email:** `{account['email']}`\n"
                f"🔑 **Password / Details:** `{account['password']}`\n\n"
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
                await update.message.reply_text(f"🛡 **SESSION DATA / COOKIE:**\n```{account['data']}```", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ **Invalid or Already Used Code:** Please check your code.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def get_netflix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_netflix()
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🎬 **NETFLIX VIP**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    await update.message.reply_text(f"```{account['data']}```", parse_mode="Markdown")

async def get_crunchyroll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(CRUNCHYROLL_FILE, "Crunchyroll")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🌸 **CRUNCHYROLL VIP**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_minecraft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(MINECRAFT_FILE, "Minecraft")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"⛏️ **MINECRAFT VIP**\n👤 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    if account.get("data"):
        await update.message.reply_text(f"```{account['data']}```", parse_mode="Markdown")

async def get_iptv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(IPTV_FILE, "IPTV")
    if not account:
        account = {"email": "crackhed01", "password": "dca2002a", "plan": "Silver", "region": "http://vpn.silver-iptval.store", "data": "http://vpn.silver-iptval.store/get.php?username=crackhed01&password=dca2002a&type=m3u_plus&output=ts"}
    caption = f"📺 **IPTV STREAM**\n👤 `{account['email']}`\n🔑 `{account['password']}`\n🔗 `{account['data']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_hotmail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(HOTMAIL_FILE, "Hotmail")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"📧 **HOTMAIL VIP**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_steam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(STEAM_FILE, "Steam")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🎮 **STEAM VIP ACCOUNT**\n👤 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID,
$botCode = @'
import os
import re
import random
import zipfile
from colorama import init, Fore, Style
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

# Initialize terminal colors
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

EPIC_GIF_ID = "CgACAgQAAxkBAAID8GrWUp6oFYRL0wXnz84eY-dpMu9uAAItIAACYEq5Unt0oPSbvFyUPQQ"

def is_authorized(update: Update) -> bool:
    user = update.effective_user
    if user and user.username:
        return user.username.lower() == ALLOWED_USERNAME.lower()
    return False

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.animation:
        file_id = update.message.animation.file_id
        await update.message.reply_text(f"✨ **GIF File ID:**\n`{file_id}`", parse_mode="Markdown")

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
        print(f"{Fore.RED}[!] Netflix Error: {e}")
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
        print(f"{Fore.RED}[!] Error reading {platform_name}: {e}")
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
    welcome_text = (
        "✨ ════════════════════════════ ✨\n"
        "🔥 **WELCOME TO THE ULTIMATE VIP VAULT** 🔥\n"
        "✨ ════════════════════════════ ✨\n\n"
        "🛡 **System Status:** `Online & Secured`\n"
        "⚡ **Master Controller:** `@Akk_Taiyou_Asano`\n\n"
        "🎯 **Available Commands:**\n"
        "🎁 `/redeem <CODE>` — Redeem your VIP access code to instantly get a random account from stock!\n\n"
    )

    if is_authorized(update):
        welcome_text += (
            "👑 **Admin Commands (Stock Gen):**\n"
            "🍿 `/netflix`  |  🌸 `/crunchyroll`  |  ⛏️ `/minecraft`\n"
            "📺 `/iptv`     |  📧 `/hotmail`     |  🎮 `/steam`\n"
            "🎧 `/spotify`  |  🟣 `/kick`        |  🛒 `/g2a`\n\n"
            "📥 `/addstock <platform>` — Send a .txt or .zip file with this command to auto-sort & add stock!\n"
            "➕ `/addcode <code> <platform>` — Link a code to stock\n"
            "🔄 `/check` — Clean & validate stock databases\n"
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

# --- أداة الفحص وتطهير الستوك المحلية الآمنة ---
async def check_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    files = {
        "Crunchyroll": CRUNCHYROLL_FILE,
        "Minecraft": MINECRAFT_FILE,
        "Hotmail": HOTMAIL_FILE,
        "IPTV": IPTV_FILE,
        "Steam": STEAM_FILE,
        "Spotify": SPOTIFY_FILE,
        "Kick": KICK_FILE,
        "G2A": G2A_FILE
    }

    report = "🔄 **Stock Cleaning & Check Report:**\n\n"
    total_valid = 0

    for name, path in files.items():
        if not os.path.exists(path):
            continue
        valid_lines = []
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    clean = line.strip()
                    if clean and not clean.startswith("#") and len(clean) > 3:
                        valid_lines.append(clean + "\n")
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(valid_lines)
            total_valid += len(valid_lines)
            report += f"• **{name}:** `{len(valid_lines)}` valid accounts\n"
        except Exception:
            pass

    report += f"\n📊 **Total Active Accounts:** `{total_valid}`"
    await update.message.reply_text(report, parse_mode="Markdown")

async def add_stock_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("⚠️ **Usage Error!**\nSend a `.txt` or `.zip` file with the command: `/addstock <platform>`", parse_mode="Markdown")
        return

    platform = args[0].strip().lower()
    valid_platforms = ["netflix", "crunchyroll", "minecraft", "iptv", "hotmail", "steam", "spotify", "kick", "g2a"]
    
    if platform not in valid_platforms:
        await update.message.reply_text(f"⚠️ **Invalid Platform!** Choose from: {', '.join(valid_platforms)}")
        return

    message = update.message
    document = message.document or (message.reply_to_message and message.reply_to_message.document)

    if not document:
        await update.message.reply_text("⚠️ **Please attach a file (.txt or .zip)** or reply to a file with `/addstock <platform>`")
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
                        
                        if platform != "netflix":
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
            await update.message.reply_text(f"✅ **Success!** Added *{added_lines}* accounts to *{platform.upper()}* stock.", parse_mode="Markdown")

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
            await update.message.reply_text(f"✅ **Success!** Added *{added_lines}* accounts to *{platform.upper()}* stock.", parse_mode="Markdown")
        else:
            os.remove(file_path)
            await update.message.reply_text("❌ **Unsupported format:** Please upload only `.txt` or `.zip` files.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def add_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    args = context.args
    if len(args) < 2:
        await update.message.reply_text("⚠️ **Usage Error!**\nFormat: `/addcode <code> <platform>`", parse_mode="Markdown")
        return

    code = args[0].strip()
    platform = args[1].strip().lower()

    valid_platforms = ["netflix", "crunchyroll", "minecraft", "iptv", "hotmail", "steam", "spotify", "kick", "g2a"]
    if platform not in valid_platforms:
        await update.message.reply_text(f"⚠️ **Invalid Platform!**")
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

        await update.message.reply_text(f"✅ **Success!** Code `{code}` linked to *{platform.upper()}*", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def redeem_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username_str = f"@{user.username}" if user.username else user.first_name
    user_id = user.id

    args = context.args
    if not args:
        await update.message.reply_text("⚠️ **Please provide a code!**\nUsage: `/redeem <code>`", parse_mode="Markdown")
        return

    user_code = args[0].strip()
    
    if not os.path.exists(CODES_FILE):
        await update.message.reply_text("❌ **Vault Error:** No redeem codes available.")
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
            account = fetch_account_by_platform(found_platform)
            if not account:
                await update.message.reply_text(f"⚠️ **Stock Empty** for *{found_platform.upper()}*!", parse_mode="Markdown")
                return

            caption = (
                "🎉 ════════════════════════════ 🎉\n"
                f"   🎁 **REDEEMED: {found_platform.upper()} VIP** 🎁   \n"
                "🎉 ════════════════════════════ 🎉\n\n"
                f"💎 **Plan / Tier:** `{account['plan']}`\n"
                f"🌍 **Region:** `{account['region']}`\n"
                f"📧 **Username / Email:** `{account['email']}`\n"
                f"🔑 **Password / Details:** `{account['password']}`\n\n"
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
                await update.message.reply_text(f"🛡 **SESSION DATA / COOKIE:**\n```{account['data']}```", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ **Invalid or Already Used Code:** Please check your code.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def get_netflix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_netflix()
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🎬 **NETFLIX VIP**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    await update.message.reply_text(f"```{account['data']}```", parse_mode="Markdown")

async def get_crunchyroll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(CRUNCHYROLL_FILE, "Crunchyroll")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🌸 **CRUNCHYROLL VIP**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_minecraft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(MINECRAFT_FILE, "Minecraft")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"⛏️ **MINECRAFT VIP**\n👤 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    if account.get("data"):
        await update.message.reply_text(f"```{account['data']}```", parse_mode="Markdown")

async def get_iptv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(IPTV_FILE, "IPTV")
    if not account:
        account = {"email": "crackhed01", "password": "dca2002a", "plan": "Silver", "region": "http://vpn.silver-iptval.store", "data": "http://vpn.silver-iptval.store/get.php?username=crackhed01&password=dca2002a&type=m3u_plus&output=ts"}
    caption = f"📺 **IPTV STREAM**\n👤 `{account['email']}`\n🔑 `{account['password']}`\n🔗 `{account['data']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_hotmail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(HOTMAIL_FILE, "Hotmail")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"📧 **HOTMAIL VIP**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_steam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(STEAM_FILE, "Steam")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🎮 **STEAM VIP ACCOUNT**\n👤 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID,
$botCode = @'
import os
import re
import random
import zipfile
from colorama import init, Fore, Style
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

# Initialize terminal colors
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

EPIC_GIF_ID = "CgACAgQAAxkBAAID8GrWUp6oFYRL0wXnz84eY-dpMu9uAAItIAACYEq5Unt0oPSbvFyUPQQ"

def is_authorized(update: Update) -> bool:
    user = update.effective_user
    if user and user.username:
        return user.username.lower() == ALLOWED_USERNAME.lower()
    return False

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.animation:
        file_id = update.message.animation.file_id
        await update.message.reply_text(f"✨ **GIF File ID:**\n`{file_id}`", parse_mode="Markdown")

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
        print(f"{Fore.RED}[!] Netflix Error: {e}")
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
        print(f"{Fore.RED}[!] Error reading {platform_name}: {e}")
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
    welcome_text = (
        "✨ ════════════════════════════ ✨\n"
        "🔥 **WELCOME TO THE ULTIMATE VIP VAULT** 🔥\n"
        "✨ ════════════════════════════ ✨\n\n"
        "🛡 **System Status:** `Online & Secured`\n"
        "⚡ **Master Controller:** `@Akk_Taiyou_Asano`\n\n"
        "🎯 **Available Commands:**\n"
        "🎁 `/redeem <CODE>` — Redeem your VIP access code to instantly get a random account from stock!\n\n"
    )

    if is_authorized(update):
        welcome_text += (
            "👑 **Admin Commands (Stock Gen):**\n"
            "🍿 `/netflix`  |  🌸 `/crunchyroll`  |  ⛏️ `/minecraft`\n"
            "📺 `/iptv`     |  📧 `/hotmail`     |  🎮 `/steam`\n"
            "🎧 `/spotify`  |  🟣 `/kick`        |  🛒 `/g2a`\n\n"
            "📥 `/addstock <platform>` — Send a .txt or .zip file with this command to auto-sort & add stock!\n"
            "➕ `/addcode <code> <platform>` — Link a code to stock\n"
            "🔄 `/check` — Clean & validate stock databases\n"
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

# --- أداة الفحص وتطهير الستوك المحلية ---
async def check_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    files = {
        "Crunchyroll": CRUNCHYROLL_FILE,
        "Minecraft": MINECRAFT_FILE,
        "Hotmail": HOTMAIL_FILE,
        "IPTV": IPTV_FILE,
        "Steam": STEAM_FILE,
        "Spotify": SPOTIFY_FILE,
        "Kick": KICK_FILE,
        "G2A": G2A_FILE
    }

    report = "🔄 **Stock Cleaning & Check Report:**\n\n"
    total_valid = 0

    for name, path in files.items():
        if not os.path.exists(path):
            continue
        valid_lines = []
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    clean = line.strip()
                    if clean and not clean.startswith("#") and len(clean) > 3:
                        valid_lines.append(clean + "\n")
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(valid_lines)
            total_valid += len(valid_lines)
            report += f"• **{name}:** `{len(valid_lines)}` valid accounts\n"
        except Exception:
            pass

    report += f"\n📊 **Total Active Accounts:** `{total_valid}`"
    await update.message.reply_text(report, parse_mode="Markdown")

async def add_stock_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("⚠️ **Usage Error!**\nSend a `.txt` or `.zip` file with the command: `/addstock <platform>`", parse_mode="Markdown")
        return

    platform = args[0].strip().lower()
    valid_platforms = ["netflix", "crunchyroll", "minecraft", "iptv", "hotmail", "steam", "spotify", "kick", "g2a"]
    
    if platform not in valid_platforms:
        await update.message.reply_text(f"⚠️ **Invalid Platform!** Choose from: {', '.join(valid_platforms)}")
        return

    message = update.message
    document = message.document or (message.reply_to_message and message.reply_to_message.document)

    if not document:
        await update.message.reply_text("⚠️ **Please attach a file (.txt or .zip)** or reply to a file with `/addstock <platform>`")
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
                        
                        if platform != "netflix":
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
            await update.message.reply_text(f"✅ **Success!** Added *{added_lines}* accounts to *{platform.upper()}* stock.", parse_mode="Markdown")

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
            await update.message.reply_text(f"✅ **Success!** Added *{added_lines}* accounts to *{platform.upper()}* stock.", parse_mode="Markdown")
        else:
            os.remove(file_path)
            await update.message.reply_text("❌ **Unsupported format:** Please upload only `.txt` or `.zip` files.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def add_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    args = context.args
    if len(args) < 2:
        await update.message.reply_text("⚠️ **Usage Error!**\nFormat: `/addcode <code> <platform>`", parse_mode="Markdown")
        return

    code = args[0].strip()
    platform = args[1].strip().lower()

    valid_platforms = ["netflix", "crunchyroll", "minecraft", "iptv", "hotmail", "steam", "spotify", "kick", "g2a"]
    if platform not in valid_platforms:
        await update.message.reply_text(f"⚠️ **Invalid Platform!**")
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

        await update.message.reply_text(f"✅ **Success!** Code `{code}` linked to *{platform.upper()}*", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def redeem_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username_str = f"@{user.username}" if user.username else user.first_name
    user_id = user.id

    args = context.args
    if not args:
        await update.message.reply_text("⚠️ **Please provide a code!**\nUsage: `/redeem <code>`", parse_mode="Markdown")
        return

    user_code = args[0].strip()
    
    if not os.path.exists(CODES_FILE):
        await update.message.reply_text("❌ **Vault Error:** No redeem codes available.")
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
            account = fetch_account_by_platform(found_platform)
            if not account:
                await update.message.reply_text(f"⚠️ **Stock Empty** for *{found_platform.upper()}*!", parse_mode="Markdown")
                return

            caption = (
                "🎉 ════════════════════════════ 🎉\n"
                f"   🎁 **REDEEMED: {found_platform.upper()} VIP** 🎁   \n"
                "🎉 ════════════════════════════ 🎉\n\n"
                f"💎 **Plan / Tier:** `{account['plan']}`\n"
                f"🌍 **Region:** `{account['region']}`\n"
                f"📧 **Username / Email:** `{account['email']}`\n"
                f"🔑 **Password / Details:** `{account['password']}`\n\n"
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
                await update.message.reply_text(f"🛡 **SESSION DATA / COOKIE:**\n```{account['data']}```", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ **Invalid or Already Used Code:** Please check your code.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def get_netflix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_netflix()
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🎬 **NETFLIX VIP**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    await update.message.reply_text(f"```{account['data']}```", parse_mode="Markdown")

async def get_crunchyroll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(CRUNCHYROLL_FILE, "Crunchyroll")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🌸 **CRUNCHYROLL VIP**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_minecraft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(MINECRAFT_FILE, "Minecraft")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"⛏️ **MINECRAFT VIP**\n👤 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    if account.get("data"):
        await update.message.reply_text(f"```{account['data']}```", parse_mode="Markdown")

async def get_iptv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(IPTV_FILE, "IPTV")
    if not account:
        account = {"email": "crackhed01", "password": "dca2002a", "plan": "Silver", "region": "http://vpn.silver-iptval.store", "data": "http://vpn.silver-iptval.store/get.php?username=crackhed01&password=dca2002a&type=m3u_plus&output=ts"}
    caption = f"📺 **IPTV STREAM**\n👤 `{account['email']}`\n🔑 `{account['password']}`\n🔗 `{account['data']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_hotmail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(HOTMAIL_FILE, "Hotmail")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"📧 **HOTMAIL VIP**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_steam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(STEAM_FILE, "Steam")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🎮 **STEAM VIP ACCOUNT**\n👤 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_spotify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(SPOTIFY_FILE, "Spotify")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🎧 **SPOTIFY PREMIUM VIP**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(KICK_FILE, "Kick")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🟣 **KICK VIP ACCOUNT**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_g2a(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(G2A_FILE, "G2A")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🛒 **G2A VIP ACCOUNT / KEY**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "report_broken":
        await query.message.reply_text("🚨 **Report Received:** Account flagged for replacement!")
    elif query.data == "help_redeem":
        await query.message.reply_text("💡 **How to redeem:** Use `/redeem CODE` to get your random account instantly!", parse_mode="Markdown")

def main():
    print("="*65)
    print("    🎁 ULTIMATE G2A & AUTO-STOCK BOT - RUNNING 🎁")
    print("="*65)

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
    
    # أداة الفحص الآمنة
    app.add_handler(CommandHandler("check", check_stock))

    app.add_handler(MessageHandler(filters.ANIMATION, get_file_id))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
