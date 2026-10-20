import sys
import asyncio
from playwright.async_api import async_playwright

async def activate(tv_code, cookie_content):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://www.netflix.com/login", timeout=60000)

            cookies_list = []
            for line in cookie_content.splitlines():
                if line.strip() and not line.startswith('#'):
                    parts = line.split('\t')
                    if len(parts) >= 7:
                        cookies_list.append({
                            'name': parts[5],
                            'value': parts[6],
                            'domain': parts[0],
                            'path': parts[2],
                            'secure': parts[3].upper() == 'TRUE',
                            'httpOnly': False
                        })
            
            if cookies_list:
                await context.add_cookies(cookies_list)

            await page.goto("https://www.netflix.com/tv2", timeout=60000)
            await page.wait_for_timeout(3000)

            input_locator = page.locator("input[name='code'], input#field-code, input.ui-text-input")
            await input_locator.first.fill(tv_code)
            
            submit_btn = page.locator("button[type='submit'], button.submit-button, button:has-text('Activate'), button:has-text('متابعة')")
            await submit_btn.first.click()
            await page.wait_for_timeout(4000)

            confirm_btn = page.locator("button:has-text('Confirm'), button:has-text('تأكيد'), button.nf-btn-primary")
            if await confirm_btn.count() > 0:
                await confirm_btn.first.click()
                await page.wait_for_timeout(3000)

            await browser.close()
            print("SUCCESS")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    code = sys.argv[1]
    cookie = sys.argv[2]
    asyncio.run(activate(code, cookie))