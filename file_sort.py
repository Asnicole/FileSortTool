import os
import shutil
import time

# ===================== 1. 定义文件分类规则 =====================
FILE_TYPE = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "视频": [".mp4", ".avi", ".mov", ".flv", ".mkv"],
    "文档": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".txt"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "程序": [".exe", ".bat", ".cmd", ".py"],
    "音频": [".mp3", ".wav", ".flac"]
}

# ===================== 2. 日志记录函数 =====================
def write_log(msg):
    """写入运行日志"""
    with open("file_sort_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    print(msg)

# ===================== 3. 获取文件对应的分类文件夹 =====================
def get_folder_name(file_suffix):
    """根据后缀匹配分类"""
    for folder_name, suffix_list in FILE_TYPE.items():
        if file_suffix.lower() in suffix_list:
            return folder_name
    return "其他文件"

# ===================== 4. 核心整理函数 =====================
def sort_files(folder_path):
    # 判断文件夹是否存在
    if not os.path.exists(folder_path):
        write_log(f"错误：路径 {folder_path} 不存在")
        return

    # 遍历文件夹所有文件
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        # 拼接完整文件路径
        old_path = os.path.join(folder_path, file_name)

        # 跳过文件夹，只处理文件
        if os.path.isdir(old_path):
            continue

        # 获取文件后缀
        _, suffix = os.path.splitext(file_name)
        # 获取分类名
        target_folder = get_folder_name(suffix)
        # 新文件夹完整路径
        new_folder_path = os.path.join(folder_path, target_folder)

        # 不存在则创建分类文件夹
        if not os.path.exists(new_folder_path):
            os.mkdir(new_folder_path)
            write_log(f"创建文件夹：{target_folder}")

        # 新文件路径
        new_path = os.path.join(new_folder_path, file_name)

        # 处理重复文件
        if os.path.exists(new_path):
            write_log(f"跳过重复文件：{file_name}")
            continue

        # 移动文件，捕获异常
        try:
            shutil.move(old_path, new_path)
            write_log(f"成功移动：{file_name} → {target_folder}")
        except Exception as e:
            write_log(f"移动失败：{file_name}，原因：{str(e)}")

# ===================== 5. 程序入口 =====================
if __name__ == "__main__":
    write_log("====== 文件整理程序启动 ======")
    # 这里可以改成你要整理的文件夹绝对路径
    target_dir = "./test_folder"

    # 自动创建测试文件夹（方便新手测试）
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    sort_files(target_dir)
    write_log("====== 文件整理程序执行完毕 ======\n")
