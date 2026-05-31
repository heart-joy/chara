import os
import sys
import io
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import shutil

try:
    # 重新包装 stdout，指定 encoding='utf-8'
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
except Exception:
    pass


# ================= 配置区域 =================
SERVER_URL = "http://192.168.10.223:8000/"
SAVE_FOLDER_NAME = "stress_test_downloads"
MAX_WORKERS = 5          # 并发线程数
REQUEST_TIMEOUT = 10     # 单次请求超时时间(秒)
# ============================================

def get_script_dir():
    """获取当前脚本所在的绝对路径"""
    return os.path.dirname(os.path.abspath(__file__))

def download_file(url, save_path):
    """
    下载单个文件的函数
    """
    filename = os.path.basename(url)
    full_path = os.path.join(save_path, filename)

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            with open(full_path, 'wb') as f:
                f.write(response.content)
            print(f"[OK] 下载成功: {filename}")
            return True
        else:
            print(f"[ERROR] 状态码错误 ({response.status_code}): {filename}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 请求失败: {filename} -> {e}")
        return False
    except Exception as e:
        print(f"[ERROR] 未知错误: {filename} -> {e}")
        return False

def test():
    script_dir = get_script_dir()
    save_dir = os.path.join(script_dir, SAVE_FOLDER_NAME)

    # 创建保存目录
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"[INFO] 已创建保存目录: {save_dir}")

    # 模拟生成一些测试文件名 (你可以替换为你真实的文件列表获取逻辑)
    # 这里假设你要下载 digit_1.png 到 digit_49.png
    file_list = [f"digit_{i:02d}.png" for i in range(1,50)]

    print(f"---------------- 开始下载测试 ----------------")
    print(f"目标服务器: {SERVER_URL}")
    print(f"保存位置:   {save_dir}")
    print(f"文件总数:   {len(file_list)}")
    print(f"--------------------------------------------")

    success_count = 0
    fail_count = 0

    # 使用线程池并发下载
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}
        for filename in file_list:
            url = f"{SERVER_URL}{filename}"
            future = executor.submit(download_file, url, save_dir)
            futures[future] = filename

        for future in as_completed(futures):
            if future.result():
                success_count += 1
            else:
                fail_count += 1

    print(f"--------------------------------------------")
    print(f"[完成] 总计: {len(file_list)}, 成功: {success_count}, 失败: {fail_count}")
    
        

if __name__ == "__main__":
    try:
        while True:
            script_dir = get_script_dir()
            save_dir = os.path.join(script_dir, SAVE_FOLDER_NAME)
            if os.path.exists(save_dir):
                try:
                    shutil.rmtree(save_dir)
                    print(f"[INFO] 已彻底清理之前的下载文件夹: {save_dir}", flush=True)
                except Exception as e:
                    print(f"[ERROR] 清理文件夹失败: {e}", flush=True)
            test()
            time.sleep(1)
            # 随机等待一段时间，模拟真实用户行为，避免过快的请求导致服务器压力过大  
            rand = random.randint(60,120)
            print(f"[INFO] 等待 {rand} 秒后开始下载测试...", flush=True)
            for i in range(rand * 10):
                time.sleep(0.1)
    except Exception as e:
        print(f"[ERROR] 测试异常终止")
    