#!/usr/bin/env python3
import os
import sys
import subprocess
import platform

def build_executable():
    """构建独立可执行文件"""
    
    system = platform.system()
    
    # 基本的 PyInstaller 命令
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", "yt-t",
        "--add-data", "yt_t:yt_t",
        "-c",  # 控制台应用
    ]
    
    # 根据操作系统添加特定选项
    if system == "Darwin":  # macOS
        # 不指定架构，让 PyInstaller 自动检测
        pass
    elif system == "Windows":
        cmd.extend([
            "--icon", "icon.ico" if os.path.exists("icon.ico") else None,
        ])
        cmd = [x for x in cmd if x is not None]  # 移除 None 值
    
    # 添加入口点
    cmd.append("yt_t/cli.py")
    
    print(f"构建命令: {' '.join(cmd)}")
    
    # 执行构建
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ 构建成功！")
        print(f"可执行文件位置: dist/yt-t{'.exe' if system == 'Windows' else ''}")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 构建失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_executable()