# create_repo.ps1 — initialize local repo and push to GitHub (public)
param(
  [string]$RepoName = "laeda-efm-prompt-pack",
  [string]$GitUser = "Arseny Perel",
  [string]$GitEmail = "arielperseny@gmail.com"
)

git --version | Out-Null
gh --version | Out-Null

git config --global user.name "$GitUser"
git config --global user.email "$GitEmail"

git init
git add .
git commit -m "Initial public highlights (prompts + checklists + examples)"
gh auth login --web --scopes "repo"
gh repo create $RepoName --public --source=. --remote=origin --push
