# Easy-YT-DLP

**Easy-YT-DLP** 是一个基于 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 的 Python 脚本，旨在简化音频下载流程，支持手动输入 URL 和剪贴板监控两种模式，自动创建下载目录，具备自动重试机制，并提供友好的命令行界面。

---

## ⚙️ 使用方法

### 手动输入模式

启动脚本后，选择手动输入模式，输入视频 URL 即可下载音频。

```bash
python easy_yt_dlp.py
```

### 剪贴板监控模式

启动脚本后，选择剪贴板监控模式，程序将自动监听剪贴板内容，当检测到有效的 YouTube 链接时，自动开始下载。

```bash
python easy_yt_dlp.py
```

---

## 📝 注意事项

* **版权声明**：请确保仅下载公开授权或个人允许的内容，遵守相关法律法规。
* **依赖说明**：脚本依赖于 `yt-dlp` 和 `clipboard-monitor`，请确保已正确安装。
* **系统兼容性**：本脚本在 Windows、Linux 和 macOS 上均可运行。

---

## 📄 License

本项目采用 [MIT License](LICENSE) 进行许可。
