# Trunk-Based Development Setup - Complete

This document provides a complete overview of the trunk-based development setup for Ragbits.

## Overview

The repository has been configured for **trunk-based development** where:
- `main` is the single source of truth for all development
- Nightly builds are published from `main` automatically
- Stable releases are created via PR → merge → auto-tag workflow
- Hotfixes follow the same pattern with patch version bumps

## Quick Reference

### For Developers

**Creating a feature/fix:**
```bash
git checkout main
git pull origin main
git checkout -b feature/my-feature
# ... make changes ...
git push origin feature/my-feature
# Create PR targeting main
```

**Installing nightly build:**
```bash
pip install ragbits --pre
```

**Installing stable release:**
```bash
pip install ragbits
```

### For Maintainers

**Creating a stable release (major/minor):**
1. Go to Actions → "Stable Release"
2. Run workflow with version type
3. Review and merge the auto-generated PR
4. Release is automatically tagged and published

**Creating a hotfix (patch):**
1. Go to Actions → "Patch Release (Hotfix)"
2. Run workflow with description
3. Review and merge the auto-generated PR
4. Hotfix is automatically tagged and published

## File Changes

### New Workflows

1. **`.github/workflows/release-stable.yml`**
   - Creates PR for stable (major/minor) releases
   - Updates all package versions
   - Generates changelog entries
   - Manual trigger with version type selection

2. **`.github/workflows/release-stable-publish.yml`**
   - Automatically runs when release PR is merged
   - Creates git tag
   - Publishes to PyPI
   - Deploys stable documentation
   - Creates GitHub release

3. **`.github/workflows/release-patch.yml`**
   - Creates PR for hotfix/patch releases
   - Bumps patch version for all packages
   - Adds hotfix entry to changelogs
   - Manual trigger with description input

4. **`.github/workflows/update-readme-stable.yml`**
   - Updates README after stable release
   - Runs automatically on GitHub release creation

### Updated Workflows

5. **`.github/workflows/nightly-build.yml`**
   - Changed from `develop` branch to `main` branch
   - Continues to build nightly releases daily at 2 AM UTC

### Deprecated Workflows

6. **`.github/workflows/prepare-release.yml`**
   - Marked as deprecated (individual package releases)
   - Use `release-stable.yml` instead

7. **`.github/workflows/publish-pypi.yml`**
   - Marked as deprecated
   - Use `release-stable-publish.yml` instead

### Removed Workflows

8. **`.github/workflows/pull-request-change-base-branch.yml`**
   - ❌ Removed (no longer needed)
   - Previously auto-rebased PRs from main to develop

9. **`.github/workflows/sync-develop-after-release.yml`**
   - ❌ Removed (no longer needed)
   - Previously synced develop after release

### Updated Scripts

10. **`scripts/generate_changelog_entries.py`**
    - Default branch changed from `develop` to `main`

11. **`scripts/update_develop_versions.py`**
    - Deprecated and renamed to `.deprecated` extension

### Updated Documentation

12. **`CONTRIBUTING.md`**
    - Added branching strategy section
    - Added PR creation workflow
    - Added release process documentation

13. **`MIGRATION_TRUNK_BASED.md`** (NEW)
    - Complete migration guide from git-flow to trunk-based
    - FAQ and troubleshooting
    - Step-by-step instructions for maintainers and contributors

14. **`.github/TRUNK_BASED_SETUP.md`** (THIS FILE)
    - Overview of the new setup
    - Quick reference guide
    - Complete file changes list

## Workflow Diagrams

### Stable Release Flow
```
Developer Trigger → release-stable.yml
                    ↓
                    Creates PR (version bumps + changelog)
                    ↓
                    Manual Review & Merge
                    ↓
                    release-stable-publish.yml (auto)
                    ↓
                    Tag + Publish PyPI + GitHub Release + Docs
```

### Hotfix Flow
```
Developer Trigger → release-patch.yml
                    ↓
                    Creates PR (patch bump + changelog entry)
                    ↓
                    Manual Review & Merge
                    ↓
                    release-stable-publish.yml (auto)
                    ↓
                    Tag + Publish PyPI + GitHub Release
```

### Nightly Build Flow
```
Daily at 2 AM UTC → nightly-build.yml
                    ↓
                    Check for new commits on main
                    ↓
                    Build & Publish to PyPI (--pre)
                    ↓
                    Tag with .devYYYYMMDDHHMM
```

### Development Flow
```
Developer creates feature branch from main
                    ↓
                    Makes changes
                    ↓
                    Creates PR targeting main
                    ↓
                    CI checks run
                    ↓
                    Review & Merge to main
                    ↓
                    Available in nightly builds
```

## Key Benefits

### ✅ Developer Experience
- **No branch confusion** - Always target `main`
- **Faster feedback** - Changes available in nightly immediately
- **Simpler workflow** - One branch to remember
- **No auto-rebase surprises** - PRs stay where you put them

### ✅ Release Management
- **Automated workflow** - PR → Review → Merge → Auto-publish
- **Consistent versioning** - All packages stay in sync
- **Clear audit trail** - Every release has a PR
- **Quick hotfixes** - Patch releases follow same pattern

### ✅ Quality & Stability
- **Main always releasable** - CI must pass to merge
- **Nightly testing** - Daily builds catch issues early
- **Protected releases** - Manual review required for all releases
- **Changelog automation** - AI-generated changelog entries

### ✅ Documentation
- **Clear README** - Front page shows both stable and nightly options
- **Versioned docs** - Stable docs deployed automatically
- **Migration guide** - Easy transition for contributors

## Migration Checklist

For repository maintainers migrating to this setup:

- [ ] Review all new workflow files
- [ ] Test stable release workflow in a feature branch first
- [ ] Test patch release workflow in a feature branch first
- [ ] Update GitHub repository settings (default branch = main)
- [ ] Merge or close all PRs targeting `develop`
- [ ] Communicate changes to all contributors
- [ ] Update external documentation/links
- [ ] Delete `develop` branch (after transition period)
- [ ] Monitor first few releases for issues

## Testing the Setup

Before going live, test each workflow:

### 1. Test Stable Release
```bash
# Create a test branch
git checkout -b test/release-workflow
# Manually trigger release-stable workflow
# Verify PR is created correctly
# Do NOT merge the test PR
```

### 2. Test Patch Release
```bash
# Manually trigger release-patch workflow
# Verify PR is created correctly
# Do NOT merge the test PR
```

### 3. Test Nightly Build
```bash
# Wait for next scheduled run or trigger manually
# Verify it builds from main
# Check PyPI for nightly package
```

## Troubleshooting

### Workflow fails with permission error
- Ensure `GH_TOKEN` secret is set with appropriate permissions
- Check workflow permissions in repository settings

### PyPI publish fails
- Verify `PYPI_TOKEN` secret is set correctly
- Check token permissions on PyPI

### Git tag creation fails
- Ensure bot user has write access
- Check branch protection rules

### Nightly build not running
- Check workflow schedule syntax
- Verify workflow is enabled in repository settings

## Support

For issues or questions:
1. Check `MIGRATION_TRUNK_BASED.md` for migration help
2. Review `CONTRIBUTING.md` for workflow details
3. Open an issue on GitHub
4. Contact repository maintainers

---

**Setup Date**: 2025-11-19
**Status**: Ready for deployment
**Version**: 1.0
