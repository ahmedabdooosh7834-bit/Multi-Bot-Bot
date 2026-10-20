import os
import re
import random
import zipfile
import paramiko
from colorama import init, Fore, Style
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

init(autoreset=True)

TOKEN = "7946580929:AAFQoVnSU7JxOMx_Gu0ClRwcd7bO3nUDK5I"
ALLOWED_USERNAME = "Akk_Taiyou_Asano"

VPS_HOST = "149.129.255.179"
VPS_PORT = 22
VPS_USER = "adminDJ"
VPS_PASS = "Gajebo108"

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

def get_random_netflix_cookie():
    if not os.path.exists(NETFLIX_ZIP):
        return None, None
    try:
        with zipfile.ZipFile(NETFLIX_ZIP, 'r') as archive:
            file_list = [f for f in archive.infolist() if not f.is_dir() and f.filename.endswith('.txt')]
            if not file_list:
                return None, None
            selected_file = random.choice(file_list)
            filename = os.path.basename(selected_file.filename)
            
            with archive.open(selected_file) as f:
                cookie_content = f.read().decode('utf-8', errors='ignore').strip()
            return cookie_content, filename
    except Exception as e:
        print(f"{Fore.RED}[!] Netflix Cookie Error: {e}")
        return None, None

def get_random_text_account(file_path, platform_name):
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
        if not lines:
            return None
        
        selected_line = random.choice(lines)
        
        # التعرف الذكي إذا كان السطر عبارة عن كوكيز/بيانات مباشرة بدون فاصل |
        if "|" not in selected_line:
            login_urls = {
                "Spotify": "[https://accounts.spotify.com/en/login](https://accounts.spotify.com/en/login)",
                "Crunchyroll": "[https://www.crunchyroll.com/login](https://www.crunchyroll.com/login)",
                "Minecraft": "[https://www.minecraft.net/en-us/login](https://www.minecraft.net/en-us/login)",
                "Hotmail": "[https://outlook.live.com](https://outlook.live.com)",
                "IPTV": "[http://vpn.silver-iptval.store](http://vpn.silver-iptval.store)",
                "Steam": "[https://store.steampowered.com/login/](https://store.steampowered.com/login/)",
                "Kick": "[https://kick.com/](https://kick.com/)",
                "G2A": "[https://www.g2a.com/](https://www.g2a.com/)"
            }
            return {
                "platform": platform_name,
                "email": f"{platform_name} Cookie / Session",
                "password": "🔐 Secure Session Data",
                "plan": "VIP Premium",
                "region": "Global",
                "data": selected_line,
                "login": login_urls.get(platform_name, "[https://www.g2a.com/](https://www.g2a.com/)")
            }

        parts = selected_line.split("|")
        email = parts[0].strip() if len(parts) > 0 else "user@vip.com"
        password = parts[1].strip() if len(parts) > 1 else "N/A"
        plan = parts[2].strip() if len(parts) > 2 else "VIP Access"
        region = parts[3].strip() if len(parts) > 3 else "Global"
        data = parts[4].strip() if len(parts) > 4 else ""

        login_urls = {
            "Crunchyroll": "[https://www.crunchyroll.com/login](https://www.crunchyroll.com/login)",
            "Minecraft": "[https://www.minecraft.net/en-us/login](https://www.minecraft.net/en-us/login)",
            "Hotmail": "[https://outlook.live.com](https://outlook.live.com)",
            "IPTV": "[http://vpn.silver-iptval.store](http://vpn.silver-iptval.store)",
            "Steam": "[https://store.steampowered.com/login/](https://store.steampowered.com/login/)",
            "Spotify": "[https://accounts.spotify.com/en/login](https://accounts.spotify.com/en/login)",
            "Kick": "[https://kick.com/](https://kick.com/)",
            "G2A": "[https://www.g2a.com/](https://www.g2a.com/)"
        }

        return {
            "platform": platform_name,
            "email": email,
            "password": password,
            "plan": plan,
            "region": region,
            "data": data,
            "login": login_urls.get(platform_name, "[https://www.g2a.com/](https://www.g2a.com/)")
        }
    except Exception as e:
        print(f"{Fore.RED}[!] Error reading {platform_name}: {e}")
        return None

def fetch_account_by_platform(platform_name):
    p = platform_name.lower()
    if "net" in p:
        cookie, name = get_random_netflix_cookie()
        return {"platform": "Netflix", "email": name, "password": "Cookie Session", "plan": "Premium UHD", "region": "Global", "data": cookie, "login": "[https://www.netflix.com/login](https://www.netflix.com/login)"}
    else:
        file_path = os.path.join(BASE_DIR, f"{p}_accounts.txt")
        if os.path.exists(file_path):
            return get_random_text_account(file_path, p.capitalize())
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "✨ ════════════════════════════ ✨\n"
        "🔥 **WELCOME TO THE ULTIMATE VIP VAULT** 🔥\n"
        "✨ ════════════════════════════ ✨\n\n"
        "🛡 **System Status:** `Online & Secured`\n"
        "⚡ **Master Controller:** `@Akk_Taiyou_Asano`\n\n"
        "🎯 **Available Commands:**\n"
        "🎁 `/redeem <CODE>` — Redeem your VIP access code!\n"
        "📺 `/tv <TV_CODE>` — Auto-activate Netflix on your Smart TV via Root VPS!\n\n"
    )

    if is_authorized(update):
        welcome_text += (
            "👑 **Admin Commands:**\n"
            "🍿 `/netflix`  |  🌸 `/crunchyroll`  |  ⛏️ `/minecraft`\n"
            "📺 `/iptv`     |  📧 `/hotmail`     |  🎮 `/steam`\n"
            "🎧 `/spotify`  |  🟣 `/kick`        |  🛒 `/g2a`\n\n"
            "➕ `/addserviece <name>` — Create a new service\n"
            "📥 `/addstock <platform>` — Add stock files\n"
            "➕ `/addcode <code> <platform>` — Link a code\n"
            "🔄 `/check` — Clean & validate stock databases\n"
        )
    
    welcome_text += "✨ ════════════════════════════ ✨"

    keyboard = [
        [InlineKeyboardButton("🎁 How to Redeem", callback_data="help_redeem")],
        [InlineKeyboardButton("💎 Bot Channel / Support", url="[https://t.me/Akk_M_Bot](https://t.me/Akk_M_Bot)")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_animation(
        animation=EPIC_GIF_ID,
        caption=welcome_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def activate_tv_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("⚠️ **Usage Error!**\nأرسل كود التلفزيون مع الأمر:\nمثال: `/tv ABC1234`", parse_mode="Markdown")
        return

    tv_code = args[0].strip().upper()
    status_msg = await update.message.reply_text("🔄 **جاري الاتصال بالـ VPS وتجهيز المتصفح وتفعيل الشاشة... ⏳**", parse_mode="Markdown")

    cookie_content, cookie_name = get_random_netflix_cookie()
    if not cookie_content:
        await status_msg.edit_text("⚠️ **عذراً، لا يوجد كوكيز نتفليكس مخزن في الستوك حالياً!**")
        return

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(VPS_HOST, port=VPS_PORT, username=VPS_USER, password=VPS_PASS, timeout=15)

        sftp = ssh.open_sftp()

        runner_code = '''import sys
import asyncio
from playwright.async_api import async_playwright

async def activate(tv_code, cookie_file_path):
    browser = None
    try:
        with open(cookie_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            cookie_content = f.read()

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("[https://www.netflix.com/login](https://www.netflix.com/login)", timeout=60000)

            cookies_list = []
            for line in cookie_content.splitlines():
                if line.strip() and not line.startswith('#'):
                    parts = line.split('\\t')
                    if len(parts) >= 7:
                        cookies_list.append({
                            'name': parts[5],
                            'value': parts[6],
                            'domain': parts[0],
                            'path': parts[2],
                            'secure': parts[3].upper() == 'TRUE',
                            'httpOnly': False
                        })
            
            if cookies_list:
                await context.add_cookies(cookies_list)

            await page.goto("[https://www.netflix.com/tv2](https://www.netflix.com/tv2)", timeout=60000)
            await page.wait_for_timeout(3000)

            input_locator = page.locator("input[name='code'], input#field-code, input.ui-text-input")
            await input_locator.first.fill(tv_code)
            
            submit_btn = page.locator("button[type='submit'], button.submit-button, button:has-text('Activate'), button:has-text('متابعة')")
            await submit_btn.first.click()
            await page.wait_for_timeout(4000)

            confirm_btn = page.locator("button:has-text('Confirm'), button:has-text('تأكيد'), button.nf-btn-primary")
            if await confirm_btn.count() > 0:
                await confirm_btn.first.click()
                await page.wait_for_timeout(3000)

            await page.screenshot(path="screenshot.png", full_page=True)
            await browser.close()
            print("SUCCESS")
    except Exception as e:
        try:
            if 'page' in locals():
                await page.screenshot(path="screenshot.png", full_page=True)
            if browser:
                await browser.close()
        except:
            pass
        print(f"ERROR: {e}")

if __name__ == "__main__":
    code = sys.argv[1]
    c_file = sys.argv[2]
    asyncio.run(activate(code, c_file))
'''
        with sftp.file('tv_runner.py', 'w') as f:
            f.write(runner_code)

        with sftp.file('/tmp/temp_cookie.txt', 'w') as f:
            f.write(cookie_content)
        sftp.close()

        ssh.exec_command('pip3 install playwright && playwright install chromium --with-deps', get_pty=True)

        stdin, stdout, stderr = ssh.exec_command(f'python3 tv_runner.py {tv_code} /tmp/temp_cookie.txt', get_pty=True, timeout=90)
        output = stdout.read().decode()
        error = stderr.read().decode()

        local_screenshot = os.path.join(BASE_DIR, "vps_screenshot.png")
        try:
            sftp = ssh.open_sftp()
            sftp.get('screenshot.png', local_screenshot)
            sftp.close()
        except Exception as ex:
            print(f"Screenshot download warning: {ex}")

        ssh.exec_command('rm -f /tmp/temp_cookie.txt screenshot.png')
        ssh.close()

        if "SUCCESS" in output:
            caption = (
                f"✨ **تم تفعيل شاشة التلفزيون عبر الـ VPS بنجاح!**\n\n"
                f"📺 **الكود المفعل:** `{tv_code}`\n"
                f"🍪 **الملف المستخدم:** `{cookie_name}`\n\n"
                f"✅ **تحقق من شاشة التلفزيون الآن!** 🎉"
            )
        else:
            caption = f"❌ **نتيجة التفعيل (مع وجود ملاحظة/خطأ):**\n`{output or error}`"

        await status_msg.delete()

        if os.path.exists(local_screenshot):
            with open(local_screenshot, 'rb') as photo_file:
                await update.message.reply_photo(photo=photo_file, caption=caption, parse_mode="Markdown")
            os.remove(local_screenshot)
        else:
            await update.message.reply_text(caption, parse_mode="Markdown")

    except Exception as e:
        await status_msg.edit_text(f"❌ **خطأ في الاتصال بالـ VPS:**\n`{str(e)}`", parse_mode="Markdown")

async def add_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("⚠️ **Usage Error!**\nFormat: `/addserviece <service_name>`", parse_mode="Markdown")
        return

    service_name = args[0].strip().lower()
    file_path = os.path.join(BASE_DIR, f"{service_name}_accounts.txt")

    if os.path.exists(file_path):
        await update.message.reply_text(f"⚠️ Service `{service_name}` already exists!")
        return

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# Accounts database for {service_name}\n")

        context.application.add_handler(CommandHandler(service_name, get_dynamic_service))

        await update.message.reply_text(
            f"✅ **Success!** Service `{service_name}` created successfully.\n"
            f"• Command `/{service_name}` is now active.\n"
            f"• Use `/addstock {service_name}` to upload accounts.",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def get_dynamic_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    command = update.message.text.lstrip('/').lower().split()[0]
    file_path = os.path.join(BASE_DIR, f"{command}_accounts.txt")
    account = get_random_text_account(file_path, command.capitalize())
    if not account:
        await update.message.reply_text(f"⚠️ **Stock Empty** for {command.capitalize()}")
        return
    caption = f"🛒 **{command.upper()} VIP ACCOUNT**\n👤 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    if account.get("data") and len(str(account["data"])) > 5:
        await update.message.reply_text(f"🛡 **SESSION DATA / COOKIE:**\n```{account['data']}```", parse_mode="Markdown")

async def check_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    report = "🔄 **Stock Cleaning & Check Report:**\n\n"
    total_valid = 0

    if os.path.exists(NETFLIX_ZIP):
        try:
            with zipfile.ZipFile(NETFLIX_ZIP, 'r') as arch:
                nf_count = len([f for f in arch.infolist() if not f.is_dir() and f.filename.endswith('.txt')])
                total_valid += nf_count
                report += f"• **Netflix (ZIP):** `{nf_count}` cookie files\n"
        except:
            pass

    for filename in os.listdir(BASE_DIR):
        if filename.endswith("_accounts.txt"):
            path = os.path.join(BASE_DIR, filename)
            name = filename.replace("_accounts.txt", "").capitalize()
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

    report += f"\n📊 **Total Active Items:** `{total_valid}`"
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

        if "net" in platform and file_name.endswith('.zip'):
            if file_path != NETFLIX_ZIP:
                if os.path.exists(NETFLIX_ZIP):
                    os.remove(NETFLIX_ZIP)
                with open(file_path, 'rb') as src, open(NETFLIX_ZIP, 'wb') as dst:
                    dst.write(src.read())
                os.remove(file_path)
            await update.message.reply_text("✅ **Success!** Netflix cookies ZIP saved successfully as `x4015_Netflix_COOKIES.zip`.", parse_mode="Markdown")
            return

        target_file = os.path.join(BASE_DIR, f"{platform}_accounts.txt")
        added_lines = 0

        if file_name.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as archive:
                for z_info in archive.infolist():
                    if z_info.is_dir() or not z_info.filename.endswith('.txt'):
                        continue
                    with archive.open(z_info) as z_f:
                        content = z_f.read().decode('utf-8', errors='ignore')
                        lines = content.splitlines()
                        
                        with open(target_file, "a", encoding="utf-8") as out:
                            for line in lines:
                                clean_line = line.strip()
                                if clean_line and not clean_line.startswith("#"):
                                    if "|" not in clean_line:
                                        out.write(clean_line + "\n")
                                    else:
                                        out.write(clean_line + "\n")
                                    added_lines += 1
            os.remove(file_path)
            await update.message.reply_text(f"✅ **Success!** Added *{added_lines}* items to *{platform.upper()}* stock.", parse_mode="Markdown")

        elif file_name.endswith('.txt'):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as src:
                lines = src.readlines()
            
            with open(target_file, "a", encoding="utf-8") as out:
                for line in lines:
                    clean_line = line.strip()
                    if clean_line and not clean_line.startswith("#"):
                        out.write(clean_line + "\n")
                        added_lines += 1
            os.remove(file_path)
            await update.message.reply_text(f"✅ **Success!** Added *{added_lines}* items to *{platform.upper()}* stock.", parse_mode="Markdown")
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

    try:
        if os.path.exists(CODES_FILE):
            with open(CODES_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith(code + "|"):
                        await update.message.










































$botCode = @'
import os
import re
import random
import zipfile
import paramiko
from colorama import init, Fore, Style
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

init(autoreset=True)

TOKEN = "7946580929:AAFQoVnSU7JxOMx_Gu0ClRwcd7bO3nUDK5I"
ALLOWED_USERNAME = "Akk_Taiyou_Asano"

VPS_HOST = "149.129.255.179"
VPS_PORT = 22
VPS_USER = "adminDJ"
VPS_PASS = "Gajebo108"

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

def get_random_netflix_cookie():
    if not os.path.exists(NETFLIX_ZIP):
        return None, None
    try:
        with zipfile.ZipFile(NETFLIX_ZIP, 'r') as archive:
            file_list = [f for f in archive.infolist() if not f.is_dir() and f.filename.endswith('.txt')]
            if not file_list:
                return None, None
            selected_file = random.choice(file_list)
            filename = os.path.basename(selected_file.filename)
            
            with archive.open(selected_file) as f:
                cookie_content = f.read().decode('utf-8', errors='ignore').strip()
            return cookie_content, filename
    except Exception as e:
        print(f"{Fore.RED}[!] Netflix Cookie Error: {e}")
        return None, None

def get_random_text_account(file_path, platform_name):
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
        if not lines:
            return None
        
        selected_line = random.choice(lines)
        
        # التعرف الذكي إذا كان السطر عبارة عن كوكيز/بيانات مباشرة بدون فاصل |
        if "|" not in selected_line:
            login_urls = {
                "Spotify": "[https://accounts.spotify.com/en/login](https://accounts.spotify.com/en/login)",
                "Crunchyroll": "[https://www.crunchyroll.com/login](https://www.crunchyroll.com/login)",
                "Minecraft": "[https://www.minecraft.net/en-us/login](https://www.minecraft.net/en-us/login)",
                "Hotmail": "[https://outlook.live.com](https://outlook.live.com)",
                "IPTV": "[http://vpn.silver-iptval.store](http://vpn.silver-iptval.store)",
                "Steam": "[https://store.steampowered.com/login/](https://store.steampowered.com/login/)",
                "Kick": "[https://kick.com/](https://kick.com/)",
                "G2A": "[https://www.g2a.com/](https://www.g2a.com/)"
            }
            return {
                "platform": platform_name,
                "email": f"{platform_name} Cookie / Session",
                "password": "🔐 Secure Session Data",
                "plan": "VIP Premium",
                "region": "Global",
                "data": selected_line,
                "login": login_urls.get(platform_name, "[https://www.g2a.com/](https://www.g2a.com/)")
            }

        parts = selected_line.split("|")
        email = parts[0].strip() if len(parts) > 0 else "user@vip.com"
        password = parts[1].strip() if len(parts) > 1 else "N/A"
        plan = parts[2].strip() if len(parts) > 2 else "VIP Access"
        region = parts[3].strip() if len(parts) > 3 else "Global"
        data = parts[4].strip() if len(parts) > 4 else ""

        login_urls = {
            "Crunchyroll": "[https://www.crunchyroll.com/login](https://www.crunchyroll.com/login)",
            "Minecraft": "[https://www.minecraft.net/en-us/login](https://www.minecraft.net/en-us/login)",
            "Hotmail": "[https://outlook.live.com](https://outlook.live.com)",
            "IPTV": "[http://vpn.silver-iptval.store](http://vpn.silver-iptval.store)",
            "Steam": "[https://store.steampowered.com/login/](https://store.steampowered.com/login/)",
            "Spotify": "[https://accounts.spotify.com/en/login](https://accounts.spotify.com/en/login)",
            "Kick": "[https://kick.com/](https://kick.com/)",
            "G2A": "[https://www.g2a.com/](https://www.g2a.com/)"
        }

        return {
            "platform": platform_name,
            "email": email,
            "password": password,
            "plan": plan,
            "region": region,
            "data": data,
            "login": login_urls.get(platform_name, "[https://www.g2a.com/](https://www.g2a.com/)")
        }
    except Exception as e:
        print(f"{Fore.RED}[!] Error reading {platform_name}: {e}")
        return None

def fetch_account_by_platform(platform_name):
    p = platform_name.lower()
    if "net" in p:
        cookie, name = get_random_netflix_cookie()
        return {"platform": "Netflix", "email": name, "password": "Cookie Session", "plan": "Premium UHD", "region": "Global", "data": cookie, "login": "[https://www.netflix.com/login](https://www.netflix.com/login)"}
    else:
        file_path = os.path.join(BASE_DIR, f"{p}_accounts.txt")
        if os.path.exists(file_path):
            return get_random_text_account(file_path, p.capitalize())
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "✨ ════════════════════════════ ✨\n"
        "🔥 **WELCOME TO THE ULTIMATE VIP VAULT** 🔥\n"
        "✨ ════════════════════════════ ✨\n\n"
        "🛡 **System Status:** `Online & Secured`\n"
        "⚡ **Master Controller:** `@Akk_Taiyou_Asano`\n\n"
        "🎯 **Available Commands:**\n"
        "🎁 `/redeem <CODE>` — Redeem your VIP access code!\n"
        "📺 `/tv <TV_CODE>` — Auto-activate Netflix on your Smart TV via Root VPS!\n\n"
    )

    if is_authorized(update):
        welcome_text += (
            "👑 **Admin Commands:**\n"
            "🍿 `/netflix`  |  🌸 `/crunchyroll`  |  ⛏️ `/minecraft`\n"
            "📺 `/iptv`     |  📧 `/hotmail`     |  🎮 `/steam`\n"
            "🎧 `/spotify`  |  🟣 `/kick`        |  🛒 `/g2a`\n\n"
            "➕ `/addserviece <name>` — Create a new service\n"
            "📥 `/addstock <platform>` — Add stock files\n"
            "➕ `/addcode <code> <platform>` — Link a code\n"
            "🔄 `/check` — Clean & validate stock databases\n"
        )
    
    welcome_text += "✨ ════════════════════════════ ✨"

    keyboard = [
        [InlineKeyboardButton("🎁 How to Redeem", callback_data="help_redeem")],
        [InlineKeyboardButton("💎 Bot Channel / Support", url="[https://t.me/Akk_M_Bot](https://t.me/Akk_M_Bot)")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_animation(
        animation=EPIC_GIF_ID,
        caption=welcome_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def activate_tv_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("⚠️ **Usage Error!**\nأرسل كود التلفزيون مع الأمر:\nمثال: `/tv ABC1234`", parse_mode="Markdown")
        return

    tv_code = args[0].strip().upper()
    status_msg = await update.message.reply_text("🔄 **جاري الاتصال بالـ VPS وتجهيز المتصفح وتفعيل الشاشة... ⏳**", parse_mode="Markdown")

    cookie_content, cookie_name = get_random_netflix_cookie()
    if not cookie_content:
        await status_msg.edit_text("⚠️ **عذراً، لا يوجد كوكيز نتفليكس مخزن في الستوك حالياً!**")
        return

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(VPS_HOST, port=VPS_PORT, username=VPS_USER, password=VPS_PASS, timeout=15)

        sftp = ssh.open_sftp()

        runner_code = '''import sys
import asyncio
from playwright.async_api import async_playwright

async def activate(tv_code, cookie_file_path):
    browser = None
    try:
        with open(cookie_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            cookie_content = f.read()

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("[https://www.netflix.com/login](https://www.netflix.com/login)", timeout=60000)

            cookies_list = []
            for line in cookie_content.splitlines():
                if line.strip() and not line.startswith('#'):
                    parts = line.split('\\t')
                    if len(parts) >= 7:
                        cookies_list.append({
                            'name': parts[5],
                            'value': parts[6],
                            'domain': parts[0],
                            'path': parts[2],
                            'secure': parts[3].upper() == 'TRUE',
                            'httpOnly': False
                        })
            
            if cookies_list:
                await context.add_cookies(cookies_list)

            await page.goto("[https://www.netflix.com/tv2](https://www.netflix.com/tv2)", timeout=60000)
            await page.wait_for_timeout(3000)

            input_locator = page.locator("input[name='code'], input#field-code, input.ui-text-input")
            await input_locator.first.fill(tv_code)
            
            submit_btn = page.locator("button[type='submit'], button.submit-button, button:has-text('Activate'), button:has-text('متابعة')")
            await submit_btn.first.click()
            await page.wait_for_timeout(4000)

            confirm_btn = page.locator("button:has-text('Confirm'), button:has-text('تأكيد'), button.nf-btn-primary")
            if await confirm_btn.count() > 0:
                await confirm_btn.first.click()
                await page.wait_for_timeout(3000)

            await page.screenshot(path="screenshot.png", full_page=True)
            await browser.close()
            print("SUCCESS")
    except Exception as e:
        try:
            if 'page' in locals():
                await page.screenshot(path="screenshot.png", full_page=True)
            if browser:
                await browser.close()
        except:
            pass
        print(f"ERROR: {e}")

if __name__ == "__main__":
    code = sys.argv[1]
    c_file = sys.argv[2]
    asyncio.run(activate(code, c_file))
'''
        with sftp.file('tv_runner.py', 'w') as f:
            f.write(runner_code)

        with sftp.file('/tmp/temp_cookie.txt', 'w') as f:
            f.write(cookie_content)
        sftp.close()

        ssh.exec_command('pip3 install playwright && playwright install chromium --with-deps', get_pty=True)

        stdin, stdout, stderr = ssh.exec_command(f'python3 tv_runner.py {tv_code} /tmp/temp_cookie.txt', get_pty=True, timeout=90)
        output = stdout.read().decode()
        error = stderr.read().decode()

        local_screenshot = os.path.join(BASE_DIR, "vps_screenshot.png")
        try:
            sftp = ssh.open_sftp()
            sftp.get('screenshot.png', local_screenshot)
            sftp.close()
        except Exception as ex:
            print(f"Screenshot download warning: {ex}")

        ssh.exec_command('rm -f /tmp/temp_cookie.txt screenshot.png')
        ssh.close()

        if "SUCCESS" in output:
            caption = (
                f"✨ **تم تفعيل شاشة التلفزيون عبر الـ VPS بنجاح!**\n\n"
                f"📺 **الكود المفعل:** `{tv_code}`\n"
                f"🍪 **الملف المستخدم:** `{cookie_name}`\n\n"
                f"✅ **تحقق من شاشة التلفزيون الآن!** 🎉"
            )
        else:
            caption = f"❌ **نتيجة التفعيل (مع وجود ملاحظة/خطأ):**\n`{output or error}`"

        await status_msg.delete()

        if os.path.exists(local_screenshot):
            with open(local_screenshot, 'rb') as photo_file:
                await update.message.reply_photo(photo=photo_file, caption=caption, parse_mode="Markdown")
            os.remove(local_screenshot)
        else:
            await update.message.reply_text(caption, parse_mode="Markdown")

    except Exception as e:
        await status_msg.edit_text(f"❌ **خطأ في الاتصال بالـ VPS:**\n`{str(e)}`", parse_mode="Markdown")

async def add_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("⚠️ **Usage Error!**\nFormat: `/addserviece <service_name>`", parse_mode="Markdown")
        return

    service_name = args[0].strip().lower()
    file_path = os.path.join(BASE_DIR, f"{service_name}_accounts.txt")

    if os.path.exists(file_path):
        await update.message.reply_text(f"⚠️ Service `{service_name}` already exists!")
        return

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# Accounts database for {service_name}\n")

        context.application.add_handler(CommandHandler(service_name, get_dynamic_service))

        await update.message.reply_text(
            f"✅ **Success!** Service `{service_name}` created successfully.\n"
            f"• Command `/{service_name}` is now active.\n"
            f"• Use `/addstock {service_name}` to upload accounts.",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def get_dynamic_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    command = update.message.text.lstrip('/').lower().split()[0]
    file_path = os.path.join(BASE_DIR, f"{command}_accounts.txt")
    account = get_random_text_account(file_path, command.capitalize())
    if not account:
        await update.message.reply_text(f"⚠️ **Stock Empty** for {command.capitalize()}")
        return
    caption = f"🛒 **{command.upper()} VIP ACCOUNT**\n👤 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    if account.get("data") and len(str(account["data"])) > 5:
        await update.message.reply_text(f"🛡 **SESSION DATA / COOKIE:**\n```{account['data']}```", parse_mode="Markdown")

async def check_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ **Access Denied:** Master privilege required.")
        return

    report = "🔄 **Stock Cleaning & Check Report:**\n\n"
    total_valid = 0

    if os.path.exists(NETFLIX_ZIP):
        try:
            with zipfile.ZipFile(NETFLIX_ZIP, 'r') as arch:
                nf_count = len([f for f in arch.infolist() if not f.is_dir() and f.filename.endswith('.txt')])
                total_valid += nf_count
                report += f"• **Netflix (ZIP):** `{nf_count}` cookie files\n"
        except:
            pass

    for filename in os.listdir(BASE_DIR):
        if filename.endswith("_accounts.txt"):
            path = os.path.join(BASE_DIR, filename)
            name = filename.replace("_accounts.txt", "").capitalize()
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

    report += f"\n📊 **Total Active Items:** `{total_valid}`"
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

        if "net" in platform and file_name.endswith('.zip'):
            if file_path != NETFLIX_ZIP:
                if os.path.exists(NETFLIX_ZIP):
                    os.remove(NETFLIX_ZIP)
                with open(file_path, 'rb') as src, open(NETFLIX_ZIP, 'wb') as dst:
                    dst.write(src.read())
                os.remove(file_path)
            await update.message.reply_text("✅ **Success!** Netflix cookies ZIP saved successfully as `x4015_Netflix_COOKIES.zip`.", parse_mode="Markdown")
            return

        target_file = os.path.join(BASE_DIR, f"{platform}_accounts.txt")
        added_lines = 0

        if file_name.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as archive:
                for z_info in archive.infolist():
                    if z_info.is_dir() or not z_info.filename.endswith('.txt'):
                        continue
                    with archive.open(z_info) as z_f:
                        content = z_f.read().decode('utf-8', errors='ignore')
                        lines = content.splitlines()
                        
                        with open(target_file, "a", encoding="utf-8") as out:
                            for line in lines:
                                clean_line = line.strip()
                                if clean_line and not clean_line.startswith("#"):
                                    if "|" not in clean_line:
                                        out.write(clean_line + "\n")
                                    else:
                                        out.write(clean_line + "\n")
                                    added_lines += 1
            os.remove(file_path)
            await update.message.reply_text(f"✅ **Success!** Added *{added_lines}* items to *{platform.upper()}* stock.", parse_mode="Markdown")

        elif file_name.endswith('.txt'):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as src:
                lines = src.readlines()
            
            with open(target_file, "a", encoding="utf-8") as out:
                for line in lines:
                    clean_line = line.strip()
                    if clean_line and not clean_line.startswith("#"):
                        out.write(clean_line + "\n")
                        added_lines += 1
            os.remove(file_path)
            await update.message.reply_text(f"✅ **Success!** Added *{added_lines}* items to *{platform.upper()}* stock.", parse_mode="Markdown")
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

            if account.get("data") and len(str(account["data"])) > 5:
                await update.message.reply_text(f"🛡 **SESSION DATA / COOKIE:**\n```{account['data']}```", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ **Invalid or Already Used Code:** Please check your code.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def get_netflix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    cookie, name = get_random_netflix_cookie()
    if not cookie:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🎬 **NETFLIX COOKIE VIP**\n🍪 File: `{name}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    await update.message.reply_text(f"🛡 **COOKIE DATA:**\n```{cookie}```", parse_mode="Markdown")

async def get_crunchyroll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(CRUNCHYROLL_FILE, "Crunchyroll")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🌸 **CRUNCHYROLL VIP**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    if account.get("data") and len(str(account["data"])) > 5:
        await update.message.reply_text(f"🛡 **SESSION DATA / COOKIE:**\n```{account['data']}```", parse_mode="Markdown")

async def get_minecraft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(MINECRAFT_FILE, "Minecraft")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"⛏️ **MINECRAFT VIP**\n👤 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    if account.get("data") and len(str(account["data"])) > 5:
        await update.message.reply_text(f"🛡 **SESSION DATA / COOKIE:**\n```{account['data']}```", parse_mode="Markdown")

async def get_iptv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(IPTV_FILE, "IPTV")
    if not account:
        account = {"email": "crackhed01", "password": "dca2002a", "plan": "Silver", "region": "[http://vpn.silver-iptval.store](http://vpn.silver-iptval.store)", "data": "[http://vpn.silver-iptval.store/get.php?username=crackhed01&password=dca2002a&type=m3u_plus&output=ts](http://vpn.silver-iptval.store/get.php?username=crackhed01&password=dca2002a&type=m3u_plus&output=ts)"}
    caption = f"📺 **IPTV STREAM**\n👤 `{account['email']}`\n🔑 `{account['password']}`\n🔗 `{account['data']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    if account.get("data") and len(str(account["data"])) > 5:
        await update.message.reply_text(f"🛡 **SESSION DATA / COOKIE:**\n```{account['data']}```", parse_mode="Markdown")

async def get_hotmail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(HOTMAIL_FILE, "Hotmail")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"📧 **HOTMAIL VIP**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    if account.get("data") and len(str(account["data"])) > 5:
        await update.message.reply_text(f"🛡 **SESSION DATA / COOKIE:**\n```{account['data']}```", parse_mode="Markdown")

async def get_steam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(STEAM_FILE, "Steam")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🎮 **STEAM VIP ACCOUNT**\n👤 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    if account.get("data") and len(str(account["data"])) > 5:
        await update.message.reply_text(f"🛡 **SESSION DATA / COOKIE:**\n```{account['data']}```", parse_mode="Markdown")

async def get_spotify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(SPOTIFY_FILE, "Spotify")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🎧 **SPOTIFY PREMIUM VIP**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    if account.get("data") and len(str(account["data"])) > 5:
        await update.message.reply_text(f"🛡 **SESSION DATA / COOKIE:**\n```{account['data']}```", parse_mode="Markdown")

async def get_kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(KICK_FILE, "Kick")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🟣 **KICK VIP ACCOUNT**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    if account.get("data") and len(str(account["data"])) > 5:
        await update.message.reply_text(f"🛡 **SESSION DATA / COOKIE:**\n```{account['data']}```", parse_mode="Markdown")

async def get_g2a(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    account = get_random_text_account(G2A_FILE, "G2A")
    if not account:
        await update.message.reply_text("⚠️ **Stock Empty**")
        return
    caption = f"🛒 **G2A VIP ACCOUNT / KEY**\n📧 `{account['email']}`\n🔑 `{account['password']}`"
    keyboard = [[InlineKeyboardButton("⚠️ Account Not Work", callback_data="report_broken")]]
    await update.message.reply_animation(animation=EPIC_GIF_ID, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    if account.get("data") and len(str(account["data"])) > 5:
        await update.message.reply_text(f"🛡 **SESSION DATA / COOKIE:**\n```{account['data']}```", parse_mode="Markdown")

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
    
    app.add_handler(CommandHandler("tv", activate_tv_code))
    app.add_handler(CommandHandler("addserviece", add_service))
    app.add_handler(CommandHandler("addstock", add_stock_file))
    app.add_handler(CommandHandler("addcode", add_code))
    app.add_handler(CommandHandler("redeem", redeem_code))
    app.add_handler(CommandHandler("reedem", redeem_code))
    app.add_handler(CommandHandler("check", check_stock))

    for filename in os.listdir(BASE_DIR):
        if filename.endswith("_accounts.txt"):
            serv_name = filename.replace("_accounts.txt", "").lower()
            if serv_name not in ["crunchyroll", "minecraft", "hotmail", "iptv", "steam", "spotify", "kick", "g2a"]:
                app.add_handler(CommandHandler(serv_name, get_dynamic_service))

    app.add_handler(MessageHandler(filters.ANIMATION, get_file_id))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
