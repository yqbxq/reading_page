# 📚 Reading Page

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-success?logo=github)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Visualize your Kindle reading records as a beautiful page and display it on GitHub Pages.

🌐 **Demo**: `https://chempeng.github.io/reading_page`

English | [简体中文](README.md)

## ✨ Features

- 📊 **Reading Heatmap** - Visualize yearly reading activity (square grid)
- 📅 **Daily Calendar** - Auto-display daily cultural content
- 📈 **Reading Statistics** - Total days, this month, current streak, longest streak
- 🎨 **Kindle Minimalist Style** - Elegant design with book aesthetics
- ⚡ **Auto Sync** - Daily updates via GitHub Actions
- 📱 **Responsive Layout** - Perfect for desktop and mobile devices

## 🚀 Quick Start

### 1. Fork This Repository

Click the **Fork** button in the top right corner.

### 2. Get Kindle Cookie

1. Visit [Amazon Kindle Reading Insights](https://www.amazon.com/kindle/reading/insights) and log in
2. Press **F12** to open browser developer tools
3. Switch to **Network** tab
4. **Refresh the page** (F5)
5. Find the `insights` or `data` request in the list
6. Click the request, then check **Headers** > **Request Headers**
7. Copy the entire **Cookie** field content

> 💡 Format example: `session-id=xxx; ubid-main=xxx; at-main=xxx; ...`

### 3. Configure GitHub

#### Add Secret

1. Go to your forked repository
2. **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret**
4. Add:
   - **Name**: `KINDLE_COOKIE`
   - **Value**: The cookie content you copied

#### Configure Pages and Permissions

1. **Settings** > **Pages** > **Source**: Select **GitHub Actions**
2. **Settings** > **Actions** > **General** > **Workflow permissions**: Select **Read and write permissions** > **Save**

### 4. Trigger First Sync

1. **Actions** > **Sync Kindle Data and Deploy**
2. Click **Run workflow** > **Run workflow**
3. Wait for completion (about 1-2 minutes)
4. Visit: `https://your-username.github.io/reading_page`

## 📁 Project Structure

```
reading_page/
├── scripts/
│   ├── kindle_sync.py      # Sync Kindle data
│   ├── gen_page.py         # Generate static page
│   └── config.py           # Configuration
├── data/
│   ├── kindle_data.json    # Raw data
│   └── reading_data.json   # Processed data
├── .github/workflows/
│   └── sync_kindle.yml     # Auto-sync workflow
└── index.html              # Generated page
```

## ⚙️ Configuration

### Modify Auto-Sync Schedule

Default: Daily at UTC 00:00 (8:00 AM Beijing Time).

Edit `.github/workflows/sync_kindle.yml`:

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 00:00 = 8:00 AM Beijing Time
  # - cron: '0 12 * * *'  # UTC 12:00 = 8:00 PM Beijing Time
```

### Manual Sync

**Actions** > **Sync Kindle Data and Deploy** > **Run workflow**

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Sync data
export KINDLE_COOKIE="your_cookie_here"
python scripts/kindle_sync.py

# Generate page
python scripts/gen_page.py

# Open index.html in browser
```

## ❓ FAQ

**Q: Page shows 404?**  
A: Confirm GitHub Pages is set to **GitHub Actions** and workflow ran successfully. Wait 1-2 minutes.

**Q: Data not updating?**  
A: Cookie may have expired. Re-obtain and update the `KINDLE_COOKIE` secret.

**Q: Does it support Amazon.cn?**  
A: Amazon.cn's Kindle service closed in 2023. Only Amazon.com is supported.

## 🤝 Credits

- [GitHubPoster](https://github.com/yihong0618/GitHubPoster) - Data fetching inspiration
- [running_page](https://github.com/yihong0618/running_page) - Project architecture reference
- [Owspace Daily Calendar](https://owspace.com) - Daily cultural content

## 📄 License

[MIT License](LICENSE) © 2025

---

<p align="center">
  <i>💡 Keep Reading, Keep Growing</i>
</p>

