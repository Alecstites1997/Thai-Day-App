import os
import json
import base64
from github import Github

def get_access_token():
    # Replit Connectors provide access tokens via environment variables or identity token
    # For GitHub connector, we can fetch it from the Replit API
    import requests
    hostname = os.environ.get('REPLIT_CONNECTORS_HOSTNAME')
    x_replit_token = os.environ.get('REPL_IDENTITY')
    
    if not x_replit_token:
        # Fallback for deployment environments
        x_replit_token = os.environ.get('WEB_REPL_RENEWAL')
    
    if not x_replit_token:
        raise Exception("Authentication token not found")

    response = requests.get(
        f'https://{hostname}/api/v2/connection?include_secrets=true&connector_names=github',
        headers={
            'Accept': 'application/json',
            'X-Replit-Token': f"repl {x_replit_token}" if os.environ.get('REPL_IDENTITY') else f"depl {x_replit_token}"
        }
    )
    data = response.json()
    item = data.get('items', [{}])[0]
    settings = item.get('settings', {})
    token = settings.get('access_token') or settings.get('oauth', {}).get('credentials', {}).get('access_token')
    
    if not token:
        raise Exception("GitHub access token not found in connector settings")
    return token

def push_to_github():
    try:
        token = get_access_token()
        g = Github(token)
        user = g.get_user()
        
        repo_name = "thai-day-orders"
        try:
            repo = user.get_repo(repo_name)
            print(f"Found existing repo: {repo_name}")
        except:
            print(f"Creating new repo: {repo_name}")
            repo = user.create_repo(repo_name, private=True)

        files_to_push = [
            "main.py",
            "templates/index.html",
            "templates/thanks.html",
            "templates/admin.html",
            "templates/locked.html",
            "pyproject.toml"
        ]

        for file_path in files_to_push:
            if not os.path.exists(file_path):
                continue
                
            with open(file_path, 'r') as f:
                content = f.read()
            
            try:
                contents = repo.get_contents(file_path)
                repo.update_file(contents.path, f"Update {file_path}", content, contents.sha)
                print(f"Updated {file_path}")
            except:
                repo.create_file(file_path, f"Add {file_path}", content)
                print(f"Created {file_path}")
        
        print("Successfully pushed all changes to GitHub!")
        return True
    except Exception as e:
        print(f"Error pushing to GitHub: {e}")
        return False

if __name__ == "__main__":
    push_to_github()
