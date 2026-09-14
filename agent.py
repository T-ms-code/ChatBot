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
REPO_SOURCE = "T-ms-code/TestApplication" 

def get_pr_diff():
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
    prompt = f"""Analyze this git diff from a Pull Request.
Identify the new business logic.
You MUST RESPOND STRICTLY in Romanian using the following format and tags (do not write anything else outside this format):

SHORT_TITLE: [Write a 3-5 word title in Romanian here, e.g., Adaugare validare impartire la zero]
SHORT_DESCRIPTION: [Write a single clear sentence in Romanian about what changed]
MD_CONTENT: 
[Write the detailed explanation in Markdown format here, in Romanian. Use bullet points for identified business rules. Use bold for important variables or decisions. Do not add an H1 title here, start directly with H2 (##) or lists.]

The modified code is:
{diff_text}
"""
    
    if AZURE_OPENAI_API_KEY:
        print("Data goes to LLM (Azure OpenAI)...")
        
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
        print("No AZURE_OPENAI_API_KEY found! Using fallback simulation.")
        return "SHORT_TITLE: Simulare Actualizare\nSHORT_DESCRIPTION: Aceasta este o simulare detaliată fară cheie API.\nMD_CONTENT: \n## Reguli adăugate\n* Simulare de proces finalizată cu succes."

def parse_llm_response(text):
    title = f"Update_PR_{PR_NUMBER}"
    description = "O noua modificare a logicii de business a fost adaugată."
    content = text

    try:
        if "SHORT_TITLE:" in text and "MD_CONTENT:" in text:
            title = text.split("SHORT_TITLE:")[1].split("SHORT_DESCRIPTION:")[0].strip()
            description = text.split("SHORT_DESCRIPTION:")[1].split("MD_CONTENT:")[0].strip()
            content = text.split("MD_CONTENT:")[1].strip()
    except Exception as e:
        print("Warning: LLM formatting failed. Using fallback parsing.")
        
    return title, description, content

def update_documentation(short_title, short_description, md_content):
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 1. Create a NEW FILE for this specific update
    clean_filename = "".join(x for x in short_title if x.isalnum() or x in " ").replace(" ", "_").lower()
    file_name = f"pr_{PR_NUMBER}_{clean_filename}.md"
    new_file_path = f"docs/{file_name}"
    
    with open(new_file_path, "w", encoding="utf-8") as f_new:
        f_new.write(f"# Detalii: {short_title}\n\n")
        f_new.write(md_content)
        f_new.write(f"\n\n---\n*Acest document a fost generat automat de AI la data de {current_datetime} (Sursa: PR #{PR_NUMBER}).*")
        
    # 2. Update the ROOT file (business_logic.md) like a TREE (add path only)
    root_entry = f"* **[{current_date}] {short_description}** \n  * -> [Explorează detaliile logicii](./{file_name})\n"
    
    with open("docs/business_logic.md", "a", encoding="utf-8") as f_root:
        f_root.write(root_entry)
        
    print(f"Documentation updated successfully as a tree! New file created: {file_name}")

if __name__ == "__main__":
    diff = get_pr_diff()
    if diff:
        raw_response = llm_analyze(diff)
        title, desc, content = parse_llm_response(raw_response)
        update_documentation(title, desc, content)