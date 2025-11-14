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

### 步骤 5: 创建 PostgreSQL 数据库（重要！）

为了数据持久化，需要创建一个 PostgreSQL 数据库：

1. 在 Render 控制台，点击 **"New +"** → **"PostgreSQL"**
2. 配置数据库：
   - **Name**: `aram-hongbaoju-db`（或你喜欢的名字）
   - **Database**: `expenses`（或留空使用默认）
   - **User**: 会自动生成
   - **Region**: 选择与 Web Service 相同的区域（推荐）
   - **PostgreSQL Version**: `16`（或最新版本）
   - **Instance Type**: `Free`（免费层有 90 天限制，之后需要付费或迁移）
3. 点击 **"Create Database"**
4. 等待数据库创建完成（1-2 分钟）
5. **重要**：复制数据库的 **"Internal Database URL"** 或 **"External Database URL"**
   - 格式类似：`postgresql://user:password@host:port/dbname`

### 步骤 6: 配置环境变量

在 Web Service 的 **"Environment"** 部分，添加以下环境变量：

1. **DATABASE_URL**（必需）：
   - **Key**: `DATABASE_URL`
   - **Value**: 粘贴刚才复制的数据库 URL
   - 这个变量会让应用自动使用 PostgreSQL 而不是 SQLite

2. **SECRET_KEY**（推荐）：
   - **Key**: `SECRET_KEY`
   - **Value**: 一个随机字符串（例如：`your-secret-key-12345`）
   - 用于 Flask session 加密

> 💡 **提示**：如果使用 Render 的内部数据库 URL，数据库连接会更快且更安全。外部 URL 用于从其他平台访问。

### 步骤 7: 开始部署

1. 点击页面底部的 **"Create Web Service"**
2. Render 会自动开始构建和部署
3. 等待 2-5 分钟（首次部署较慢）

### 步骤 8: 查看部署状态

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

**问题**: 数据库连接失败

**解决**:
- 确保已创建 PostgreSQL 数据库
- 检查 `DATABASE_URL` 环境变量是否正确设置
- 确保数据库和 Web Service 在同一个区域
- 查看 Live Logs 中的错误信息

**问题**: 数据丢失（如果使用 SQLite）

**说明**:
- SQLite 数据库文件存储在 Render 的临时文件系统中
- 免费层重启后数据会丢失
- **解决方案**：使用 PostgreSQL 数据库（见步骤 5），数据会持久保存

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

- [ ] PostgreSQL 数据库已创建并配置
- [ ] `DATABASE_URL` 环境变量已设置
- [ ] 应用可以正常访问
- [ ] 可以添加记录
- [ ] 数据可以正常保存（刷新后数据还在）
- [ ] 样式文件正常加载
- [ ] 所有功能正常工作

## 🎯 数据持久化说明

### 为什么需要 PostgreSQL？

Render 免费层的文件系统是**临时存储**：
- 应用重启或重建时，SQLite 数据库文件会丢失
- 数据无法持久保存

### PostgreSQL 的优势

✅ **数据持久化**：数据存储在独立的数据库中，不会因为应用重启而丢失  
✅ **免费层可用**：Render 提供免费的 PostgreSQL 数据库（90 天试用）  
✅ **性能更好**：适合生产环境  
✅ **自动备份**：Render 会定期备份数据库  

### 免费层限制

- **90 天试用**：免费 PostgreSQL 数据库有 90 天限制
- **到期后**：需要升级到付费计划（$7/月起）或迁移到其他数据库服务
- **替代方案**：可以考虑使用其他免费的 PostgreSQL 服务，如：
  - [Supabase](https://supabase.com)（免费 PostgreSQL）
  - [Railway](https://railway.app)（免费额度）
  - [Neon](https://neon.tech)（免费 PostgreSQL）

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

