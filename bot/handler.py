#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""پرواز نفرین‌شده — بات خوش‌آمدگویی (اجرا روی GitHub Actions، هر ۵ دقیقه)

برای هر بازیکن تازه، پیام خوش‌آمد با دو دکمه می‌فرستد:
  🎮 شروع بازی      → مینی‌اپ تلگرام (GitHub Pages — بدون نیاز به VPN)
  👥 دعوت از دوستان  → صفحه اشتراک‌گذاری تلگرام با متن آماده

بدون نیاز به دیتابیس: آپدیت‌ها بلافاصله پس از پاسخ‌دادن تأیید (confirm) می‌شوند
و صف تلگرام تا ۲۴ ساعت نگه می‌دارد، پس هیچ خوش‌آمدی از دست نمی‌رود.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

TOKEN = os.environ.get("BOT_TOKEN", "")
API = "https://api.telegram.org/bot" + TOKEN
GAME_URL = "https://prauofi21-svg.github.io/cursed-flight-app/"
FALLBACK_USERNAME = "Midnight_talebot"
INVITE_TEXT = "🦇 بیا «پرواز نفرین‌شده» بازی کنیم — پرواز در آسمون قبرستان! 🌙"

WELCOME = (
    "🦇 به «پرواز نفرین‌شده» خوش اومدی!\n\n"
    "در آسمون قبرستان پرواز کن، از دروازه‌های استخوانی رد شو، "
    "رکورد بزن و کاراکترهای جدید رو باز کن.\n\n"
    "🎮 برای شروع، دکمهٔ زیر رو بزن 👇"
)
INVITE_MSG = "🎁 دوستات رو هم به بازی دعوت کن!\nبا دکمهٔ زیر لینک بازی رو براشون بفرست 🦇"


def call(method, payload=None, timeout=65):
    data = json.dumps(payload or {}).encode("utf-8")
    req = urllib.request.Request(
        API + "/" + method, data=data,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        out = json.loads(r.read().decode("utf-8"))
    if not out.get("ok"):
        raise RuntimeError(method + " -> " + json.dumps(out, ensure_ascii=False)[:300])
    return out["result"]


def build_keyboard(username):
    share = ("https://t.me/share/url?url="
             + urllib.parse.quote("https://t.me/" + username, safe="")
             + "&text=" + urllib.parse.quote(INVITE_TEXT, safe=""))
    return {"inline_keyboard": [
        [{"type": "web_app", "text": "🎮 شروع بازی", "web_app": {"url": GAME_URL}}],
        [{"type": "url", "text": "👥 دعوت از دوستان", "url": share}],
    ]}


def main():
    if not TOKEN:
        print("BOT_TOKEN missing")
        return 1
    me = call("getMe")
    username = me.get("username") or FALLBACK_USERNAME
    keyboard = build_keyboard(username)
    print("running as @" + username, flush=True)

    def fetch(timeout, offset=None):
        params = {"timeout": timeout, "limit": 100, "allowed_updates": ["message"]}
        if offset is not None:
            params["offset"] = offset
        return call("getUpdates", params, timeout=timeout + 15)

    def send(chat_id, text):
        call("sendMessage", {
            "chat_id": chat_id, "text": text,
            "reply_markup": keyboard, "disable_web_page_preview": True})

    once = "--once" in sys.argv          # حالت یک‌بارِ دستی (تست/اجرای محلی)
    deadline = time.time() + (5 if once else 270)  # حالت چرخه‌ای: ~۴.۵ دقیقه polling
    offset = None
    welcomed = 0

    while time.time() < deadline:
        try:
            updates = fetch(0 if once else 50, offset)
        except Exception as e:
            print("poll error:", e, flush=True)
            if once:
                return 1
            time.sleep(5)
            continue

        if not updates:
            if once:
                break
            continue  # long-poll تمام شد → ادامه تا پایان مهلت

        # فقط آخرین پیام هر چت پاسخ داده می‌شود (ضد اسپم برای چندبار Start زدن)
        last_per_chat = {}
        max_id = 0
        for u in updates:
            max_id = max(max_id, u.get("update_id") or 0)
            msg = u.get("message") or {}
            chat = msg.get("chat") or {}
            if chat.get("type") == "private":
                last_per_chat[chat["id"]] = msg

        for msg in last_per_chat.values():
            text = (msg.get("text") or "").strip()
            try:
                send(msg["chat"]["id"], INVITE_MSG if text.startswith("/invite") else WELCOME)
                welcomed += 1
                print("welcomed chat", msg["chat"]["id"], flush=True)
            except Exception as e:
                print("send error:", e, flush=True)

        offset = max_id + 1
        try:
            fetch(0, offset)  # تأیید آپدیت‌های پردازش‌شده
        except Exception as e:
            print("confirm error:", e, flush=True)

        if once:
            break

    print("done; welcomed chats:", welcomed, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
