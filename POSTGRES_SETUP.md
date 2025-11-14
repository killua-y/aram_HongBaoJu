# PostgreSQL 数据库设置指南

## 🎯 为什么需要 PostgreSQL？

Render 免费层的文件系统是**临时存储**，应用重启或重建时，SQLite 数据库文件会丢失。使用 PostgreSQL 数据库可以确保数据持久保存。

## 📋 快速设置步骤

### 1. 在 Render 创建 PostgreSQL 数据库

1. 登录 [Render](https://render.com)
2. 点击 **"New +"** → **"PostgreSQL"**
3. 配置数据库：
   - **Name**: `aram-hongbaoju-db`（或你喜欢的名字）
   - **Region**: 选择与 Web Service 相同的区域（推荐）
   - **PostgreSQL Version**: `16`（或最新版本）
   - **Instance Type**: `Free`（免费层）
4. 点击 **"Create Database"**
5. 等待创建完成（1-2 分钟）

### 2. 获取数据库连接 URL

数据库创建完成后：

1. 进入数据库详情页面
2. 找到 **"Connections"** 部分
3. 复制 **"Internal Database URL"**（推荐，用于 Render 内部连接）
   - 格式：`postgresql://user:password@host:port/dbname`

### 3. 配置环境变量

在你的 Web Service 中：

1. 进入 Web Service 设置
2. 找到 **"Environment"** 部分
3. 添加环境变量：
   - **Key**: `DATABASE_URL`
   - **Value**: 粘贴刚才复制的数据库 URL
4. 保存更改

### 4. 重新部署应用

1. 在 Render 控制台，点击 **"Manual Deploy"** → **"Deploy latest commit"**
2. 或者推送代码到 GitHub，Render 会自动重新部署

## ✅ 验证设置

部署完成后：

1. 访问你的应用
2. 添加一条记录
3. 刷新页面，数据应该还在
4. 等待一段时间后再次访问，数据应该仍然存在

## 🔧 工作原理

应用会自动检测 `DATABASE_URL` 环境变量：

- **有 `DATABASE_URL`**：使用 PostgreSQL 数据库（生产环境）
- **没有 `DATABASE_URL`**：使用 SQLite 数据库（本地开发）

这样你可以：
- 本地开发使用 SQLite（简单快速）
- 生产环境使用 PostgreSQL（数据持久化）

## ⚠️ 注意事项

### 免费层限制

- Render 免费 PostgreSQL 数据库有 **90 天试用期**
- 到期后需要升级到付费计划（$7/月起）或迁移数据

### 替代方案

如果不想付费，可以考虑：

1. **Supabase**：提供免费的 PostgreSQL 数据库
   - 网址：https://supabase.com
   - 免费层：500 MB 存储，2 GB 带宽

2. **Neon**：免费的 PostgreSQL 数据库
   - 网址：https://neon.tech
   - 免费层：3 GB 存储

3. **Railway**：提供免费额度
   - 网址：https://railway.app
   - 免费层：$5 额度/月

## 📝 迁移到其他数据库服务

如果你想把数据库迁移到其他服务：

1. 在 Render 导出数据库（使用 pg_dump）
2. 在新服务创建数据库
3. 导入数据
4. 更新 Web Service 的 `DATABASE_URL` 环境变量

## 🆘 遇到问题？

1. **数据库连接失败**：
   - 检查 `DATABASE_URL` 是否正确
   - 确保数据库和 Web Service 在同一个区域
   - 查看应用日志中的错误信息

2. **数据丢失**：
   - 确保使用的是 PostgreSQL，不是 SQLite
   - 检查环境变量是否正确设置
   - 查看数据库中的数据是否存在

3. **应用无法启动**：
   - 检查 `requirements.txt` 中是否包含 `psycopg2-binary`
   - 查看构建日志中的错误信息

---

需要更多帮助？查看 [DEPLOY.md](./DEPLOY.md) 获取完整的部署指南。

