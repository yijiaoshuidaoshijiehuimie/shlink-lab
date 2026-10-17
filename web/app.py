from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

SHLINK_API_URL = "http://localhost:8080/rest"
API_KEY = "test_key_123456789abcdef"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>短网址管理系统</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 20px auto; padding: 0 20px; }
        .input-group { margin-bottom: 15px; }
        input { padding: 10px; width: 70%; font-size: 16px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        .short-url-item { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>短网址管理系统</h1>
    <form method="POST">
        <div class="input-group">
            <input type="text" name="long_url" placeholder="输入长URL" required>
        </div>
        <div class="input-group">
            <input type="text" name="custom_slug" placeholder="自定义短码（可选）">
        </div>
        <button type="submit">生成短链</button>
    </form>
    <h2>短链列表</h2>
    {% for item in short_urls %}
    <div class="short-url-item">
        <p>短链: <a href="{{ item.shortUrl }}" target="_blank">{{ item.shortUrl }}</a></p>
        <p>长链: {{ item.longUrl }}</p>
        <p>访问次数: {{ item.visitsSummary.total }}</p>
    </div>
    {% endfor %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        custom_slug = request.form.get('custom_slug', '').strip()
        
        headers = {'X-Api-Key': API_KEY, 'Content-Type': 'application/json'}
        data = {'longUrl': long_url}
        if custom_slug:
            data['customSlug'] = custom_slug
        
        response = requests.post(f"{SHLINK_API_URL}/v3/short-urls", json=data, headers=headers)
        if response.status_code == 201:
            return redirect('/')
    
    headers = {'X-Api-Key': API_KEY}
    response = requests.get(f"{SHLINK_API_URL}/v3/short-urls?paginateBy=10", headers=headers)
    short_urls = response.json().get('shortUrls', {}).get('data', [])
    
    return render_template_string(HTML_TEMPLATE, short_urls=short_urls)

if __name__ == '__main__':
    app.run(port=8501, debug=True)
