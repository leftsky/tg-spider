import os
import asyncio
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from tqdm import tqdm

# 加载环境变量
load_dotenv()

# Telegram API 配置
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')
SESSION_NAME = os.getenv('SESSION_NAME')
MEDIA_DIR = Path(os.getenv('MEDIA_DIR', './downloads'))

# 确保下载目录存在
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

class TeleSpider:
    def __init__(self):
        self.client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    async def start(self):
        """启动客户端"""
        await self.client.start(phone=PHONE)
        print("已成功连接到 Telegram!")

    async def get_dialogs(self):
        """获取对话列表"""
        dialogs = await self.client.get_dialogs()
        return dialogs

    async def get_messages(self, dialog, limit=100):
        """获取指定对话的消息"""
        messages = await self.client.get_messages(dialog, limit=limit)
        return messages

    async def download_media(self, message, progress_callback=None):
        """下载媒体文件"""
        if message.media:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if isinstance(message.media, MessageMediaPhoto):
                filename = f"{timestamp}_photo.jpg"
            elif isinstance(message.media, MessageMediaDocument):
                orig_filename = message.file.name or f"{timestamp}_document"
                filename = f"{timestamp}_{orig_filename}"
            else:
                return None

            filepath = MEDIA_DIR / filename
            await self.client.download_media(message, file=str(filepath), progress_callback=progress_callback)
            return filepath
        return None

    def progress_callback(self, current, total):
        """下载进度回调"""
        if not hasattr(self, 'pbar'):
            self.pbar = tqdm(total=total, unit='B', unit_scale=True)
        self.pbar.update(current - self.pbar.n)
        if current == total:
            self.pbar.close()
            delattr(self, 'pbar')

async def main():
    spider = TeleSpider()
    await spider.start()

    while True:
        print("\n=== TeleSpider 菜单 ===")
        print("1. 显示对话列表")
        print("2. 获取聊天记录")
        print("3. 下载媒体文件")
        print("4. 退出")
        
        choice = input("\n请选择操作 (1-4): ")

        if choice == '1':
            dialogs = await spider.get_dialogs()
            print("\n=== 对话列表 ===")
            for i, dialog in enumerate(dialogs, 1):
                print(f"{i}. {dialog.name} ({dialog.id})")

        elif choice == '2':
            dialogs = await spider.get_dialogs()
            print("\n=== 选择对话 ===")
            for i, dialog in enumerate(dialogs, 1):
                print(f"{i}. {dialog.name}")
            
            dialog_index = int(input("\n请选择对话序号: ")) - 1
            limit = int(input("请输入要获取的消息数量: "))
            
            messages = await spider.get_messages(dialogs[dialog_index], limit=limit)
            print("\n=== 聊天记录 ===")
            for msg in messages:
                timestamp = msg.date.strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] {msg.sender_id}: {msg.text or '[媒体消息]'}")

        elif choice == '3':
            dialogs = await spider.get_dialogs()
            print("\n=== 选择对话 ===")
            for i, dialog in enumerate(dialogs, 1):
                print(f"{i}. {dialog.name}")
            
            dialog_index = int(input("\n请选择对话序号: ")) - 1
            limit = int(input("请输入要检查的最近消息数量: "))
            
            messages = await spider.get_messages(dialogs[dialog_index], limit=limit)
            media_messages = [msg for msg in messages if msg.media]
            
            print(f"\n找到 {len(media_messages)} 个媒体文件")
            for msg in media_messages:
                print(f"正在下载: {msg.file.name if hasattr(msg.file, 'name') else '未命名文件'}")
                filepath = await spider.download_media(msg, spider.progress_callback)
                if filepath:
                    print(f"已下载到: {filepath}")

        elif choice == '4':
            print("感谢使用 TeleSpider!")
            break

        else:
            print("无效的选择，请重试")

    await spider.client.disconnect()

if __name__ == "__main__":
    asyncio.run(main()) 