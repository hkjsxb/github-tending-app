import os
import requests
import csv
from datetime import datetime, timedelta
from flask import Flask, render_template, request, make_response
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 配置
GITHUB_API_URL = "https://api-github-com.hkjsxb.com/search/repositories"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# 设置请求头，包含认证信息
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {GITHUB_TOKEN}"
}

# 常见编程语言列表
COMMON_LANGUAGES = [
    "", "Python", "JavaScript", "Java", "C++", "C", "C#", "Ruby", 
    "Go", "Swift", "Kotlin", "PHP", "TypeScript", "Rust", "Objective-C"
]

def get_trending_repos(sort_by="stars", period="weekly", language=None, per_page=30, search=None):
    """获取GitHub热门项目，支持搜索功能"""
    # 计算时间范围
    period_map = {"daily": 1, "weekly": 7, "monthly": 30}
    since_date = (datetime.now() - timedelta(days=period_map[period])).strftime("%Y-%m-%d")

    # 构建查询参数
    query_parts = [f"created:>{since_date}"]
    
    if language:
        query_parts.append(f"language:{language}")
    
    # 处理搜索关键词，支持空格分隔的多关键词
    if search and search.strip():
        search_terms = search.strip().split()
        query_parts.append(" ".join([f'"{term}"' for term in search_terms]))
    
    query = " ".join(query_parts)

    params = {
        "q": query,
        "sort": sort_by,
        "order": "desc",
        "per_page": per_page
    }

    try:
        response = requests.get(
            GITHUB_API_URL,
            headers=HEADERS,
            params=params,
            verify=True
        )
        response.raise_for_status()
        repos_data = response.json()["items"]

        # 格式化项目数据
        formatted_repos = []
        for repo in repos_data:
            formatted_repos.append({
                "name": repo["name"],
                "full_name": repo["full_name"],
                "owner_login": repo["owner"]["login"],
                "url": repo["html_url"],
                "description": repo["description"] or "无描述",
                "stars": f"{repo['stargazers_count']:,}",
                "forks": f"{repo['forks_count']:,}",
                "language": repo["language"] or "未知",
                "updated_at": datetime.strptime(
                    repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ"
                ).strftime("%Y-%m-%d"),
                "owner_avatar": repo["owner"]["avatar_url"]
            })
        return formatted_repos, None

    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            return [], "API调用频率超限，请稍后再试"
        return [], f"HTTP错误: {e}"
    except Exception as e:
        return [], f"数据获取失败: {str(e)}"

@app.route("/")
def index():
    # 获取请求参数
    sort_by = request.args.get("sort", "stars")
    period = request.args.get("period", "weekly")
    language = request.args.get("language", "")
    per_page = int(request.args.get("per_page", 30))
    search = request.args.get("search", "")

    # 获取热门项目
    repos, error = get_trending_repos(sort_by, period, language, per_page, search)

    # 渲染模板
    return render_template(
        "index.html",
        repos=repos,
        error=error,
        common_languages=COMMON_LANGUAGES,
        current_sort=sort_by,
        current_period=period,
        current_language=language,
        current_search=search
    )



if __name__ == "__main__":
    # 生产环境使用 Vercel 提供的端口
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)  # 务必关闭 debug 模式
