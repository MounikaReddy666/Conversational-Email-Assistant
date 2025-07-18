# # this code for browser automation while it working upto composing but not sending the email using playwright
# from playwright.async_api import async_playwright
# import os
# import asyncio
# from dotenv import load_dotenv
# from datetime import datetime

# load_dotenv()

# async def send_email_with_playwright(sender_email, app_password, recipient_email, subject, body):
#     screenshots = []
#     max_retries = 3

#     for attempt in range(max_retries):
#         print(f"\n🚀 Attempt {attempt + 1} to send email...")
#         try:
#             async with async_playwright() as p:
#                 browser = await p.chromium.launch_persistent_context(
#                     user_data_dir='C:\\Users\\bogga\\gmail-profile',
#                     headless=False,
#                     slow_mo=100,
#                     args=["--start-maximized"]
#                 )

#                 await asyncio.sleep(2)
#                 pages = browser.pages
#                 page = pages[0] if pages else await browser.new_page()

#                 try:
#                     await page.goto("https://mail.google.com", timeout=120000)
#                     await page.wait_for_load_state("domcontentloaded")
#                     print("✅ Gmail loaded:", page.url)
#                 except Exception as e:
#                     print(f"⚠️ Failed to load Gmail: {e}")
#                     await browser.close()
#                     continue

#                 try:
#                     if "inbox" in page.url:
#                         print("✅ Already logged in. Skipping login.")
#                     else:
#                         print("🔐 Login flow started.")
#                         await page.wait_for_selector('input[type="email"]', timeout=15000)
#                         await page.fill('input[type="email"]', sender_email)
#                         await page.click('button:has-text("Next")')
#                         await page.wait_for_timeout(3000)

#                         await page.wait_for_selector('input[type="password"]', timeout=15000)
#                         await page.fill('input[type="password"]', app_password)
#                         await page.click('button:has-text("Next")')
#                         await page.wait_for_load_state("networkidle", timeout=60000)

#                 except Exception as login_error:
#                     print(f"⚠️ Login error: {login_error}")
#                     screenshot_path = f"login_error_{datetime.now().strftime('%H%M%S')}.png"
#                     await page.screenshot(path=screenshot_path)
#                     print(f"🖼️ Screenshot saved to {screenshot_path}")
#                     await browser.close()
#                     continue

#                 try:
#                     # Click Compose
#                     await page.wait_for_selector('div[gh="cm"]', timeout=30000)
#                     await page.click('div[gh="cm"]')

#                     # Wait for compose dialog
#                     dialog = page.locator('div[role="dialog"]').first
#                     await dialog.wait_for(timeout=30000)

#                     # --- Reliable wait for "To" field ---
#                     to_field = dialog.locator('textarea[name="to"]')
#                     found_to_field = False
#                     for wait in range(10):  # Wait up to ~10 seconds
#                         if await to_field.is_visible():
#                             found_to_field = True
#                             break
#                         await asyncio.sleep(1)

#                     if not found_to_field:
#                         raise Exception("❌ 'To' field not visible after waiting.")

#                     await to_field.fill(recipient_email)

#                     # Subject
#                     subject_field = dialog.locator('input[name="subjectbox"]')
#                     await subject_field.wait_for(timeout=10000)
#                     await subject_field.fill(subject)

#                     # Body
#                     body_field = dialog.locator('div[aria-label="Message Body"]')
#                     await body_field.wait_for(timeout=10000)
#                     await body_field.click()
#                     await body_field.fill(body)

#                     # Send
#                     send_button = dialog.locator('div[aria-label*="Send"]')
#                     await send_button.wait_for(timeout=10000)
#                     await send_button.click()
#                     await page.wait_for_timeout(3000)

#                     print(f"✅ Email sent to {recipient_email}!")
#                     await browser.close()
#                     return screenshots

#                 except Exception as send_error:
#                     print(f"⚠️ Error sending email: {send_error}")
#                     screenshot_path = f"send_error_{datetime.now().strftime('%H%M%S')}.png"
#                     await page.screenshot(path=screenshot_path)
#                     print(f"🖼️ Screenshot saved to {screenshot_path}")
#                     await browser.close()
#                     continue

#         except Exception as e:
#             print(f"❌ Attempt {attempt + 1} failed: {e}")
#             await asyncio.sleep(5)
#             continue

#     print("❌ All attempts failed.")
#     return []

