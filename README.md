# 📚 Reading Page

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-success?logo=github)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 将 Kindle 阅读记录可视化，自动部署到 GitHub Pages

🌐 **Demo**: https://chempeng.github.io/reading_page

[English](README-EN.md) | 简体中文

## ✨ 特性

- 📊 **阅读热力图** - 全年阅读活动可视化
- 📅 **每日单向历** - 自动显示文化内容
- 📈 **阅读统计** - 总天数、本月、连续记录
- 🎨 **Kindle 极简风格** - 优雅的书香设计
- ⚡ **自动同步** - 每天自动更新
- 📱 **响应式** - 完美适配各种设备

## 🚀 5 分钟快速部署

### 1. Fork 本仓库

点击右上角 **Fork**。

### 2. 获取 Cookie

1. 访问 [Kindle Reading Insights](https://www.amazon.com/kindle/reading/insights)
2. **F12** 开发者工具 > **Network** 标签
3. **刷新页面**（F5）
4. 找到 `insights` 请求 > **Headers** > 复制 **Cookie** 字段

### 3. 配置 Secret

1. **Settings** > **Secrets and variables** > **Actions** > **New repository secret**
2. **Name**: `KINDLE_COOKIE`
3. **Value**: 粘贴 Cookie

### 4. 配置 Pages

**Settings** > **Pages** > **Source** 选择 **GitHub Actions**

### 5. 运行

**Actions** > **Sync Kindle Data and Deploy** > **Run workflow**

等待 1-2 分钟，访问：`https://你的用户名.github.io/reading_page`

## ⚙️ 配置

### 修改同步时间

编辑 `.github/workflows/sync_kindle.yml`：

```yaml
schedule:
  - cron: '0 0 * * *'  # 每天 UTC 00:00（北京时间 08:00）
```

### 手动同步

**Actions** > **Run workflow**

## 🔧 本地运行

```bash
pip install -r requirements.txt
export KINDLE_COOKIE="your_cookie"
python scripts/kindle_sync.py
python scripts/gen_page.py
```

## ❓ 常见问题

**Cookie 过期？** 重新获取并更新 Secret

**404 错误？** 确认 Pages 配置为 **GitHub Actions**

## 🤝 致谢

- [GitHubPoster](https://github.com/yihong0618/GitHubPoster) - 数据获取灵感
- [running_page](https://github.com/yihong0618/running_page) - 项目架构参考
- [单向历](https://owspace.com) - 每日文化内容

## 📄 许可证

[MIT License](LICENSE) © 2025

---

<p align="center">
  💡 Keep Reading, Keep Growing
</p>
