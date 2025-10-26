# 📚 Reading Page

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-success?logo=github)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 将你的 Kindle 阅读记录可视化为精美的页面，展示在 GitHub Pages 上。

🌐 **在线演示**: `https://chempeng.github.io/reading_page`

[English](README-EN.md) | 简体中文

## ✨ 特性

- 📊 **阅读热力图** - 全年阅读活动可视化（正方形网格）
- 📅 **每日单向历** - 自动显示当日文化内容
- 📈 **阅读统计** - 总天数、本月、当前连续、最长连续
- 🎨 **Kindle 极简风格** - 书香气息的优雅设计
- ⚡ **自动同步** - 每天自动更新（GitHub Actions）
- 📱 **响应式布局** - 完美适配桌面和移动设备

## 🚀 快速开始

### 1. Fork 本仓库

点击右上角 **Fork** 按钮。

### 2. 获取 Kindle Cookie

1. 访问 [Amazon Kindle Reading Insights](https://www.amazon.com/kindle/reading/insights) 并登录
2. 按 **F12** 打开浏览器开发者工具
3. 切换到 **Network**（网络）标签
4. **刷新页面**（F5）
5. 在请求列表中找到 `insights` 或 `data` 请求
6. 点击该请求，查看 **Headers** > **Request Headers**
7. 复制 **Cookie** 字段的完整内容

> 💡 格式示例：`session-id=xxx; ubid-main=xxx; at-main=xxx; ...`

### 3. 配置 GitHub

#### 添加 Secret

1. 进入你 fork 的仓库
2. **Settings** > **Secrets and variables** > **Actions**
3. 点击 **New repository secret**
4. 添加：
   - **Name**: `KINDLE_COOKIE`
   - **Value**: 你复制的 Cookie 完整内容

#### 配置 Pages 和权限

1. **Settings** > **Pages** > **Source** 选择 **GitHub Actions**
2. **Settings** > **Actions** > **General** > **Workflow permissions** 选择 **Read and write permissions** > **Save**

### 4. 触发首次同步

1. **Actions** > **Sync Kindle Data and Deploy**
2. 点击 **Run workflow** > **Run workflow**
3. 等待运行完成（约 1-2 分钟）
4. 访问：`https://你的用户名.github.io/reading_page`

## 📁 项目结构

```
reading_page/
├── scripts/
│   ├── kindle_sync.py      # 同步 Kindle 数据
│   ├── gen_page.py         # 生成静态页面
│   └── config.py           # 配置文件
├── data/
│   ├── kindle_data.json    # 原始数据
│   └── reading_data.json   # 处理后的数据
├── .github/workflows/
│   └── sync_kindle.yml     # 自动同步工作流
└── index.html              # 生成的页面
```

## ⚙️ 配置

### 修改自动同步时间

默认每天 UTC 00:00（北京时间 08:00）自动同步。

编辑 `.github/workflows/sync_kindle.yml`：

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 00:00 = 北京时间 08:00
  # - cron: '0 12 * * *'  # UTC 12:00 = 北京时间 20:00
```

### 手动触发同步

**Actions** > **Sync Kindle Data and Deploy** > **Run workflow**

## 🔧 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 同步数据
export KINDLE_COOKIE="your_cookie_here"
python scripts/kindle_sync.py

# 生成页面
python scripts/gen_page.py

# 在浏览器中打开 index.html
```

## ❓ 常见问题

**Q: 页面显示 404？**  
A: 确认 GitHub Pages 配置为 **GitHub Actions**，且 workflow 运行成功。等待 1-2 分钟。

**Q: 数据没有更新？**  
A: Cookie 可能过期，重新获取并更新 `KINDLE_COOKIE` secret。

**Q: 支持 Amazon.cn 吗？**  
A: Amazon.cn 的 Kindle 服务已于 2023 年关闭，仅支持 Amazon.com。

## 🤝 致谢

- [GitHubPoster](https://github.com/yihong0618/GitHubPoster) - 数据获取灵感
- [running_page](https://github.com/yihong0618/running_page) - 项目架构参考
- [Owspace 单向历](https://owspace.com) - 每日文化内容

## 📄 许可证

[MIT License](LICENSE) © 2025

---

<p align="center">
  <i>💡 Keep Reading, Keep Growing</i>
</p>
