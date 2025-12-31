import os
import time
import uuid
import shutil
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
chat_ids_env = os.getenv("ALLOWED_CHAT_IDS", "")
ALLOWED_CHAT_IDS = [int(chat_id.strip()) for chat_id in chat_ids_env.split(",") if chat_id.strip()]
user_ids_env = os.getenv("ALLOWED_USERS", "")
ALLOWED_USERS = [int(user_id.strip()) for user_id in user_ids_env.split(",") if user_id.strip()]

# 路徑設定
BASE_DIR = "/opt/mt-script"
QUEUE_DIR = os.path.join(BASE_DIR, "queue")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
HISTORY_DIR = os.path.join(BASE_DIR,  "history")
HOST_LIST_PATH = os.path.join(BASE_DIR, "host_list.txt")

# 確保歷史目錄存在
os.makedirs(HISTORY_DIR, exist_ok=True)

# 各動作的逾時設定（秒）
ACTION_TIMEOUT = {
    'maint_on': 60,
    'maint_off': 60,
    'restart': 600,
}


def get_timeout(action):
    return ACTION_TIMEOUT.get(action, 60)


def load_hosts():
    with open(HOST_LIST_PATH, 'r') as f:
        hosts = [line.strip() for line in f if line.strip()]

    groups = {}
    all_proxies = []
    all_aps = []

    for host in hosts:
        parts = host.rsplit('-', 1)
        if len(parts) == 2 and parts[1] in ['proxy', 'ap']:
            group_name = parts[0]
        else:
            group_name = host

        if group_name not in groups:
            groups[group_name] = {'proxy': None, 'ap': None}

        if host.endswith('-proxy'):
            groups[group_name]['proxy'] = host
            all_proxies.append(host)
        elif host.endswith('-ap'):
            groups[group_name]['ap'] = host
            all_aps.append(host)

    return groups, all_proxies, all_aps


def build_main_panel(status_message=""):
    groups, all_proxies, all_aps = load_hosts()

    keyboard = []

    keyboard.append([
        InlineKeyboardButton("📋 請選擇操作主機與功能", callback_data="none")
    ])

    keyboard.append([
        InlineKeyboardButton("❌ 關閉選單", callback_data="close")
    ])

    keyboard.append([
        InlineKeyboardButton("⏬ 全部進入維護", callback_data="all|maint_on"),
        InlineKeyboardButton("🔄 全部重啟服務", callback_data="all|restart"),
        InlineKeyboardButton("⏫ 全部結束維護", callback_data="all|maint_off"),
    ])

    keyboard.append([
        InlineKeyboardButton("─────── 個別操作 ───────", callback_data="none")
    ])

    for group_name, hosts in groups.items():
        row = []

        if hosts['proxy']:
            row.append(InlineKeyboardButton("▶️ 進入維護", callback_data=hosts['proxy'] + "|maint_on"))
        else:
            row.append(InlineKeyboardButton(" ", callback_data="none"))

        if hosts['ap']:
            row.append(InlineKeyboardButton("🔄 重啟服務", callback_data=hosts['ap'] + "|restart"))
        else:
            row.append(InlineKeyboardButton(" ", callback_data="none"))

        if hosts['proxy']:
            row.append(InlineKeyboardButton("⏹ 結束維護", callback_data=hosts['proxy'] + "|maint_off"))
        else:
            row.append(InlineKeyboardButton(" ", callback_data="none"))

        row.append(InlineKeyboardButton("🖥 " + group_name, callback_data="none"))

        keyboard.append(row)

    message_text = "🤖 <b>主機維護控制面板</b>\n"
    message_text += "━" * 25 + "\n"

    if status_message:
        message_text += "\n" + status_message + "\n"
        message_text += "━" * 25 + "\n"

    message_text += "\n💡 <i>點擊對應按鈕執行操作</i>"

    return message_text, InlineKeyboardMarkup(keyboard)


def is_authorized(user_id: int, chat_id: int) -> bool:
    return user_id in ALLOWED_USERS or chat_id in ALLOWED_CHAT_IDS

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    if is_authorized(user_id, chat_id):
        message_text, reply_markup = build_main_panel()
        update.message.reply_html(message_text, reply_markup=reply_markup)
    else:
        update.message.reply_text("未授權操作...")


def execute_task(host, action):
    unique_id = uuid.uuid4().hex[:8]
    timestamp = int(time.time())

    # 檔案名稱格式: {}_{}_{}{}.task
    # 例如: server1-proxy_maint_on_1735123456a1b2c3d4.task
    task_id = host + "_" + action + "_" + str(timestamp) + unique_id
    file_path = os.path.join(QUEUE_DIR, task_id + ".task")

    with open(file_path, 'w') as f:
        f.write("HOST=" + host + "\nACTION=" + action)

    return task_id


def archive_result(task_id):
    """將完成的結果檔案移動到歷史目錄"""
    result_path = os.path.join(RESULTS_DIR, task_id + ".result")
    if os.path.exists(result_path):
        # 建立以日期為名的子目錄
        date_str = time.strftime("%Y%m%d")
        date_dir = os.path.join(HISTORY_DIR, date_str)
        os.makedirs(date_dir, exist_ok=True)
        
        # 移動檔案到歷史目錄
        dest_path = os.path.join(date_dir, task_id + ".result")
        try:
            shutil.move(result_path, dest_path)
        except Exception as e:
            # 如果移動失敗，嘗試刪除原檔案
            try:
                os.remove(result_path)
            except:
                pass


def archive_results(task_ids):
    """批次將完成的結果檔案移動到歷史目錄"""
    for task_id in task_ids:
        archive_result(task_id)


def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query

    if query.data == "none":
        query.answer("此按鈕僅供顯示", show_alert=False)
        return

    if query.data == "close":
        query.answer("選單已關閉")
        query.delete_message()
        return

    query.answer()

    target, action = query.data.split('|')

    action_names = {
        'maint_on': '進入維護',
        'maint_off': '結束維護',
        'restart': '重啟服務'
    }
    action_display = action_names.get(action, action)

    if target == "all":
        handle_batch_operation(query, action, action_display)
    else:
        handle_single_operation(query, target, action, action_display)


def handle_single_operation(query, host, action, action_display):
    timeout = get_timeout(action)

    status = "⏳ <b>執行中...</b>\n📍 主機: <code>" + host + "</code>\n🔧 動作: " + action_display
    message_text, reply_markup = build_main_panel(status)
    query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='HTML')

    task_id = execute_task(host, action)
    result_path = os.path.join(RESULTS_DIR, task_id + ".result")

    check_interval = 0.5
    elapsed = 0
    success = False
    result = ""

    while elapsed < timeout:
        if os.path.exists(result_path):
            with open(result_path, 'r') as f:
                success = True
                result = f.read().strip()
            break

        time.sleep(check_interval)
        elapsed += check_interval

    if success:
        status = "✅ <b>執行完成!</b>\n📍 主機: <code>" + host + "</code>\n🔧 動作: " + action_display + "\n📄 結果: " + result + "\n⏱ 耗時: " + str(round(elapsed, 1)) + " 秒"
    else:
        status = "⚠️ <b>執行逾時!</b>\n📍 主機: <code>" + host + "</code>\n🔧 動作: " + action_display + "\n⏱ 已等待: " + str(timeout) + " 秒\n❗ 請檢查該主機 Worker 狀態"

    message_text, reply_markup = build_main_panel(status)
    query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='HTML')

    # 歸檔結果檔案
    archive_result(task_id)


def handle_batch_operation(query, action, action_display):
    groups, all_proxies, all_aps = load_hosts()
    timeout = get_timeout(action)

    if action == 'restart':
        target_hosts = all_aps
    else:
        target_hosts = all_proxies

    total = len(target_hosts)

    if total == 0:
        status = "⚠️ <b>無可操作主機</b>\n🔧 動作: " + action_display
        message_text, reply_markup = build_main_panel(status)
        query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='HTML')
        return

    status = "⏳ <b>派送任務中...</b>\n🔧 動作: " + action_display + " 全部\n📊 派送: 0/" + str(total)
    message_text, reply_markup = build_main_panel(status)
    query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='HTML')

    tasks = []
    for host in target_hosts:
        task_id = execute_task(host, action)
        tasks.append({'host': host, 'task_id': task_id})

    status = "⏳ <b>等待執行結果...</b>\n🔧 動作: " + action_display + " 全部\n📊 已派送: " + str(total) + "/" + str(total)
    message_text, reply_markup = build_main_panel(status)
    query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='HTML')

    results = {}
    for task in tasks:
        results[task['task_id']] = {'host': task['host'], 'success': None, 'result': None}

    pending_tasks = set(task['task_id'] for task in tasks)

    check_interval = 0.5
    elapsed = 0
    last_update = 0

    while pending_tasks and elapsed < timeout:
        completed = []
        for task_id in pending_tasks:
            result_path = os.path.join(RESULTS_DIR, task_id + ".result")
            if os.path.exists(result_path):
                with open(result_path, 'r') as f:
                    results[task_id]['success'] = True
                    results[task_id]['result'] = f.read().strip()
                completed.append(task_id)

        for task_id in completed:
            pending_tasks.remove(task_id)

        if not pending_tasks:
            break

        if elapsed - last_update >= 2:
            done_count = total - len(pending_tasks)
            status = "⏳ <b>等待執行結果...</b>\n🔧 動作: " + action_display + " 全部\n📊 完成: " + str(done_count) + "/" + str(total) + "\n⏱ 已等待: " + str(int(elapsed)) + " 秒"
            message_text, reply_markup = build_main_panel(status)
            try:
                query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='HTML')
            except:
                pass
            last_update = elapsed

        time.sleep(check_interval)
        elapsed += check_interval

    for task_id in pending_tasks:
        results[task_id]['success'] = False
        results[task_id]['result'] = '執行逾時'

    success_count = 0
    fail_count = 0
    result_lines = []

    for task in tasks:
        task_id = task['task_id']
        host = results[task_id]['host']
        success = results[task_id]['success']
        result = results[task_id]['result']

        if success:
            success_count += 1
            result_lines.append("✅ " + host + ": " + result)
        else:
            fail_count += 1
            result_lines.append("❌ " + host + ": " + result)

    result_summary = "\n".join(result_lines)

    if fail_count == 0:
        status = "✅ <b>批次執行完成!</b>\n🔧 動作: " + action_display + " 全部\n📊 成功: " + str(success_count) + "/" + str(total) + "\n⏱ 耗時: " + str(round(elapsed, 1)) + " 秒\n\n<b>詳細結果:</b>\n" + result_summary
    else:
        status = "⚠️ <b>批次執行完成 (部分失敗)</b>\n🔧 動作: " + action_display + " 全部\n📊 成功: " + str(success_count) + ", 失敗: " + str(fail_count) + "\n⏱ 耗時: " + str(round(elapsed, 1)) + " 秒\n\n<b>詳細結果:</b>\n" + result_summary

    message_text, reply_markup = build_main_panel(status)
    query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='HTML')

    # 歸檔所有結果檔案
    all_task_ids = [task['task_id'] for task in tasks]
    archive_results(all_task_ids)


if __name__ == "__main__":
    updater = Updater(TELEGRAM_TOKEN)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()
