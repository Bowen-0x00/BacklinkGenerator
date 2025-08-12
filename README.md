# BacklinkGenerator - One-Click Capture, Pinpoint Recall

[English](./README.md) | [简体中文](./docs/README_ZH.md)

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Bowen-0x00/BacklinkGenerator)](https://github.com/Bowen-0x00/BacklinkGenerator/releases)

Ever wished you could effortlessly capture key information while watching videos, reading PDFs, or viewing presentations, and have it instantly saved to your knowledge base like Obsidian、Eagle or Anki? Even better, what if you could click a link in your notes and jump right back to the exact source—be it a specific timestamp in a video or the corresponding page in a PDF?

**BacklinkGenerator** is the core engine that makes this workflow possible. It specializes in capturing information and generating precise backlinks to the original content.

## ✨ Core Features

This tool is a key component in an automated knowledge-capturing workflow. When combined with productivity tools (like Quicker) and knowledge base plugins, it enables:

-   **One-Click Capture**: Quickly grab video frames, screenshots of PDF/PPT pages, or selected text.
-   **Intelligent Processing**: Automatically send the captured content and its metadata (like video timestamps or PDF page numbers) to your target application.
-   **Precise Backlinking**: Embed a clickable link in the generated note or card, allowing you to revisit the original context anytime.
-   **Broad Compatibility**: Supports capturing from various applications, including PotPlayer, BookxNote, Zotero, and PowerPoint.
-   **Multi-Platform Sync**: Seamlessly send content to your favorite note-taking and asset management tools like Obsidian, Obsidian-Excalidraw, Anki, and Eagle.

## 🚀 Getting Started

### 1. Quick Start

The easiest way to begin is by using the pre-packaged executable.

1.  Go to the [Releases page](https://github.com/Bowen-0x00/BacklinkGenerator/releases) and download the latest version of `app_hub.exe`.
2.  Use a launcher like Listary, Quicker, or your preferred tool to bind a global hotkey to `app_hub.exe`.
3.  When you want to capture something, simply press the hotkey with the required arguments.

**Common Command Examples:**

-   **Capture a sentence to Anki** (with a backlink):
    ```bash
    app_hub.exe --target=anki
    ```
-   **Capture a screenshot to Eagle** (with a backlink):
    ```bash
    app_hub.exe --target=eagle
    ```

### 2. Watch the Video Tutorial

To help you visually understand the setup and usage, a detailed video tutorial is available (in Chinese).

[![Configuration tutorial for capturing from Videos, PDFs, and PPTs to Obsidian and Excalidraw](https://i1.hdslb.com/bfs/archive/ffd87eb63fd6655d5359b29ead642d19343b6585.jpg)](https://www.bilibili.com/video/BV1qH4y1j7Q6/)

### 3. Explore the Demo Vault

You can download our [Obsidian Example Vault](https://github.com/Bowen-0x00/obsidian-excalidraw-example-vault) to experience the full workflow firsthand.

1.  Download and unzip the [Example Vault](https://github.com/Bowen-0x00/obsidian-excalidraw-example-vault).
2.  Open the vault using Obsidian.
3.  Check the `摘录方式.excalidraw.md` file for a visual demonstration of different capture methods.

### Command-Line Arguments

`app_hub.exe` serves as the central hub for all functions and automatically detects the currently active application.

| Argument  | Description                                              | Default | Example                      |
| :-------- | :------------------------------------------------------- | :------ | :--------------------------- |
| `--app`   | **Source App**: Specify the app to capture from. Usually auto-detected. | `''`    | `--app=potplayer`            |
| `--method`| **Capture Method**: How to get the content (e.g., clipboard, file). | `paste` | `--method=http`              |
| `--target`| **Target App**: Where to send the captured content.      | `ob`    | `--target=anki`              |
| `--extra` | **Extra Info**: Pass special commands or additional data. | `N/A`   | `--extra="AI anki explain"` |

## 💬 Issues, Feedback, and Ideas

If you encounter any problems, have suggestions for improvement, or want to discuss interesting ideas for new features, feel free to reach out:

-   [GitHub Issues](https://github.com/Bowen-0x00/BacklinkGenerator/issues)
-   Email me
-   Leave a comment or send a direct message on Bilibili
-   Contact me via my personal channels (WeChat, QQ)

## ❤️ Support the Project

If you find this project helpful, I'd love to hear about your experience in the comments or issues!

You can also support my work by buying me a coffee, which will motivate me to continue maintaining and developing new features.

| WeChat Pay | Buy Me a Coffee |
| :--- | :--- |
| <img src="./images/赞助码.jpg" width="200px"> | <a href='https://ko-fi.com/G2G3SY16R' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a> |