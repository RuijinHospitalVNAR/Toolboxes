# Deployment Guide

This guide explains how to deploy the Toolboxes repository to GitHub Pages.

## Prerequisites

1. GitHub account: [RuijinHospitalVNAR](https://github.com/RuijinHospitalVNAR)
2. Git installed on your local machine
3. Access to the repository

## Step 1: Create the Repository on GitHub

1. Go to https://github.com/RuijinHospitalVNAR
2. Click "New repository"
3. Name it: `Toolboxes`
4. Set it to Public
5. Do NOT initialize with README, .gitignore, or license
6. Click "Create repository"

## Step 2: Initialize Local Repository

```bash
# Navigate to the project root directory
cd "F:\文章投递内容\2025\VLPIM\脚本"

# Initialize git repository (if not already done)
git init

# Add remote repository
git remote add origin https://github.com/RuijinHospitalVNAR/Toolboxes.git

# Or if using SSH:
# git remote add origin git@github.com:RuijinHospitalVNAR/Toolboxes.git
```

## Step 3: Prepare Files for Commit

```bash
# Add all necessary files
git add README.md
git add index.html
git add VLPIM_Web_services/
git add .github/

# Check what will be committed
git status
```

## Step 4: Commit and Push

```bash
# Commit changes
git commit -m "Initial commit: Add VLPIM Web Services tool"

# Push to GitHub (use main branch for GitHub Pages)
git branch -M main
git push -u origin main
```

## Step 5: Enable GitHub Pages

1. Go to repository settings: https://github.com/RuijinHospitalVNAR/Toolboxes/settings
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select:
   - Branch: `main`
   - Folder: `/ (root)`
4. Click "Save"
5. Wait a few minutes for GitHub to build and deploy

## Step 6: Access Your Site

Your site will be available at:
- **Main page**: https://ruijinhospitalvnar.github.io/Toolboxes/
- **VLPIM Web Services**: https://ruijinhospitalvnar.github.io/Toolboxes/VLPIM_Web_services/

## Future Updates

To update the site:

```bash
# Make changes to files
# Then:
git add .
git commit -m "Update: Description of changes"
git push origin main
```

GitHub Pages will automatically rebuild and deploy within a few minutes.

## Adding More Tools

When adding new tools:

1. Create a new directory: `ToolName/`
2. Add `index.html` in that directory
3. Update root `index.html` to include the new tool
4. Update root `README.md`
5. Commit and push

## Troubleshooting

- **Pages not loading**: Check GitHub Actions tab for build errors
- **404 errors**: Ensure file paths are correct (case-sensitive)
- **CSS/JS not loading**: Check CDN links are accessible
- **Large files**: GitHub Pages has size limits; consider using Git LFS for large files

