# TeleSpider

TeleSpider 是一个 Telegram 聊天记录和媒体管理工具，可以帮助你获取聊天记录、下载和管理媒体文件。

## 功能特点

- 获取和显示聊天记录
- 下载媒体文件（图片、视频、文档等）
- 本地媒体文件管理
- 支持对话历史记录导出

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/telespider.git
cd telespider
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
   - 复制 `.env.example` 为 `.env`
   - 在 [Telegram API Development Tools](https://my.telegram.org/apps) 获取 API 凭证
   - 填写 `.env` 文件中的配置信息

## 使用方法

1. 运行主程序：
```bash
python main.py
```

2. 首次运行时需要进行 Telegram 账号验证
3. 按照提示选择要执行的操作

## 注意事项

- 请确保你有足够的存储空间用于保存媒体文件
- 建议使用虚拟环境运行项目
- 请遵守 Telegram 的使用条款和 API 限制

## 许可证

MIT License 