import os
import zipfile
import re

ZIP_FILE = "x246_Spotify_COOKIES.zip"
OUTPUT_FILE = "spotify_accounts.txt"

def parse_spotify():
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
                
                # استخراج الإيميل ونوع الخطة من اسم الملف أو المسار
                email_match = re.search(r'\[(.*?)@(.*?)\.(.*?)\]', filename)
                # استخراج الإيميل الحقيقي إن وجد أو استخدامه من محتوى الملف
                try:
                    with archive.open(file_info) as f:
                        content = f.read().decode('utf-8', errors='ignore').strip()
                        # البحث عن إيميل داخل محتوى ملف الكوكي
                        email_search = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', content)
                        email = email_search.group(0) if email_search else "spotify_vip@premium.com"
                        
                        cookie_data = " ".join(content.splitlines()).replace("|", " ")
                        if not cookie_data:
                            continue

                        line_to_write = f"{email}|🔐 Spotify Premium Cookie|Family/Duo|Global|{cookie_data}\n"
                        out.write(line_to_write)
                        parsed_count += 1
                except Exception:
                    continue

    print(f"✅ تم ترتيب {parsed_count} حساب Spotify بنجاح في ملف {OUTPUT_FILE}")

if __name__ == "__main__":
    parse_spotify()