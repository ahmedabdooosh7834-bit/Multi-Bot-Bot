import os
import re

# اسم ملف الـ IPTV الذي أرسلته
INPUT_FILE = "⭐IPTV⭐Premium IPTV With 100K.txt"
OUTPUT_FILE = "iptv_accounts.txt"

def parse_iptv():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ ملف {INPUT_FILE} غير موجود!")
        return

    with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # تقسيم البيانات بناءً على الفواصل أو تكرار كلمة Playlist Name
    blocks = content.split("Playlist Name:")
    parsed_count = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for block in blocks:
            if not block.strip():
                continue

            # استخراج بيانات الحساب باستخدام التعبيرات المنتظمة (Regex)
            playlist_match = re.search(r'[:\s]*(.*?)(?=\nUsername:|$)', block, re.DOTALL)
            username_match = re.search(r'Username:\s*(.*)', block)
            password_match = re.search(r'Password:\s*(.*)', block)
            url_match = re.search(r'Url:\s*(.*)', block)
            m3u_match = re.search(r'M3U:\s*(.*)', block)

            if username_match and password_match and url_match:
                name = playlist_match.group(1).strip() if playlist_match else "Silver IPTV"
                username = username_match.group(1).strip()
                password = password_match.group(1).strip()
                url = url_match.group(1).strip()
                m3u = m3u_match.group(1).strip() if m3u_match else f"{url}/get.php?username={username}&password={password}&type=m3u_plus&output=ts"

                # تنظيف النصوص من الفراغات الزائدة
                name = re.sub(r'[^\w\s]', '', name).strip()

                # التنسيق النهائي المخزن في الملف المرتب: Name | Username | Password | URL | M3U
                line_to_write = f"{name}|{username}|{password}|{url}|{m3u}\n"
                out.write(line_to_write)
                parsed_count += 1

    print(f"✅ تم بنجاح ترتيب {parsed_count} اشتراك IPTV في ملف: {OUTPUT_FILE}")

if __name__ == "__main__":
    parse_iptv()