"""Sync Kindle reading data from Amazon"""

import argparse
import json
import os
import re
from http.cookies import SimpleCookie
from datetime import datetime

import requests

from config import (
    KINDLE_HISTORY_URL,
    KINDLE_HEADER,
    DATA_DIR,
    KINDLE_DATA_FILE,
    READING_DATA_FILE,
)


class KindleSync:
    def __init__(self, cookie):
        self.kindle_cookie = cookie
        self.session = requests.Session()
        self.header = KINDLE_HEADER
        self.kindle_url = KINDLE_HISTORY_URL
        self.has_session = False

    def _parse_kindle_cookie(self):
        """Parse cookie string to cookie jar"""
        cookie = SimpleCookie()
        cookie.load(self.kindle_cookie)
        cookies_dict = {}
        cookiejar = None
        for key, morsel in cookie.items():
            cookies_dict[key] = morsel.value
            cookiejar = requests.utils.cookiejar_from_dict(
                cookies_dict, cookiejar=None, overwrite=True
            )
        return cookiejar

    def make_session(self):
        """Create session with cookies"""
        cookies = self._parse_kindle_cookie()
        if not cookies:
            raise Exception("Please make sure your amazon cookie is correct")
        self.session.cookies = cookies
        self.has_session = True

    def get_kindle_read_data(self):
        """Get Kindle reading data from Amazon - 参考 GitHubPoster 的方法"""
        if not self.has_session:
            self.make_session()
        
        # 方法 1: 先从 HTML 页面获取完整的 days_read（最可靠的方法）
        # 参考 GitHubPoster-main/github_poster/loader/kindle_loader.py
        html_url = self.kindle_url.replace('/data', '')
        print(f"Fetching Kindle HTML from {html_url}...")
        r_html = self.session.get(html_url, headers=self.header)
        
        data = {}
        
        if r_html.status_code == 200:
            print("Successfully fetched HTML page")
            # 使用 GitHubPoster 的正则表达式提取 days_read
            days_read_data = self._parse_html_data(r_html.text)
            if days_read_data.get("days_read"):
                data = days_read_data
                print(f"✅ Extracted {len(data['days_read'])} reading days from HTML")
        
        # 方法 2: 同时获取 API 数据以获取统计信息（streaks, goals 等）
        print(f"\nFetching additional stats from {self.kindle_url}...")
        r_api = self.session.get(self.kindle_url, headers=self.header)
        
        if r_api.status_code == 200:
            try:
                api_data = r_api.json()
                # 合并数据：API 数据为基础，HTML 的 days_read 覆盖
                data.update(api_data)
                if days_read_data.get("days_read"):
                    data['days_read'] = days_read_data['days_read']  # 使用 HTML 的完整列表
                print("Successfully fetched API stats")
            except json.JSONDecodeError:
                print("⚠️  API response is not JSON, using HTML data only")
        
        if not data:
            raise Exception(f"Failed to fetch any Kindle data")
        
        return data

    def _parse_html_data(self, html_text):
        """
        Parse reading data from HTML
        使用 GitHubPoster 的方法: github_poster/html_parser/kindle_parser.py
        """
        # 方法 1: 使用 GitHubPoster 的正则表达式
        # 正则: "days_read":(.*),"goal_info"
        r = re.findall(r'"days_read":\s*(\[.*?\])(?:,|\s*[,}\]])', html_text, re.DOTALL)
        if r:
            try:
                days_read = json.loads(r[0])
                print(f"  Parsed {len(days_read)} days using GitHubPoster pattern")
                return {"days_read": days_read}
            except json.JSONDecodeError as e:
                print(f"  Error parsing days_read: {e}")
        
        # 方法 2: 更宽松的匹配
        r2 = re.findall(r'"days_read":\s*\[(.*?)\]', html_text, re.DOTALL)
        if r2:
            try:
                # 重新构建 JSON 数组
                json_str = f'[{r2[0]}]'
                days_read = json.loads(json_str)
                print(f"  Parsed {len(days_read)} days using fallback pattern")
                return {"days_read": days_read}
            except json.JSONDecodeError as e:
                print(f"  Error parsing days_read (fallback): {e}")
        
        print("  ⚠️  Could not find days_read in HTML")
        return {"days_read": []}

    def parse_reading_days(self, data):
        """Parse reading days from Kindle data"""
        reading_dict = {}
        
        # 方法 1: 优先使用从 HTML 提取的 days_read 数组（最完整、最准确）
        days_read = data.get("days_read", [])
        if days_read:
            print(f"📚 Processing {len(days_read)} reading days from days_read...")
            for day in days_read:
                # day is a date string like "2024-01-15"
                if day:
                    reading_dict[day] = 1  # 1 means read on this day
            
            if reading_dict:
                dates = sorted(reading_dict.keys())
                print(f"✅ Date range: {dates[0]} to {dates[-1]}")
                return reading_dict
        
        # 方法 2: 从 streak 信息中提取（备用方法）
        if not reading_dict:
            print("⚠️  No days_read found, trying streak data...")
            reading_dict = self._extract_days_from_streaks(data)
        
        # 方法 3: 从 titles_read 中提取日期（最后的备用方法）
        if not reading_dict:
            print("⚠️  No streak data, trying titles_read...")
            reading_dict = self._extract_days_from_titles(data)
        
        return reading_dict
    
    def _extract_days_from_streaks(self, data):
        """从 streak 信息中提取阅读日期"""
        from datetime import datetime, timedelta
        reading_dict = {}
        
        # 从当前每日连续阅读中提取
        daily_streak = data.get("current_daily_streak", {})
        if daily_streak and daily_streak.get("duration", 0) > 0:
            start_str = daily_streak.get("start", "")
            duration = daily_streak.get("duration", 0)
            
            if start_str:
                try:
                    # 解析开始日期
                    start_date = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                    # 生成连续的日期
                    for i in range(duration):
                        date = start_date + timedelta(days=i)
                        date_str = date.strftime("%Y-%m-%d")
                        reading_dict[date_str] = 1
                        print(f"  Found reading day from streak: {date_str}")
                except Exception as e:
                    print(f"  Error parsing streak date: {e}")
        
        # 也可以从每周连续阅读中提取额外的日期
        weekly_streak = data.get("current_weekly_streak", {})
        if weekly_streak and weekly_streak.get("duration", 0) > 0:
            start_str = weekly_streak.get("start", "")
            end_str = weekly_streak.get("end", "")
            
            if start_str and end_str:
                try:
                    start_date = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                    end_date = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
                    
                    # 注意：周连续不代表每天都读，只标记已知的连续日期
                    # 这里我们只从 daily_streak 获取精确日期
                    pass
                except Exception as e:
                    print(f"  Error parsing weekly streak: {e}")
        
        return reading_dict
    
    def _extract_days_from_titles(self, data):
        """从已读书籍列表中提取阅读日期"""
        reading_dict = {}
        
        titles_read = data.get("goal_info", {}).get("titles_read", [])
        for title in titles_read:
            date_read = title.get("date_read", "")
            if date_read:
                try:
                    # 解析日期 "2024-06-04T15:51:42Z"
                    date_obj = datetime.fromisoformat(date_read.replace('Z', '+00:00'))
                    date_str = date_obj.strftime("%Y-%m-%d")
                    reading_dict[date_str] = 1
                    print(f"  Found reading day from titles: {date_str}")
                except Exception as e:
                    print(f"  Error parsing title date: {e}")
        
        return reading_dict

    def save_data(self, data, reading_dict):
        """Save data to files"""
        # Create data directory if not exists
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Save raw Kindle data
        with open(KINDLE_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved raw Kindle data to {KINDLE_DATA_FILE}")
        
        # Save processed reading data
        reading_data = {
            "reading_days": reading_dict,
            "total_days": len(reading_dict),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        with open(READING_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(reading_data, f, ensure_ascii=False, indent=2)
        print(f"Saved reading data to {READING_DATA_FILE}")
        print(f"Total reading days: {len(reading_dict)}")

    def sync(self):
        """Main sync method"""
        try:
            # Fetch data
            data = self.get_kindle_read_data()
            
            # Parse reading days
            reading_dict = self.parse_reading_days(data)
            
            if not reading_dict:
                print("⚠️  Warning: No reading days found in the data")
                print("   This could mean:")
                print("   1. Your account has no reading history yet")
                print("   2. The API structure has changed")
                print("   3. Cookie is for a different account")
                print("   Tip: Check your reading history at Amazon Kindle Reading Insights")
            
            # Save data
            self.save_data(data, reading_dict)
            
            return True
        except Exception as e:
            print(f"Error during sync: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


def main():
    parser = argparse.ArgumentParser(description="Sync Kindle reading data from Amazon")
    parser.add_argument("cookie", nargs="?", help="Amazon Kindle cookie")
    
    args = parser.parse_args()
    
    # Get cookie from argument or environment variable
    cookie = args.cookie or os.environ.get("KINDLE_COOKIE")
    
    if not cookie:
        print("Error: Please provide Kindle cookie as argument or set KINDLE_COOKIE environment variable")
        return False
    
    # Create syncer and sync
    syncer = KindleSync(cookie)
    success = syncer.sync()
    
    if success:
        print("✅ Kindle data synced successfully!")
        return True
    else:
        print("❌ Failed to sync Kindle data")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

