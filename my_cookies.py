import os
import re
import zipfile

# اسم ملف الـ ZIP أو مساره
ZIP_FILE = "x4015_Netflix_COOKIES.zip"
OUTPUT_FILE = "accounts.txt"

def extract_and_format():
    if not os.path.exists(ZIP_FILE):
        print(f"الملف {ZIP_FILE} غير موجود في المجلد الحالي!")
        return

    accounts_count = 0
    with zipfile.ZipFile(ZIP_FILE, 'r') as archive:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
            for file_info in archive.infolist():
                # تجاهل المجلدات والملفات غير النصية
                if file_info.is_dir() or not file_info.filename.endswith('.txt'):
                    continue

                filename = os.path.basename(file_info.filename)
                
                # استخراج البيانات من اسم الملف: [Plan] [payments] [extra] [Region] [Email]
                tags = re.findall(r'\[(.*?)\]', filename)
                
                if len(tags) >= 5:
                    plan = tags[0].strip() if tags[0].strip() else "Premium"
                    region = tags[3].strip()
                    email = tags[4].strip()
                elif len(tags) >= 1:
                    plan = tags[0].strip()
                    region = "Global"
                    email = "Netflix User"
                else:
                    plan = "Premium VIP"
                    region = "Global"
                    email = filename.replace(".txt", "")

                # قراءة محتوى الكوكي من داخل الملف المضغوط
                try:
                    with archive.open(file_info) as f:
                        cookie_content = f.read().decode('utf-8', errors='ignore').strip()
                        
                        # إزالة النزول لسطر جديد حتى لا يخرب تنسيق السطر في accounts.txt
                        clean_cookie = cookie_content.replace("\r", "").replace("\n", " ")

                        if not clean_cookie:
                            continue

                        password = "N/A (Cookie Login)"
                        screens = "4 Screens (4K UHD)"
                        expiry = "Active"

                        # كتابة السطر بالتنسيق المطلوب للبوت
                        line = f"{email}|{password}|{plan}|{screens}|{region}|{expiry}|{clean_cookie}\n"
                        out.write(line)
                        accounts_count += 1
                except Exception as e:
                    continue

    print(f"تم بنجاح استخراج وترتيب {accounts_count} حساب داخل {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_and_format()