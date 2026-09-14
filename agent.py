import os
import requests
from datetime import datetime
from openai import AzureOpenAI

# From GitHub Actions secrets, we can get the PR number and GitHub token
PR_NUMBER = os.getenv("PR_NUMBER")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
AZURE_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 
AZURE_ENDPOINT = "https://bachero-ai-switzerland.openai.azure.com/"
API_VERSION = "2024-02-15-preview"
DEPLOYMENT_NAME = "gpt-5-mini" 
REPO_SOURCE = "T-ms-code/AplicatieTest"

def obt_diff_pr():
    print(f"Downloading new code from {REPO_SOURCE}, PR #{PR_NUMBER}...")
    url = f"https://api.github.com/repos/{REPO_SOURCE}/pulls/{PR_NUMBER}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error while fetching the differences: {response.status_code}")
        return None

def llm_analyze(diff_text):
    prompt = f"Analyze this new code extracted from a PR. Generate a short paragraph in Romanian explaining what new business logic has been added. Do not provide code, only the logic:\n\n{diff_text}"
    
    if AZURE_OPENAI_API_KEY:
        print("Date go to LLM (Azure OpenAI)...")
        
        try:
            client = AzureOpenAI(
                azure_endpoint=AZURE_ENDPOINT,
                api_key=AZURE_OPENAI_API_KEY,
                api_version=API_VERSION
            )


            response = client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=4000
            )
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error from LLM API: {e}")
            return f"Error from LLM API: {e}"
    else:
        print("No AZURE_OPENAI_API_KEY found!")
        return f"**(No AZURE_OPENAI_API_KEY found!)**\n\n"

def update_documentation(llm_result):
    current_data = datetime.now().strftime("%Y-%m-%d %H:%M")
    content = f"\n\n## Actualizare la {current_data} (Sursa: PR #{PR_NUMBER})\n{llm_result}\n"
    
    with open("docs/business_logic.md", "a", encoding="utf-8") as f:
        f.write(content)
    print("Documentation updated successfully!")

if __name__ == "__main__":
    diff = obt_diff_pr()
    if diff:
        analyze = llm_analyze(diff)
        update_documentation(analyze)