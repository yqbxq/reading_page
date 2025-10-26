# 📚 Reading Page

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-success?logo=github)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Visualize your Kindle reading records, auto-deploy to GitHub Pages

🌐 **Demo**: https://chempeng.github.io/reading_page

English | [简体中文](README.md)

## ✨ Features

- 📊 **Reading Heatmap** - Visualize yearly activity
- 📅 **Daily Calendar** - Cultural content
- 📈 **Statistics** - Days, streaks, records
- 🎨 **Kindle Style** - Minimalist design
- ⚡ **Auto Sync** - Daily updates
- 📱 **Responsive** - All devices

## 🚀 5-Minute Setup

### 1. Fork This Repo

Click **Fork** button.

### 2. Get Cookie

1. Visit [Kindle Reading Insights](https://www.amazon.com/kindle/reading/insights)
2. **F12** > **Network** tab
3. **Refresh** (F5)
4. Find `insights` request > **Headers** > Copy **Cookie**

### 3. Add Secret

1. **Settings** > **Secrets and variables** > **Actions** > **New repository secret**
2. **Name**: `KINDLE_COOKIE`
3. **Value**: Paste cookie

### 4. Configure Pages

**Settings** > **Pages** > **Source**: Select **GitHub Actions**

### 5. Run

**Actions** > **Sync Kindle Data and Deploy** > **Run workflow**

Wait 1-2 minutes, visit: `https://your-username.github.io/reading_page`

## ⚙️ Configuration

### Modify Sync Schedule

Edit `.github/workflows/sync_kindle.yml`:

```yaml
schedule:
  - cron: '0 0 * * *'  # Daily at UTC 00:00
```

### Manual Sync

**Actions** > **Run workflow**

## 🔧 Local Development

```bash
pip install -r requirements.txt
export KINDLE_COOKIE="your_cookie"
python scripts/kindle_sync.py
python scripts/gen_page.py
```

## ❓ FAQ

**Cookie expired?** Re-obtain and update Secret

**404 error?** Confirm Pages set to **GitHub Actions**

**Calendar not loading?** Normal, doesn't affect functionality

## 📄 License

[MIT License](LICENSE) © 2025

---

<p align="center">
  💡 Keep Reading, Keep Growing
</p>
