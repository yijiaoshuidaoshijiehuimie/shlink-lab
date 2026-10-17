from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

# Shlink API配置
SHLINK_API_URL = "http://localhost:8080/rest/v3"
SHLINK_API_KEY = "test_key_123456789abcdef"

HEADERS = {
    "X-Api-Key": SHLINK_API_KEY,
    "Content-Type": "application/json"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>短网址管理系统</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 0 20px; }
        h1 { color: #333; }
        form { margin: 20px 0; display: flex; gap: 10px; }
        input[type="url"] { flex: 1; padding: 10px; font-size: 16px; border: 1px solid #ddd; border-radius: 4px; }
        button { padding: 10px 20px; font-size: 16px; background: #1a73e8; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #1557b0; }
        .error { color: red; margin: 10px 0; }
        .short-url-item { padding: 15px; border: 1px solid #eee; margin: 10px 0; border-radius: 4px; }
        .short-url-item a { color: #1a73e8; }
        .stats { color: #666; font-size: 14px; margin-top: 5px; }
    </style>
</head>
<body>
    <h1>短网址管理系统</h1>
    
    <form method="POST" action="/create">
        <input type="url" name="long_url" placeholder="输入长URL" required>
        <button type="submit">生成短链</button>
    </form>
    
    {% if error %}
    <div class="error">错误：{{ error }}</div>
    {% endif %}
    
    <h2>短链列表</h2>
    {% for item in short_urls %}
    <div class="short-url-item">
        <div>短链：<a href="{{ item.shortUrl }}" target="_blank">{{ item.shortUrl }}</a></div>
        <div>长链：{{ item.longUrl }}</div>
        <div class="stats">访问次数：{{ item.visitsSummary.total }}</div>
    </div>
    {% endfor %}
</body>
</html>
"""

@app.route('/')
def index():
    error = request.args.get('error', '')
    short_urls = []
    try:
        resp = requests.get(f"{SHLINK_API_URL}/short-urls", headers=HEADERS, params={"itemsPerPage": 50})
        if resp.status_code == 200:
            data = resp.json()
            short_urls = data.get('shortUrls', {}).get('data', [])
    except Exception as e:
        error = str(e)
    return render_template_string(HTML_TEMPLATE, error=error, short_urls=short_urls)

@app.route('/create', methods=['POST'])
def create():
    long_url = request.form.get('long_url', '')
    if not long_url:
        return redirect('/?error=请输入URL')
    try:
        resp = requests.post(
            f"{SHLINK_API_URL}/short-urls",
            headers=HEADERS,
            json={"longUrl": long_url}
        )
        if resp.status_code == 200:
            return redirect('/')
        else:
            return redirect(f'/?error=创建失败：{resp.text}')
    except Exception as e:
        return redirect(f'/?error={str(e)}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501, debug=False)
