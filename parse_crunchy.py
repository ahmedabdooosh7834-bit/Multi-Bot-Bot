import os
import re

# اسم الملف الذي أرسلته (تأكد أنه في نفس المجلد)
INPUT_FILE = "420X CRUNCHYROLL PREMIUM ACCOUNT.txt"
OUTPUT_FILE = "crunchyroll_accounts.txt"

def parse_accounts():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ الملف {INPUT_FILE} غير موجود! تأكد من وضعه في نفس المجلد.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # تقسيم النص بناءً على الهits أو النماذج الموجودة في الملف
    hits = content.split("🎯 HIT")
    parsed_count = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for hit in hits:
            if not hit.strip():
                continue

            # استخراج البريد وكلمة المرور من Combo
            combo_match = re.search(r"🔓 Combo\s*:\s*(.*?)\s*:\s*(.*?)(?=\n\s*➖➖|\n\s*⭐|$)", hit, re.DOTALL)
            country_match = re.search(r"⭐ Country\s*:\s*(.*?)(?=\n|$)", hit)
            plan_match = re.search(r"👑 Plan\s*:\s*(.*?)(?=\n|$)", hit)
            expiry_match = re.search(r"⏰ Expiry\s*:\s*(.*?)(?=\n|$)", hit)

            if combo_match:
                email = combo_match.group(1).strip()
                password = combo_match.group(2).strip().replace("\n", "")
                
                country = country_match.group(1).strip() if country_match else "Global"
                plan = plan_match.group(1).strip() if plan_match else "Mega Fan"
                expiry = expiry_match.group(1).strip() if expiry_match else "Active"

                # تجاهل القيم الفارغة
                if not email or not password or password == "?":
                    continue

                # التنسيق النهائي: Email | Password | Plan | Country | Expiry
                line = f"{email}|{password}|{plan}|{country}|{expiry}\n"
                out.write(line)
                parsed_count += 1

    print(f"✅ تم بنجاح استخراج وترتيب {parsed_count} حساب في ملف: {OUTPUT_FILE}")

if __name__ == "__main__":
    parse_accounts()