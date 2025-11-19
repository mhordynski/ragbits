# Migration Guide: Trunk-Based Development

This document explains the migration from the old `develop`/`main` branching strategy to the new trunk-based development workflow.

## What Changed?

### Old Strategy (Git-Flow)
- **`develop`** - Development and nightly builds
- **`main`** - Stable releases only
- Developers had to remember to target `develop` for PRs
- Auto-rebase workflow moved PRs from `main` to `develop`

### New Strategy (Trunk-Based)
- **`main`** - Single branch for all development and nightly builds
- Stable releases are created via PR from `main` → merge → tag
- Hotfixes are patch releases following the same pattern
- No branch confusion - always work on `main`

## Benefits

✅ **Simpler workflow** - One branch to rule them all
✅ **No confusion** - Developers always target `main`
✅ **Faster releases** - No complex merge/sync workflows
✅ **Industry standard** - Used by Google, Facebook, and most modern projects
✅ **Clear README** - Front page shows `main` (which includes nightly instructions)

## Migration Steps

### For Repository Maintainers

1. **Merge `develop` into `main` (if needed)**
   ```bash
   git checkout main
   git pull origin main
   git merge origin/develop
   git push origin main
   ```

2. **Update GitHub repository settings**
   - Go to repository Settings → Branches
   - Ensure `main` is the default branch
   - Update branch protection rules for `main` if needed

3. **Delete `develop` branch (optional, after transition)**
   ```bash
   git push origin --delete develop
   git branch -d develop
   ```

4. **Communicate the change**
   - Notify all contributors about the new workflow
   - Update any external documentation
   - Close/rebase any open PRs targeting `develop`

### For Contributors

1. **Update your local repository**
   ```bash
   # Fetch latest changes
   git fetch origin

   # Switch to main
   git checkout main
   git pull origin main

   # Delete local develop branch (optional)
   git branch -d develop
   ```

2. **Update existing feature branches**
   ```bash
   # If you have a feature branch targeting develop
   git checkout your-feature-branch
   git rebase main
   git push --force-with-lease origin your-feature-branch
   ```

3. **Create new PRs targeting `main`**
   - All new PRs should target `main`
   - No more manual base branch changes needed

## New Release Workflow

### Creating a Stable Release

1. Go to **Actions** → **Stable Release**
2. Click **Run workflow**
3. Select version type: **major** or **minor**
4. Review the auto-generated PR
5. Merge the PR
6. Release is automatically tagged and published to PyPI

### Creating a Hotfix (Patch Release)

1. Go to **Actions** → **Patch Release (Hotfix)**
2. Click **Run workflow**
3. Enter a brief description of the fix
4. Review the auto-generated PR
5. Merge the PR
6. Hotfix is automatically tagged and published to PyPI

### Nightly Builds

- **Automatic**: Built daily from `main` at 2 AM UTC
- **Install**: `pip install ragbits --pre`
- **Version format**: `X.Y.Z.devYYYYMMDDHHMM`

## Workflows Reference

### New Workflows
- **`release-stable.yml`** - Creates PR for stable (major/minor) releases
- **`release-stable-publish.yml`** - Auto-publishes after release PR merge
- **`release-patch.yml`** - Creates PR for hotfix (patch) releases
- **`update-readme-stable.yml`** - Updates README after stable release

### Updated Workflows
- **`nightly-build.yml`** - Now builds from `main` instead of `develop`

### Removed Workflows
- **`pull-request-change-base-branch.yml`** - No longer needed (no auto-rebasing)
- **`sync-develop-after-release.yml`** - No longer needed (no develop branch)

### Deprecated Workflows
- **`prepare-release.yml`** - Old individual package releases (use `release-stable.yml` instead)
- **`publish-pypi.yml`** - Old publish workflow (use `release-stable-publish.yml` instead)

## FAQ

### Q: What happens to the `develop` branch?
**A:** It can be safely deleted after all in-flight PRs are merged or rebased to `main`. However, you can keep it temporarily during the transition period.

### Q: Where do nightly builds come from now?
**A:** Nightly builds are published from the `main` branch every day at 2 AM UTC.

### Q: How do I create a hotfix for a critical bug?
**A:** Use the "Patch Release (Hotfix)" workflow. It will bump the patch version, create a PR, and after merge, automatically publish.

### Q: Can I still release individual packages?
**A:** The new workflow releases all packages together with the same version. This ensures consistency and simplifies dependency management. Individual package releases are deprecated.

### Q: What if `main` has unreleased changes and I need a hotfix?
**A:**
- **Option 1** (Recommended): Include the unreleased changes in the hotfix and do a patch release
- **Option 2**: Create a release branch from the last stable tag, cherry-pick the fix, and manually release

### Q: How do I handle long-running feature branches?
**A:** Keep them short-lived. Merge frequently to `main` behind feature flags if needed. This is the core principle of trunk-based development.

### Q: What about the README on the front page?
**A:** The `main` branch README includes both stable and nightly installation instructions, so it's appropriate for the front page.

## Troubleshooting

### My PR still targets `develop`
Update the base branch in the GitHub PR interface to `main`.

### I accidentally created a branch from `develop`
```bash
git checkout your-branch
git rebase --onto main develop
git push --force-with-lease origin your-branch
```

### I need to reference the old branching model
The old workflows are preserved in git history. Use:
```bash
git log --all -- .github/workflows/
```

## Need Help?

If you encounter any issues during the migration:
1. Check this guide first
2. Review the new workflows in `.github/workflows/`
3. Open an issue on GitHub
4. Contact the maintainers

---

**Migration Date**: 2025-11-19
**Status**: Active
