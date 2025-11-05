# GitHub Pages Deployment Guide

The Ultimate Agent Directory website is automatically deployed to GitHub Pages using GitHub Actions.

## Automatic Deployment

Every push to the `main` branch triggers:
1. YAML validation
2. README generation
3. Website generation
4. Deployment to GitHub Pages

The workflow is defined in `.github/workflows/deploy.yml`.

## Initial Setup

### 1. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** > **Pages**
3. Under **Source**, select:
   - Source: **GitHub Actions**
4. Save the settings

### 2. Verify Workflow Permissions

1. Go to **Settings** > **Actions** > **General**
2. Under **Workflow permissions**, ensure:
   - "Read and write permissions" is selected
   - "Allow GitHub Actions to create and approve pull requests" is checked
3. Save changes

### 3. First Deployment

Push to `main` branch or manually trigger the workflow:

```bash
git add .
git commit -m "Enable GitHub Pages deployment"
git push origin main
```

Or trigger manually:
1. Go to **Actions** tab
2. Select "Build and Deploy to GitHub Pages"
3. Click **Run workflow**

## Website URL

After deployment, your site will be available at:

```
https://<username>.github.io/<repository-name>/
```

For this repository:
```
https://aiwithapex.github.io/Ultimate-Agent-Directory/
```

## Workflow Details

### Build Job
- Validates all YAML files
- Generates README.md
- Generates static website in `_site/`
- Uploads artifact for deployment

### Deploy Job
- Deploys `_site/` contents to GitHub Pages
- Updates the live website

## Manual Deployment

You can also build and deploy manually:

```bash
# Build site locally
make site

# The _site/ directory is ready for deployment
# GitHub Actions will handle the actual deployment
```

## Validation on Pull Requests

Pull requests automatically run validation checks (`.github/workflows/validate.yml`):
- YAML syntax validation
- Schema validation with Pydantic
- Test README generation
- Test website generation
- Check for duplicates

PRs must pass all checks before merging.

## Troubleshooting

### Build Fails

Check the Actions tab for detailed logs. Common issues:

1. **YAML validation errors**: Fix syntax in YAML files
2. **Missing dependencies**: Ensure `requirements.txt` is up to date
3. **Python version**: Workflow uses Python 3.11

### Website Not Updating

1. Check Actions tab - ensure workflow completed successfully
2. Clear browser cache
3. Wait 1-2 minutes for CDN propagation
4. Verify GitHub Pages is enabled in Settings

### Permissions Error

Ensure workflow has correct permissions in repository settings:
- Settings > Actions > General > Workflow permissions

## Custom Domain (Optional)

To use a custom domain:

1. Add a `CNAME` file to `static/` directory:
   ```
   agents.yourdomain.com
   ```

2. Update DNS records with your domain provider:
   - Add CNAME record pointing to: `<username>.github.io`

3. Enable HTTPS in GitHub Pages settings

4. Update base URL in `scripts/generate_site.py`:
   ```python
   base_url = "https://agents.yourdomain.com"
   ```

## Monitoring

Monitor deployments:
- **Actions tab**: See build/deploy status
- **Environments**: See deployment history
- **Pages settings**: See current deployment URL

## Related Files

- `.github/workflows/deploy.yml` - Deployment workflow
- `.github/workflows/validate.yml` - PR validation workflow
- `scripts/generate_site.py` - Website generator
- `_site/` - Generated website (not committed to git)
