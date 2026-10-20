import os
import re
import zipfile

ZIP_FILE = "x302_Minecraft_COOKIES.zip"
OUTPUT_FILE = "minecraft_accounts.txt"

def parse_minecraft_zip():
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
                
                # استخراج البيانات بدقة من اسم الملف
                minecoins = re.search(r'\[(.*?) minecoins\]', filename)
                networth = re.search(r'\[(.*?) networth\]', filename)
                capes = re.search(r'\[(.*?) capes\]', filename)
                
                coins_val = minecoins.group(1) if minecoins else "0"
                net_val = networth.group(1) if networth else "0"
                capes_val = capes.group(1) if capes else "1"

                # استخراج اسم المستخدم الحقيقي
                username_match = re.search(r'\]\s+\[(.*?)\]\s+@AXLE_exe', filename)
                username = username_match.group(1) if username_match else "Minecraft_VIP"

                try:
                    with archive.open(file_info) as f:
                        cookie_content = f.read().decode('utf-8', errors='ignore').strip()
                        cookie_data = " ".join(cookie_content.splitlines()).replace("|", " ")

                        if not cookie_data:
                            continue

                        # ترتيب الحقول بفاصل دقيق وآمن
                        line_to_write = f"{username}|Minecoins: {coins_val} (Capes: {capes_val})|Global|Active|{cookie_data}\n"
                        out.write(line_to_write)
                        parsed_count += 1
                except Exception:
                    continue

    print(f"✅ تم إعادة ترتيب {parsed_count} حساب ماينكرافت بنجاح!")

if __name__ == "__main__":
    parse_minecraft_zip()