# GitHub Pages Setup - Quick Start

Follow these steps to deploy your website to GitHub Pages.

## Step 1: Enable GitHub Pages

1. Go to your repository on GitHub: `https://github.com/AIwithApex/Ultimate-Agent-Directory`
2. Click **Settings** (top navigation)
3. Scroll down and click **Pages** (left sidebar)
4. Under **Source**, select:
   - **Source**: GitHub Actions
5. Save (if prompted)

## Step 2: Verify Workflow Permissions

1. Still in **Settings**, click **Actions** > **General** (left sidebar)
2. Scroll to **Workflow permissions**
3. Select: **Read and write permissions**
4. Check: **Allow GitHub Actions to create and approve pull requests**
5. Click **Save**

## Step 3: Push Changes to Trigger Deployment

```bash
# Stage all changes
git add .

# Commit with a clear message
git commit -m "Add website generation and GitHub Pages deployment"

# Push to main branch
git push origin main
```

## Step 4: Monitor Deployment

1. Go to the **Actions** tab in your repository
2. You should see "Build and Deploy to GitHub Pages" workflow running
3. Wait for it to complete (usually 2-3 minutes)
4. Look for a green checkmark ✓

## Step 5: Visit Your Website

After successful deployment, your site will be live at:

```
https://aiwithapex.github.io/Ultimate-Agent-Directory/
```

## What Happens Automatically

Every time you push to `main`:
- ✓ Validates all YAML files
- ✓ Generates README.md
- ✓ Generates static website
- ✓ Deploys to GitHub Pages

## Pull Request Validation

When someone opens a pull request:
- ✓ Validates YAML syntax
- ✓ Tests README generation
- ✓ Tests website generation
- ✓ Shows pass/fail status

## Troubleshooting

### Workflow Fails
- Check the Actions tab for error logs
- Common issue: Workflow permissions not set correctly

### Website Not Updating
- Wait 1-2 minutes after deployment completes
- Clear browser cache (Ctrl+F5 or Cmd+Shift+R)
- Check Actions tab to verify deployment succeeded

### 404 Error
- Verify GitHub Pages is enabled in Settings > Pages
- Ensure Source is set to "GitHub Actions"
- Check that workflow completed successfully

## Manual Trigger (if needed)

You can manually trigger deployment:
1. Go to **Actions** tab
2. Click "Build and Deploy to GitHub Pages"
3. Click **Run workflow** button
4. Select branch: `main`
5. Click **Run workflow**

## Next Steps

Once deployed, share your website:
- Add the URL to your repository description
- Update your README with the live link
- Share on social media, Reddit, HackerNews, etc.

## Custom Domain (Optional)

Want to use your own domain like `agents.aiwithapex.com`?

See `docs/DEPLOYMENT.md` for custom domain setup instructions.
