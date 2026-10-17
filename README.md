# 容器化短网址服务系统

## 项目介绍
基于Shlink开源项目，使用Docker Compose编排短网址API、PostgreSQL数据库和自建Web管理界面，实现短链生成、跳转和访问统计功能。

## 上游仓库
- Shlink: https://github.com/shlinkio/shlink
- 使用版本: 5.1.6

## 技术栈
- Shlink 5.1.6（短网址API服务）
- PostgreSQL 16.14（数据库）
- Flask 3.1.3（Web管理界面）
- Docker Compose（容器编排）

## 启动方法
1. 确保Docker Desktop已启动
2. 在项目根目录创建.env文件，内容：
shlink-lab/
├── docker-compose.yml    # Docker Compose 编排文件
├── .env                  # 环境变量配置（不提交到 Git）
├── web/
│   ├── app.py            # Flask Web 管理界面
│   ├── requirements.txt  # Python 依赖
│   └── Dockerfile        # Web 服务 Dockerfile
└── demo-target/
└── demo.html         # 测试跳转目标页面



## 启动方法
1. 确保Docker Desktop已启动
2. 在项目根目录创建.env文件，内容：
s

POSTGRES_PASSWORD = 你的数据库密码
INITIAL_API_KEY = 你的 API 密钥

3. 启动数据库和Shlink服务：

docker compose up -d


4. 启动Web管理界面：

cd web
pip install -r requirements.txt
python app.py

5. 访问：
- Shlink API健康检查: http://localhost:8080/rest/health
- Web管理界面: http://localhost:8501

## 停止方法


docker compose down


## 备份方法
数据库数据存储在Docker卷中，运行以下命令备份：
```

docker run --rm -v shlink-lab_shlink-db:/var/lib/postgresql/data -v $(pwd):/backup alpine tar cvf /backup/db_backup.tar /var/lib/postgresql/data

## 测试方法
1. 打开Web管理界面 http://localhost:8501
2. 输入长URL（如https://www.baidu.com），点击生成短链
3. 点击生成的短链，验证是否正确跳转到目标网站
4. 刷新Web界面，查看访问次数是否更新

## 功能说明
1. 短链生成：输入长URL，自动生成短链
2. 短链跳转：访问短链自动跳转到原始长URL
3. 访问统计：记录短链的访问次数
4. 自定义短码：支持用户自定义短链后缀

## 个人实现范围
1. Docker Compose编排PostgreSQL和Shlink服务
2. 基于Flask开发Web管理界面（生成短链、查看访问统计）
3. 实现自定义短码扩展功能
4. 完成容器持久化测试（容器重建后数据不丢失）
5. 配置环境变量和数据卷，保护API密钥安全
```
