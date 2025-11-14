# Render 部署指南

## 📋 部署前准备

### 1. 确保代码已提交到 GitHub

```bash
# 检查当前状态
git status

# 如果还有未提交的更改，先提交
git add .
git commit -m "准备部署到 Render"

# 如果没有设置远程仓库，添加 GitHub 仓库
git remote add origin https://github.com/你的用户名/aram_HongBaoJu.git

# 推送到 GitHub（如果是第一次推送）
git push -u origin main
```

## 🚀 在 Render 上部署

### 步骤 1: 注册/登录 Render

1. 访问 [https://render.com](https://render.com)
2. 点击右上角 "Get Started" 或 "Sign Up"
3. 选择 "Sign up with GitHub"（推荐，可以直接连接仓库）

### 步骤 2: 创建 Web Service

1. 登录后，点击右上角的 **"New +"** 按钮
2. 选择 **"Web Service"**
3. 会弹出 "Connect a repository" 页面

### 步骤 3: 连接 GitHub 仓库

1. 如果是第一次连接，点击 **"Connect GitHub"**
   - 会跳转到 GitHub 授权页面
   - 选择要授权的仓库或整个账户
   - 点击 "Install" 或 "Authorize"
2. 在仓库列表中找到你的 `aram_HongBaoJu` 仓库
3. 点击 **"Connect"**

### 步骤 4: 配置 Web Service

配置项如下：

| 配置项 | 值 |
|--------|-----|
| **Name** | `aram-hongbaoju` 或你喜欢的名字（只能小写字母、数字、横线） |
| **Region** | `Singapore` 或离你最近的区域 |
| **Branch** | `main`（确保是你推送代码的分支） |
| **Root Directory** | 留空（如果是根目录） |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Instance Type** | `Free`（免费层，足够使用） |

### 步骤 5: 环境变量（可选）

在 "Advanced" 或 "Environment" 部分，可以添加环境变量：

- **Key**: `SECRET_KEY`
- **Value**: 一个随机字符串（例如：`your-secret-key-12345`）

> 注意：如果不设置，Flask 会使用默认的 secret key，但这在生产环境中不够安全。

### 步骤 6: 开始部署

1. 点击页面底部的 **"Create Web Service"**
2. Render 会自动开始构建和部署
3. 等待 2-5 分钟（首次部署较慢）

### 步骤 7: 查看部署状态

部署过程中可以看到：
- 构建日志（Build Logs）
- 实时日志（Live Logs）

**构建成功标志**：
```
==> Build successful! 
==> Starting service with 'gunicorn app:app'
```

## ✅ 部署完成

部署成功后，你会看到：
- **URL**: `https://aram-hongbaoju.onrender.com`（根据你设置的名字）
- 状态：`Live`（绿色）

点击 URL 即可访问你的应用！

## 🔧 常见问题

### 1. 构建失败

**问题**: Build 阶段失败

**解决**:
- 检查 `requirements.txt` 是否正确
- 查看 Build Logs 中的错误信息
- 确保 Python 版本兼容（Render 默认使用 Python 3.9+）

### 2. 应用无法启动

**问题**: Build 成功但服务无法启动

**解决**:
- 检查 Start Command 是否正确：`gunicorn app:app`
- 查看 Live Logs 中的错误信息
- 确保 `app.py` 中应用实例名为 `app`

### 3. 数据库问题

**问题**: 数据库文件丢失

**说明**:
- SQLite 数据库文件存储在 Render 的临时文件系统中
- 免费层重启后数据可能会丢失
- 如果需要持久化数据，考虑升级到付费计划或使用 PostgreSQL

### 4. 应用超时（免费层）

**问题**: 免费层的应用会在 15 分钟无活动后休眠

**说明**:
- 这是 Render 免费层的正常行为
- 首次访问时需要等待 30-60 秒唤醒
- 后续访问会快一些
- 如需 24/7 运行，需要升级到付费计划（$7/月起）

### 5. 修改代码后重新部署

Render 支持自动部署：
- 当你推送代码到 GitHub 的主分支时，Render 会自动重新部署
- 你也可以在 Render 控制台手动点击 **"Manual Deploy"** → **"Deploy latest commit"**

## 📝 部署后的检查清单

- [ ] 应用可以正常访问
- [ ] 可以添加记录
- [ ] 数据库可以正常创建
- [ ] 样式文件正常加载
- [ ] 所有功能正常工作

## 🔗 分享给你的朋友

部署完成后，把你的 Render URL 分享给朋友们，他们就可以使用了！

例如：`https://aram-hongbaoju.onrender.com`

## 💡 后续优化建议

1. **添加自定义域名**：在 Render 设置中配置你的域名
2. **使用 PostgreSQL**：升级数据库以获得更好的持久化
3. **添加健康检查**：创建一个 `/health` 路由
4. **设置自动备份**：定期备份数据库

---

需要帮助？查看 Render 文档：[https://render.com/docs](https://render.com/docs)

