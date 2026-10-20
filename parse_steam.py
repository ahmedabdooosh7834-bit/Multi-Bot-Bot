import os
import zipfile
import re

ZIP_FILE = "x3787_Steam_COOKIES.zip"
OUTPUT_FILE = "steam_accounts.txt"

def parse_steam():
    if not os.path.exists(ZIP_FILE):
        print(f"❌ ملف الأرشيف {ZIP_FILE} غير موجود!")
        return

    parsed_count = 0
    with zipfile.ZipFile(ZIP_FILE, 'r') as archive:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
            for file_info in archive.infolist():
                if file_info.is_dir() or not file_info.filename.endswith('.txt'):
                    continue

                filename = os.path.basename(file_info.filename)
                
                # استخراج Steam ID من اسم الملف
                id_match = re.search(r'\[(7656\d+)\]', filename)
                steam_id = id_match.group(1) if id_match else "Steam_User"
                fake_email = f"{steam_id}@steamuser.com"

                try:
                    with archive.open(file_info) as f:
                        content = f.read().decode('utf-8', errors='ignore').strip()
                        cookie_data = " ".join(content.splitlines()).replace("|", " ")

                        if not cookie_data:
                            continue

                        line_to_write = f"{fake_email}|🔐 Steam Session Guard|Level VIP|Global|{cookie_data}\n"
                        out.write(line_to_write)
                        parsed_count += 1
                except Exception:
                    continue

    print(f"✅ تم ترتيب {parsed_count} حساب Steam بنجاح في ملف {OUTPUT_FILE}")

if __name__ == "__main__":
    parse_steam()