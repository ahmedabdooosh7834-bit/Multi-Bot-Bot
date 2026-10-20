
import os
import zipfile
import shutil
from telegram import Update
from telegram.ext import ContextTypes

async def addstock_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    document = message.document
    
    # البحث عن الملف سواء مرفق مع الرسالة أو رداً عليها
    if not document and message.reply_to_message and message.reply_to_message.document:
        document = message.reply_to_message.document

    if not document:
        await message.reply_text("⚠️ **الرجاء إرفاق ملف الستوك أو الرد على الملف بـ /addstock**", parse_mode="Markdown")
        return

    file_name = document.file_name.lower()
    file = await context.bot.get_file(document.file_id)
    file_path = f"temp_{file_name}"
    await file.download_to_drive(file_path)

    # تحديد ملف الحفظ بناءً على اسم الملف أو الأمر
    target_file = "accounts.txt"
    if "crunchyroll" in file_name:
        target_file = "crunchyroll_accounts.txt"
    elif "netflix" in file_name:
        target_file = "accounts.txt"
    elif "spotify" in file_name:
        target_file = "spotify_accounts.txt"
    elif "steam" in file_name:
        target_file = "steam_accounts.txt"
    elif "minecraft" in file_name:
        target_file = "minecraft_accounts.txt"
    elif "hotmail" in file_name or "mail" in file_name:
        target_file = "hotmail_accounts.txt"
    elif "iptv" in file_name:
        target_file = "iptv_accounts.txt"
    elif "kick" in file_name:
        target_file = "kick_accounts.txt"

    try:
        if file_name.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall("temp_extracted")
            
            total_added = 0
            with open(target_file, 'a', encoding='utf-8') as dest:
                for root, dirs, files in os.walk("temp_extracted"):
                    for f_name in files:
                        if f_name.endswith('.txt'):
                            sub_path = os.path.join(root, f_name)
                            with open(sub_path, 'r', encoding='utf-8', errors='ignore') as src:
                                lines = src.readlines()
                                dest.writelines(lines)
                                total_added += len(lines)
            
            if os.path.exists("temp_extracted"):
                shutil.rmtree("temp_extracted")
                
            await message.reply_text(f"✅ **تم إضافة الستوك بنجاح!**\n📊 تم استخراج وإضافة: {total_added} حساب إلى {target_file}", parse_mode="Markdown")
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                new_lines = f.readlines()

            with open(target_file, 'a', encoding='utf-8') as f:
                f.writelines(new_lines)

            await message.reply_text(f"✅ **تم إضافة الستوك بنجاح!**\n📊 عدد الحسابات: {len(new_lines)}\n📁 الملف: {target_file}", parse_mode="Markdown")

        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        await message.reply_text(f"❌ حدث خطأ أثناء المعالجة: {str(e)}")
        if os.path.exists(file_path):
            os.remove(file_path)
