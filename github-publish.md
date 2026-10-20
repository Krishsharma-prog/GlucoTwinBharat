# Publish to GitHub

A GitHub repository has not been created automatically by this package. After creating a **public** empty repository in your own GitHub account, open a terminal in the project root and run:

```bash
git init
git add .
git commit -m "Initial GlucoTwin Bharat Digital Twin proof of concept"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/glucotwin-bharat.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your account name and use the exact remote URL GitHub shows you. Do not commit secrets, account tokens, private contact details, or real patient data. Confirm the repo is public and the README, architecture PDFs, presentation, and demo link open without authentication.
