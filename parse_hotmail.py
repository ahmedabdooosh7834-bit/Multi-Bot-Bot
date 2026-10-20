import os

INPUT_FILE = "613K Hotmail Combolist.txt"
OUTPUT_FILE = "hotmail_accounts.txt"

def parse_hotmail():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ ملف {INPUT_FILE} غير موجود!")
        return

    count = 0
    with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f, \
         open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            
            # تنظيف صيغة البريد وكلمة المرور
            parts = line.split(":")
            if len(parts) >= 2 and "@" in parts[0]:
                email = parts[0].strip()
                password = parts[1].strip()
                out.write(f"{email}|{password}|Hotmail VIP|Active\n")
                count += 1

    print(f"✅ تم ترتيب {count} حساب Hotmail بنجاح في ملف {OUTPUT_FILE}")

if __name__ == "__main__":
    parse_hotmail()