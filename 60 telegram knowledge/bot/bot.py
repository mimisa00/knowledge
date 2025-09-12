import os
import re
import logging
import json
import ipaddress
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler, CommandHandler, MessageHandler, Filters
from datetime import datetime
import requests

# Logging
logging.basicConfig(
    filename='/app/fw.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global state per user
user_states = {}

# File path to coms list
COMS_FILE = 'coms.txt'

# Environment variables

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = os.getenv("API_URL")
API_AUTH = os.getenv("API_AUTH")

chat_ids_env = os.getenv("ALLOWED_CHAT_IDS", "")
ALLOWED_CHAT_IDS = [int(chat_id.strip()) for chat_id in chat_ids_env.split(",") if chat_id.strip()]
user_ids_env = os.getenv("ALLOWED_USERS", "")
ALLOWED_USERS = [int(user_id.strip()) for user_id in user_ids_env.split(",") if user_id.strip()]

def is_valid_ipv4(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

# --- UI Panels ---
def main_panel():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ 新增白名單", callback_data='allow'),
            InlineKeyboardButton("➖ 關閉白名單", callback_data='deny')
        ],
        [
            InlineKeyboardButton("✖ 關閉主選單", callback_data='close'),
            InlineKeyboardButton("📃 說明", callback_data='help')
        ]
    ])

def back_panel():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✖", callback_data='close'),
            InlineKeyboardButton("🔙", callback_data='back')
        ]
    ])

def com_panel(user_id):
    buttons = []
    try:
        with open(COMS_FILE) as f:
            for line in f:
                com = line.strip()
                display_text = f"\u200F\u3000{com}"
                buttons.append([InlineKeyboardButton(display_text, callback_data=f"com|{com}")])
    except Exception as e:
        logger.error(f"讀取 com 列表失敗: {e}")
        context.bot.edit_message_text(
            chat_id=state['chat_id'],
            message_id=state['message_id'],
            text="❌ 無法讀取域名列表，請稍後再試。",
            reply_markup=back_panel()
        )
        return
    buttons.insert(0, [
        InlineKeyboardButton("✖", callback_data='close'),
        InlineKeyboardButton("🔙", callback_data='back')
    ])
    return InlineKeyboardMarkup(buttons)

def is_authorized(user_id: int, chat_id: int) -> bool:
    return user_id in ALLOWED_USERS or chat_id in ALLOWED_CHAT_IDS

# --- Command Handlers ---
def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    if is_authorized(user_id, chat_id):
        update.message.reply_text("選擇操作：", reply_markup=main_panel())
    else:
        update.message.reply_text("未授權操作...")

# --- Callback Query Handler ---
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    data = query.data
    chat_id = query.message.chat_id
    msg_id = query.message.message_id

    if data in ['allow', 'deny']:
        user_states[user_id] = {
            'step': 'awaiting_ip',
            'action': data,
            'chat_id': chat_id,
            'message_id': msg_id
        }
        query.edit_message_text(
            f"{'📝新增' if data == 'allow' else '📝關閉'}白名單\n輸入 IP ...例：192.168.1.123",
            reply_markup=back_panel()
        )
    elif data == 'help':
        query.edit_message_text(
            "說明：\n"
            "1. 新增白名單：\n"
                        "　　　Step1：於輸入框輸入 IP \n"
                        "　　　Step2：於輸入框輸入 IP 說明 \n"
                        "　　　Step3：點選控制面版上的 公司代碼\n"
                        "　　　Step4：請等待 bot 回應... \n"
                        "　　　Step5：控制面版回應處理結果 \n"
                        "　　　Step6：控制面版回到主選單 \n"
            "2. 關閉白名單：與新增相同\n"
            "3. 關閉主選單：關閉控制面版\n"
            "4. 其它說明：可透過 /start 開啟多個控制面版，但是只有一個會生效，操作時請維持一個控制面版",
            reply_markup=back_panel()
        )
    elif data == 'close':
        user_states[user_id] = {
            'step': '',
            'action': '',
            'chat_id': '',
            'message_id': ''
        }
        query.edit_message_text("主選單已關閉。")
    elif data == 'back':
        state = user_states.get(user_id)
        if not state:
            user_states[user_id] = {
                'step': '',
                'action': '',
                'chat_id': '',
                'message_id': ''
            }
            query.edit_message_text("請選擇操作：", reply_markup=main_panel())
            return
        action_text = "新增白名單" if state.get("action") == "allow" else "關閉白名單"
        if state['step'] == 'awaiting_desc':
            state['step'] = 'awaiting_ip'
            context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=f"📝 {action_text}\n輸入 IP (例如：192.168.1.1)",
                reply_markup=back_panel()
            )
        elif state['step'] == 'domain_select':
            state['step'] = 'awaiting_desc'
            context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=f"📝 {action_text}\n輸入 IP 說明（例如：辦公室 VPN）",
                reply_markup=back_panel()
            )
        else:
            user_states[user_id] = {
                'step': '',
                'action': '',
                'chat_id': '',
                'message_id': ''
            }
            context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text="請選擇操作：",
                reply_markup=main_panel()
            )
    elif data.startswith('com|'):
        _, com = data.split('|')
        state = user_states.get(user_id, {})
        source_ip = state.get('ip')
        desc = state.get('desc')
        operator = query.from_user.full_name
        action = state.get('action')
        chat_id = state.get('chat_id')
        msg_id = state.get('message_id')
        action_text = "新增白名單" if state.get("action") == "allow" else "關閉白名單"

        payload = {
            "acl":action,
            "code":com,
            "iplist":[source_ip]
        }
        url = f"{API_URL}/"
        headers = {
            "Authorization": API_AUTH,
            "Content-Type": "application/json"
        }
        #logger.info(json.dumps(payload))
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=f"✅ {action_text}成功\n IP : {source_ip}\n公司 : {com}\n說明 : {desc}\n操作人員 : {operator}",
                reply_markup=main_panel()
            )
            log_line = f"acl:{action} user:{operator} ip:{source_ip} desc:{desc} com:{com}"
            logger.info(log_line)
        else:
            log_line = f"acl:{action} user:{operator} ip:{source_ip} desc:{desc} com:{com}ErrMsg:{response.text}"
            context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=f"❌ 操作失敗：{log_line}"
            )
            logger.error(log_line)
        user_states.pop(user_id, None)

# --- Message Handler ---
def message_handler(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    text = update.message.text
    state = user_states.get(user_id)

    if not state:
        return

    chat_id = state['chat_id']
    msg_id = state['message_id']
    action = state.get("action")
    action_text = "新增白名單" if action == "allow" else "關閉白名單"

    if state['step'] == 'awaiting_ip':
        if not is_valid_ipv4(text):
            context.bot.edit_message_text(
                chat_id=state['chat_id'],
                message_id=state['message_id'],
                text=f"⚠️ {action_text}\n需輸入有效 IP (例如：192.168.1.1)",
                reply_markup=back_panel()
            )
            return

        state['ip'] = text.strip()
        state['step'] = 'awaiting_desc'
        context.bot.edit_message_text(
            chat_id=state['chat_id'],
            message_id=state['message_id'],
            text=f"📝 {action_text}\n輸入 IP 說明（例如：辦公室 VPN）",
            reply_markup=back_panel()
        )
    elif state['step'] == 'awaiting_desc':
        if not text:
            context.bot.edit_message_text(
                chat_id=state['chat_id'],
                message_id=state['message_id'],
                text=f"⚠️ {action_text}\n需輸入 IP 說明（例如：辦公室 VPN）",
                reply_markup=back_panel()
            )
            return

        state['desc'] = text.strip()
        state['step'] = 'domain_select'

        # 產生 domain 按鈕
        context.bot.edit_message_text(
            chat_id=state['chat_id'],
            message_id=state['message_id'],
            text=f"📝 {action_text}\n選擇白名單對應公司",
            reply_markup=com_panel(user_id)
        )

# --- Main ---
def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
