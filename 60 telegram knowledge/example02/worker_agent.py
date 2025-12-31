import os
import time
import glob
import subprocess
import socket

# 設定共享目錄路徑
BASE_DIR = "/opt/mt-script/mt-bot-service"
QUEUE_DIR = os.path.join(BASE_DIR, "queue")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

# 直接取得宿主機的實體 hostname
MY_HOSTNAME = socket.gethostname()

def run_cmd(cmds):
    try:
        # 依序執行指令
        for cmd in cmds:
            print(f"正在執行指令: {cmd}")
            # shell=True 允許執行 sh 腳本，cwd 確保在正確目錄下執行
            result = subprocess.run(cmd, shell=True, check=True, cwd=BASE_DIR, capture_output=True, text=True)
            print(f"指令輸出: {result.stdout}")
        return "Success"
    except subprocess.CalledProcessError as e:
        error_msg = f"Command failed: {e.cmd} | Error: {e.stderr}"
        print(error_msg)
        return error_msg
    except Exception as e:
        return f"System Error: {str(e)}"

def main():
    print(f"--- Worker Agent 啟動 ---")
    print(f"Hostname: {MY_HOSTNAME}")
    print(f"監聽目錄: {QUEUE_DIR}")

    # 確保目錄存在
    os.makedirs(QUEUE_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    while True:
        # 搜尋符合自己 hostname 的任務檔 (例如: werp-coma-proxy_*.task)
        pattern = os.path.join(QUEUE_DIR, f"{MY_HOSTNAME}_*.task")
        tasks = glob.glob(pattern)

        for task_path in tasks:
            task_file = os.path.basename(task_path)
            # 檔名格式: werp-coma-proxy_maint_on_1703059200.task
            parts = task_file.replace(".task", "").split('_')
            
            if len(parts) < 3:
                continue
                
            task_id = task_file.replace(".task", "")
            # 抓取中間的所有內容作為 action (支援 maint_on 或 restart)
            action = "_".join(parts[1:-1])
            
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 收到任務: {action}")
            
            # 根據 hostname 類型決定執行內容
            result_msg = "Unknown Command"
            
            if MY_HOSTNAME.endswith("-proxy"):
                if action == "maint_on":
                    result_msg = run_cmd(["sh /opt/mt-script/01_nginx_index_sync.sh", "sh /opt/mt-script/02_nginx_stamt.sh"])
                elif action == "maint_off":
                    result_msg = run_cmd(["sh /opt/mt-script/03_nginx_endmt.sh"])
            
            elif MY_HOSTNAME.endswith("-ap"):
                if action == "restart":
                    # 這裡是宿主機，所以可以直接執行 sh 指令來控制宿主機上的其他 Docker
                    result_msg = run_cmd(["sh /opt/mt-script/containr-stop.sh", "sh /opt/mt-script/containr-start.sh"])

            # 寫入結果檔供 Master 讀取
            with open(os.path.join(RESULTS_DIR, f"{task_id}.result"), 'w') as f:
                f.write(result_msg)
            
            # 完成後刪除任務檔
            try:
                os.remove(task_path)
            except:
                pass

        time.sleep(3) # 每 3 秒檢查一次

if __name__ == "__main__":
    main()
