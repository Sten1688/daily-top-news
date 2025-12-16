import requests
import datetime
import os

# 1. 設定配置
API_KEY = 'c193154e0a574325b6c33d31c251d116'  # 請替換成你申請的 Key
COUNTRY = 'tw'  # 台灣
CATEGORY = 'general' # 綜合類，也可以選 technology, business 等

def fetch_top_news():
    url = f"https://newsapi.org/v2/top-headlines?country={COUNTRY}&category={CATEGORY}&apiKey={API_KEY}&pageSize=10"
    response = requests.get(url)
    data = response.json()
    return data.get('articles', [])

def generate_html(articles):
    # 取得當前日期
    today = datetime.datetime.now().strftime("%Y年%m月%d日")
    
    # Apple 風格的 HTML 模板
    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>每日熱門新聞 Top 10</title>
        <style>
            :root {{
                --bg-color: #f5f5f7;
                --card-bg: #ffffff;
                --text-main: #1d1d1f;
                --text-secondary: #86868b;
                --link-color: #0066cc;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                background-color: var(--bg-color);
                color: var(--text-main);
                margin: 0;
                padding: 40px 20px;
                line-height: 1.5;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
            }}
            header {{
                text-align: center;
                margin-bottom: 40px;
            }}
            h1 {{
                font-size: 48px;
                font-weight: 700;
                letter-spacing: -0.02em;
                margin-bottom: 10px;
            }}
            .date {{
                color: var(--text-secondary);
                font-size: 20px;
                font-weight: 500;
            }}
            .news-list {{
                list-style: none;
                padding: 0;
            }}
            .news-item {{
                background: var(--card-bg);
                border-radius: 18px;
                padding: 30px;
                margin-bottom: 20px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.04);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                display: flex;
                flex-direction: column;
            }}
            .news-item:hover {{
                transform: scale(1.01);
                box-shadow: 0 10px 20px rgba(0,0,0,0.08);
            }}
            .rank {{
                font-size: 14px;
                font-weight: 600;
                color: var(--text-secondary);
                text-transform: uppercase;
                margin-bottom: 8px;
            }}
            .news-title {{
                font-size: 24px;
                font-weight: 600;
                margin: 0 0 12px 0;
                line-height: 1.3;
            }}
            .news-title a {{
                color: var(--text-main);
                text-decoration: none;
            }}
            .news-desc {{
                font-size: 17px;
                color: var(--text-secondary);
                margin-bottom: 20px;
            }}
            .read-more {{
                font-size: 17px;
                color: var(--link-color);
                text-decoration: none;
                font-weight: 500;
                align-self: flex-start;
            }}
            .read-more:hover {{
                text-decoration: underline;
            }}
            footer {{
                text-align: center;
                margin-top: 50px;
                color: var(--text-secondary);
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>今日焦點</h1>
                <div class="date">{today}</div>
            </header>
            
            <ul class="news-list">
    """

    for index, article in enumerate(articles, 1):
        title = article.get('title', '無標題')
        # 過濾掉新聞來源名稱 (例如 " - Yahoo新聞") 以保持乾淨
        clean_title = title.split(' - ')[0] 
        desc = article.get('description', '') or ''
        link = article.get('url', '#')
        
        item_html = f"""
                <li class="news-item">
                    <span class="rank">No. {index} Trending</span>
                    <h2 class="news-title"><a href="{link}" target="_blank">{clean_title}</a></h2>
                    <div class="news-desc">{desc[:100]}...</div>
                    <a href="{link}" target="_blank" class="read-more">閱讀更多 ›</a>
                </li>
        """
        html_content += item_html

    html_content += """
            </ul>
            <footer>
                <p>Designed by AI Gemini • Updates Automatically</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    return html_content

if __name__ == "__main__":
    articles = fetch_top_news()
    if articles:
        html = generate_html(articles)
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("網頁更新成功！")
    else:
        print("無法獲取新聞資料。")