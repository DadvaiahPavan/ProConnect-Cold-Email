import requests
from bs4 import BeautifulSoup
import csv
import re

def scrape_github_repos(username):
    url = f'https://github.com/{username}?tab=repositories'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    repos = []
    for repo in soup.find_all('article', class_='Box-row'):
        repo_name = repo.find('h3', class_='wb-break-all').text.strip()
        repo_link = f'https://github.com/{username}/{repo_name}'
        
        # Try to extract technologies from repo name or description
        tech_stack = []
        repo_desc = repo.find('p', class_='col-9')
        if repo_desc:
            desc_text = repo_desc.text.strip().lower()
            
            # Common technology keywords
            tech_keywords = {
                'python': 'Python',
                'react': 'React',
                'django': 'Django',
                'flask': 'Flask',
                'javascript': 'JavaScript',
                'node': 'Node.js',
                'machine learning': 'Machine Learning',
                'ai': 'AI',
                'tensorflow': 'TensorFlow',
                'keras': 'Keras',
                'streamlit': 'Streamlit'
            }
            
            # Find matching technologies
            found_techs = [tech for keyword, tech in tech_keywords.items() if keyword in desc_text]
            tech_stack = found_techs if found_techs else ['Various Technologies']
        
        repos.append({
            'TechStack': ', '.join(tech_stack),
            'Links': repo_link
        })
    
    return repos

def update_portfolio_csv(repos):
    csv_path = 'c:/Users/pavan/OneDrive/Desktop/test/ProConnect: AI-Powered Cold Email Creator/my_portfolio.csv'
    
    # Read existing CSV
    with open(csv_path, 'r', newline='', encoding='utf-8') as file:
        existing_rows = list(csv.DictReader(file))
    
    # Combine existing rows with new GitHub repos
    updated_rows = existing_rows + repos
    
    # Write updated CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['Techstack', 'Links']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in updated_rows:
            writer.writerow({
                'Techstack': row.get('TechStack', ''),
                'Links': row.get('Links', '')
            })

def main():
    github_username = 'DadvaiahPavan'
    repos = scrape_github_repos(github_username)
    update_portfolio_csv(repos)
    print(f"Updated portfolio CSV with {len(repos)} GitHub repositories.")

if __name__ == '__main__':
    main()
