# GitHub 热门项目搜索器解析

[TOC]



## 一、项目概述

该项目是一个基于 Flask 框架开发的 GitHub 热门项目搜索与展示工具，通过调用 GitHub API 获取开源项目数据，并提供美观的 Web 界面进行展示和筛选。支持按编程语言、时间范围、排序方式等多维度筛选项目，界面采用 Bootstrap 响应式设计，适配多种设备。

## 二、使用教程

### 1. 环境准备

- 安装依赖包：

```bash
pip install flask requests python-dotenv
```

### 2. 配置 GitHub Token

- 申请 [GitHub Personal Access Token](https://github.com/settings/tokens)（无需特殊权限，仅勾选 `public_repo` 即可）
- 在项目根目录创建 .env 文件，添加以下内容：

```env
GITHUB_TOKEN=your_github_personal_access_token
```

### 3. 启动项目

- 在项目根目录执行命令：

```bash
python app.py
```



- 访问 `http://127.0.0.1:5000` 即可使用

### 4. 功能使用

- **筛选功能**：
  - 语言筛选：支持选择特定编程语言（如 Python、JavaScript 等）
  - 搜索功能：可通过关键词搜索项目名称或描述
  - 排序方式：按星标数、分支数或更新时间排序
  - 时间范围：可查看今日、本周、本月的热门项目
  - 项目数量：可选择每页显示 15/30/50 个项目
- **交互体验**：
  - 点击项目标题可直接跳转到 GitHub 项目页面
  - 鼠标悬浮在项目卡片上会有 "上浮 + 阴影" 动画效果
  - 项目描述过长时会自动截断（最多显示 3 行）

## 三、功能亮点

1. **多维度筛选**：提供丰富的筛选条件，满足不同用户的搜索需求
2. **响应式设计**：页面在手机、平板、电脑等设备上均可正常显示
3. **视觉交互**：项目卡片悬停效果提升用户体验
4. **数据格式化**：清晰展示项目星标数、分支数、更新时间等关键信息
5. **错误处理**：包含 API 调用频率超限等错误提示

## 四、扩展建议

1. **分页功能**：当前仅支持单页展示，可通过 GitHub API 的 `page` 参数实现多页加载
2. **项目分类标签**：根据项目功能（如 "工具类"、"游戏"、"AI 相关"）添加标签筛选
3. **收藏功能**：使用本地存储（LocalStorage）记录用户收藏的项目
4. **暗色模式**：基于 Bootstrap 的暗色主题，添加切换按钮
5. **邮件订阅**：定期向用户发送热门项目汇总（需集成邮件服务，如 Flask-Mail）

## 五、注意事项

- **API 调用限制**：未使用 Token 时，GitHub API 每小时仅允许 60 次请求；使用 Token 后可提升至 5000 次 / 小时，建议务必配置 Token
- **开发环境提示**：脚本中 `debug=True` 仅用于开发，生产环境部署时需关闭，并使用 Gunicorn 等 WSGI 服务器
- **界面适配**：页面采用响应式设计，在手机、平板、电脑上均可正常显示







# 部署 GitHub 热点项目搜索器到服务器

## 一、准备工作

1. **服务器要求**：
   - 推荐使用 Ubuntu 20.04/22.04 系统
   - 安装 Python 3.8+、pip、git
   - 开放 80/443 端口（用于 web 访问）
2. **安装基础依赖**：

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git nginx
```

## 二、部署步骤

### 1. 克隆项目代码

```bash
# 克隆代码到服务器（假设使用 GitHub 仓库）
git clone <你的项目仓库地址>
cd github热点项目搜索器
```

### 2. 配置虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装项目依赖
pip install flask requests python-dotenv gunicorn
```

### 3. 配置环境变量

确保 .env 文件已正确配置（已包含 `GITHUB_TOKEN`），如果没有则创建：

```bash
# 编辑 .env 文件
nano .env

# 确保内容正确
GITHUB_TOKEN=你的GitHub令牌
```

### 4. 配置 Gunicorn 服务

创建 systemd 服务文件以管理应用：

```bash
sudo nano /etc/systemd/system/github-trending.service
```

```ini
[Unit]
Description=GitHub Trending Projects Service
After=network.target

[Service]
User=ubuntu  # 替换为你的服务器用户名
WorkingDirectory=/home/ubuntu/github热点项目搜索器  # 替换为项目路径
ExecStart=/home/ubuntu/github热点项目搜索器/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

启动并设置开机自启：

```bash
sudo systemctl start github-trending
sudo systemctl enable github-trending
```

### 5. 配置 Nginx 反向代理

```bash
sudo nano /etc/nginx/sites-available/github-trending
```

添加以下配置：

```nginx
server {
    listen 80;
    server_name 你的域名或服务器IP;  # 替换为实际域名或IP

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```



启用站点配置：

```bash
sudo ln -s /etc/nginx/sites-available/github-trending /etc/nginx/sites-enabled/
sudo nginx -t  # 测试配置是否正确
sudo systemctl restart nginx
```



## 三、安全配置

1. **防火墙设置**：

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw enable
```

1. **获取 SSL 证书（推荐）**：
   使用 Let's Encrypt 配置 HTTPS：

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d 你的域名
```

## 四、维护命令

- 查看应用状态：`sudo systemctl status github-trending`
- 重启应用：`sudo systemctl restart github-trending`
- 查看日志：`sudo journalctl -u github-trending -f`
- 更新代码后重启：`git pull && sudo systemctl restart github-trending`

## 五、注意事项

1. 生产环境中需在 app.py 中关闭 debug 模式：`app.run(debug=False)`
2. 定期更新依赖包：`pip install --upgrade flask requests gunicorn`
3. 监控服务器资源使用情况，根据流量调整 Gunicorn 工作进程数（`-w` 参数）





# 将 GitHub 热点项目搜索器部署到 Vercel

Vercel 是一个适合部署前端和轻量级后端应用的平台，对 Flask 等 Python 应用有良好支持。以下是部署步骤：

## 一、准备工作

1. 将项目代码推送到 GitHub 仓库（确保包含所有必要文件：app.py、templates/index.html、.env 等）
2. 注册 / 登录 [Vercel](https://vercel.com/) 账号，并关联你的 GitHub 账号

## 二、配置项目

### 1. 添加 Vercel 配置文件

在项目根目录创建 `vercel.json` 文件，指定 Python 运行环境和入口：

```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### 2. 调整 Flask 应用（关键）

Vercel 要求应用监听特定端口，修改 app.py 的启动部分：

```python
if __name__ == "__main__":
    # 生产环境使用 Vercel 提供的端口
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)  # 务必关闭 debug 模式
```

### 3. 处理环境变量

1. 在 Vercel 部署时，不要将 .env 文件提交到仓库（避免泄露 Token）
2. 部署时在 Vercel 控制台手动添加环境变量：
   - 变量名：`GITHUB_TOKEN`
   - 变量值：你的 GitHub 令牌（与 .env 中一致）

## 三、部署步骤

1. **导入项目**：
   - 登录 Vercel 后，点击 "New Project"
   - 选择你的 GitHub 仓库（确保仓库已公开或你已授权 Vercel 访问私有仓库）
2. **配置部署**：
   - 框架预设：选择 "Other"
   - 环境变量：点击 "Add Environment Variable"，添加 `GITHUB_TOKEN`
   - 其他设置保持默认
3. **开始部署**：
   - 点击 "Deploy" 按钮，Vercel 会自动：
     - 检测 Python 环境
     - 安装依赖（`flask`、`requests` 等）
     - 部署应用并分配临时域名
4. **访问应用**：
   - 部署完成后，Vercel 会显示应用 URL（格式类似 `https://xxx.vercel.app`）
   - 点击 URL 即可访问你的 GitHub 热点项目搜索器

## 四、注意事项

1. **依赖管理**：

   - 建议创建 `requirements.txt` 文件列出所有依赖，确保 Vercel 正确安装：

   txt

   ```txt
   flask==2.3.3
   requests==2.31.0
   python-dotenv==1.0.0
   ```

2. **API 访问限制**：

   - Vercel 部署的应用可能会有 IP 变化，确保 GitHub Token 配置正确以避免 API 调用限制

3. **HTTPS 支持**：

   - Vercel 自动为应用配置 HTTPS，无需额外设置

4. **更新部署**：

   - 后续代码更新只需推送到 GitHub 仓库，Vercel 会自动检测并重新部署

5. **功能兼容性**：

   - 如果项目中有本地文件存储（如收藏功能的 `saved_projects.json`），Vercel 的文件系统是临时的，数据会在部署后重置，建议改用数据库或外部存储服务