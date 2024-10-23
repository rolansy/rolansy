import os
from github import Github
from collections import Counter

# Authenticate to GitHub
g = Github(os.getenv('GITHUB_TOKEN'))
username = os.getenv('GITHUB_USERNAME')

# Get user
user = g.get_user(username)

# Get all repositories
repos = user.get_repos()

# Count languages
language_counter = Counter()
for repo in repos:
    languages = repo.get_languages()
    for language, bytes_of_code in languages.items():
        language_counter[language] += bytes_of_code

# Get top languages
top_languages = language_counter.most_common(5)

# Generate README content
readme_content = "## Top Languages\n\n"
for language, bytes_of_code in top_languages:
    percentage = (bytes_of_code / sum(language_counter.values())) * 100
    readme_content += f"- **{language}** - {percentage:.2f}%\n"

# Update README.md
with open("README.md", "r") as file:
    readme_lines = file.readlines()

start_index = readme_lines.index("## Top Languages\n")
end_index = start_index + 1
while end_index < len(readme_lines) and readme_lines[end_index].startswith("-"):
    end_index += 1

new_readme_lines = readme_lines[:start_index + 1] + readme_content.splitlines(keepends=True) + readme_lines[end_index:]

with open("README.md", "w") as file:
    file.writelines(new_readme_lines)
