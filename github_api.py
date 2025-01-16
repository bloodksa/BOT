import aiohttp
import base64

async def search_github_repos(query: str, limit: int = 5):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.github.com/search/repositories?q={query}+language:python+topic:telegram-bot&sort=stars&order=desc"
        async with session.get(url) as response:
            data = await response.json()
            return data['items'][:limit]

async def get_repo_content(repo_full_name: str, file_path: str):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.github.com/repos/{repo_full_name}/contents/{file_path}"
        async with session.get(url) as response:
            data = await response.json()
            if 'content' in data:
                return base64.b64decode(data['content']).decode('utf-8')
            return None

