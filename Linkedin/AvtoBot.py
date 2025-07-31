import pyautogui
import time
import pyperclip
import os
from typing import Union, List, Optional
from tqdm import *
import random

class AutoBot:
    def __init__(self):
        self.last_ad_check = 0
        self.AD_CHECK_INTERVAL = 5
        self.screen_width, self.screen_height = pyautogui.size()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_root = os.path.join(script_dir, "images")
        os.makedirs(self.image_root, exist_ok=True)
        self.mouse_speed = 0.5  # 默认移动速度（秒）
    
    #region 核心操作函数
    def click_left(self, img: str, retry: int = 1):
        """单击左键"""
        self._mouse_click(1, "left", img, retry)
        print(f"单击左键 [{img}]")

    def double_click(self, img: str, retry: int = 1):
        """双击左键"""
        self._mouse_click(2, "left", img, retry)
        print(f"双击左键 [{img}]")

    def click_right(self, img: str, retry: int = 1):
        """右键单击"""
        self._mouse_click(1, "right", img, retry)
        print(f"右键点击 [{img}]")

    def input_text(self, text: str, clear: bool = False):
        """输入文本"""
        if clear:
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
        
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
        print(f"输入文本: {text}")
        time.sleep(0.2)

    def wait(self, seconds: Union[int, float]):
        """等待指定秒数"""
        print(f"等待 {seconds} 秒")
        for _ in tqdm(range(seconds)):
            time.sleep(1)

    def scroll(self, amount: int, repeat: int = 1):
        """滚动鼠标滚轮"""
        for _ in range(repeat):
            pyautogui.scroll(amount)
            print(f"滚轮滚动 {amount} 单位")
            time.sleep(0.2)

    def hotkey(self, *keys: str, repeat: int = 1):
        """执行热键组合"""
        for _ in range(repeat):
            pyautogui.hotkey(*keys)
            print(f"热键操作: {'+'.join(keys)}")
            time.sleep(0.3)

    def paste_time(self, time_format: str = "%Y-%m-%d %H:%M:%S"):
        """粘贴当前时间"""
        localtime = time.strftime(time_format, time.localtime())
        pyperclip.copy(localtime)
        pyautogui.hotkey('ctrl', 'v')
        print(f"粘贴时间: {localtime}")

    def run_command(self, command: str):
        """执行系统命令"""
        os.system(command)
        print(f"执行系统命令: {command}")

    def silent_click(self, img: str, confidence: float = 0.8):
        """静默点击（找不到不报错）"""
        try:
            pos = pyautogui.locateCenterOnScreen(img, confidence=confidence)
            if pos:
                pyautogui.click(pos)
                return True
        except Exception as e:
            pass
        return False

    #endregion


    #region 私有方法
    def _mouse_click(self, clicks: int, button: str, img: str, retry: int):
        """通用鼠标点击逻辑"""
        for _ in range(retry):
            location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
            if location:
                pyautogui.click(
                    x=location.x,
                    y=location.y,
                    clicks=clicks,
                    interval=0.2,
                    duration=0.2,
                    button=button
                )
                break
            time.sleep(0.1)
    #endregion

# 初始化自动化机器人
bot = AutoBot()

#organizations=['云深处','汇川科技']
import tkinter as tk
from tkinter import messagebox

def get_org_name():
    # 创建主窗口
    root = tk.Tk()
    root.title("输入组织名称")
    root.geometry("300x150")
    
    # 创建标签和输入框
    label = tk.Label(root, text="请输入要搜索的组织名称:", font=('微软雅黑', 10))
    label.pack(pady=10)
    
    entry = tk.Entry(root, width=30)
    entry.pack(pady=10)
    
    # 定义确认按钮的回调函数
    def on_confirm():
        global org
        org = entry.get()
        if org.strip():
            root.destroy()
        else:
            messagebox.showwarning("警告", "组织名称不能为空!")
    
    # 创建确认按钮
    confirm_button = tk.Button(root, text="确认", command=on_confirm)
    confirm_button.pack(pady=10)
    
    # 运行窗口
    root.mainloop()

# 获取组织名称


org='作业帮'
print(f"将要搜索的组织: {org}")



def demo_workflow():
        
    for page in tqdm(range(24,101)):
        bot.click_left("url.png")
        
        #bot.input_text(f'https://www.linkedin.com/search/results/people/?keywords={org}&origin=SWITCH_SEARCH_VERTICAL&page={page}', clear=True)
        bot.input_text(f'https://www.linkedin.com/search/results/people/?keywords=%E4%BD%9C%E4%B8%9A%E5%B8%AE&origin=FACETED_SEARCH&page={page}&sid=eg-', clear=True)


        bot.hotkey("enter")
        bot.wait(10)
        bot.hotkey("ctrl", "s") 
        bot.wait(2)
        bot.input_text(org+str(page))
        bot.wait(2)
        bot.hotkey("enter")
        #bot.wait(20)
        bot.wait(2)
        
    # 3. 数据录入循环
    # def save_action(num):
    #     bot.input_text(str(num))
    #     bot.hotkey("ctrl", "s") 
    # bot.loop_execute(1, 10, save_action)

if __name__ == "__main__":
    demo_workflow()
    print("自动化流程执行完成！")
    