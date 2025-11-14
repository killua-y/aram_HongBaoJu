# 和朋友算账小工具

一个简单易用的记账网页应用，用于记录和统计朋友之间的盈亏情况。所有人访问同一个网址，看到同一份账本。

## 技术栈

- **后端**: Python + Flask
- **前端**: HTML + CSS（Jinja2 模板）
- **数据库**: SQLite
- **特点**: 前后端一体，部署简单，无需复杂配置

## 功能特性

✅ 添加记录：输入名字、金额（正数=赚，负数=欠）、可选备注  
✅ 实时统计：自动计算每个人的总盈亏  
✅ 记录列表：查看所有历史记录  
✅ 删除记录：可以删除单条记录  
✅ 响应式设计：支持手机和电脑访问  

## 本地运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

应用会在 `http://localhost:5000` 启动。

首次运行会自动创建 SQLite 数据库 `expenses.db`。

## 部署到线上

### 方案一：Render（推荐）

1. **推送代码到 GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **在 Render 创建 Web Service**
   - 访问 [render.com](https://render.com)
   - 点击 "New +" → "Web Service"
   - 连接你的 GitHub 仓库
   - 配置如下：
     - **Name**: `expense-splitter`（或其他名字）
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Instance Type**: `Free`（免费层）

3. **环境变量（可选）**
   - 在 Render 的 Environment 中添加：
     - `SECRET_KEY`: 一个随机字符串（用于 Flask session）

4. **部署完成**
   - Render 会给你一个网址，例如：`https://your-app-name.onrender.com`
   - 把这个链接分享给朋友们即可

### 方案二：Railway

1. 访问 [railway.app](https://railway.app)
2. 点击 "New Project" → "Deploy from GitHub repo"
3. 选择你的仓库
4. Railway 会自动检测 Python 项目
5. 设置启动命令：`gunicorn app:app --bind 0.0.0.0:$PORT`
6. 部署完成后获取网址

### 方案三：PythonAnywhere

1. 注册 [pythonanywhere.com](https://www.pythonanywhere.com)
2. 上传项目文件（通过 Web 界面或 Git）
3. 在 Web 页面配置：
   - **Source code**: `/home/yourusername/expense-splitter`
   - **Working directory**: `/home/yourusername/expense-splitter`
   - **WSGI configuration file**: 创建并配置 WSGI

### 方案四：Fly.io

1. 安装 Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. 登录: `fly auth login`
3. 初始化: `fly launch`（会自动创建 `fly.toml`）
4. 部署: `fly deploy`

## 项目结构

```
aram_HongBaoJu/
├── app.py                 # Flask 后端主文件
├── requirements.txt       # Python 依赖
├── expenses.db           # SQLite 数据库（运行后自动创建）
├── templates/
│   └── index.html        # 前端页面模板
└── static/
    └── style.css         # 样式文件
```

## 使用说明

1. **添加记录**
   - 在表单中输入名字、金额（正数表示赚，负数表示欠）
   - 可选填写备注
   - 点击"提交"

2. **查看统计**
   - "每个人总盈亏"卡片显示每个人的累计金额
   - 绿色表示正数（赚），红色表示负数（欠）

3. **查看历史**
   - "所有记录"表格显示所有历史记录
   - 按时间倒序排列

4. **删除记录**
   - 点击记录旁边的"删除"按钮
   - 确认后删除

5. **清空所有**
   - 在"危险操作"区域输入 `CLEAR_ALL` 确认
   - 点击"清空所有记录"

## 注意事项

⚠️ **数据安全**
- 本应用没有用户认证，所有人都可以添加/删除记录
- 适合信任的小团体使用
- 如需权限控制，需要添加登录功能

⚠️ **生产环境**
- 记得修改 `app.py` 中的 `SECRET_KEY`（使用环境变量）
- 考虑定期备份 `expenses.db` 文件
- 如果数据量大，可以考虑迁移到 PostgreSQL/MySQL

## 开发建议

如果想扩展功能，可以考虑：

- [ ] 添加用户登录/注册
- [ ] 支持多个房间/账本
- [ ] 导出数据为 CSV/Excel
- [ ] 添加图表可视化
- [ ] 支持编辑记录
- [ ] 添加数据统计（总金额、平均等）

## License

MIT
