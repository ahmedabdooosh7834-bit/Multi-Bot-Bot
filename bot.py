import os
import zipfile
import shutil
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚡ **Welcome to the Stock Management Bot!**\n\n"
        "• To add stock: Upload a file and reply to it with /addstock\n"
        "• To check and clean stock: Use /check",
        parse_mode="Markdown"
    )

async def addstock_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    document = message.document
    
    if not document and message.reply_to_message and message.reply_to_message.document:
        document = message.reply_to_message.document

    if not document:
        await message.reply_text("⚠️ **Please attach a stock file or reply to a file with /addstock!**", parse_mode="Markdown")
        return

    file_name = document.file_name.lower()
    file = await context.bot.get_file(document.file_id)
    file_path = f"temp_{file_name}"
    await file.download_to_drive(file_path)

    target_file = "crunchyroll_accounts.txt" if "crunchyroll" in file_name else "accounts.txt"

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
                
            await message.reply_text(f"✅ **Stock extracted and added successfully!**\n📊 Total added: {total_added} accounts to {target_file}", parse_mode="Markdown")
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                new_lines = f.readlines()

            with open(target_file, 'a', encoding='utf-8') as f:
                f.writelines(new_lines)

            await message.reply_text(f"✅ **Stock added successfully!**\n📊 Accounts added: {len(new_lines)}\n📁 File: {target_file}", parse_mode="Markdown")

        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        await message.reply_text(f"❌ An error occurred during processing: {str(e)}")
        if os.path.exists(file_path):
            os.remove(file_path)

async def check_accounts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    await message.reply_text("🔄 **Checking stored accounts and cleaning invalid ones... Please wait.**", parse_mode="Markdown")

    target_file = "crunchyroll_accounts.txt"
    if not os.path.exists(target_file):
        await message.reply_text("⚠️ Sorry, no stock file is currently stored for checking.")
        return

    valid_accounts = []
    invalid_count = 0

    try:
        with open(target_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if ":" in line and len(line.split(":")) >= 2:
                valid_accounts.append(line + "\n")
            else:
                invalid_count += 1

        with open(target_file, 'w', encoding='utf-8') as f:
            f.writelines(valid_accounts)

        await message.reply_text(
            f"✨ **Check completed successfully!**\n\n"
            f"🟢 **Valid accounts:** {len(valid_accounts)}\n"
            f"🔴 **Removed invalid accounts:** {invalid_count}",
            parse_mode="Markdown"
        )
    except Exception as e:
        await message.reply_text(f"❌ An error occurred during checking: {str(e)}")

def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN is not set!")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addstock", addstock_handler))
    app.add_handler(CommandHandler("check", check_accounts_command))

    print("Bot is up and running...")
    app.run_polling()

if __name__ == '__main__':
    main()
