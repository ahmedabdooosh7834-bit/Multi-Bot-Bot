import os
import zipfile

ZIP_FILE = "x1658_Kick_COOKIES.zip"
OUTPUT_FILE = "kick_accounts.txt"

def parse_kick():
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
                
                # استخراج اسم المستخدم من اسم الملف مثل [0taror0]
                import re
                user_match = re.search(r'\[(.*?)\]\s+@AXLE_exe', filename)
                username = user_match.group(1) if user_match else "Kick_VIP"
                fake_email = f"{username}@kick.com"
                password = "🔐 Secure Cookie Login"

                try:
                    with archive.open(file_info) as f:
                        cookie_content = f.read().decode('utf-8', errors='ignore').strip()
                        cookie_data = " ".join(cookie_content.splitlines()).replace("|", " ")

                        if not cookie_data:
                            continue

                        line_to_write = f"{fake_email}|{password}|Kick VIP|Global|{cookie_data}\n"
                        out.write(line_to_write)
                        parsed_count += 1
                except Exception:
                    continue

    print(f"✅ تم ترتيب {parsed_count} حساب Kick بنجاح في ملف {OUTPUT_FILE}")

if __name__ == "__main__":
    parse_kick()