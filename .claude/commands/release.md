# /release — Cut a new release

Automate the release process for PyPI and GitHub.

## What it does
1. **Bump version** in `mapwidgets/__init__.py` (`VERSION` tuple; prompts for semver: patch/minor/major) — `setup.py` reads it from there, no need to edit both
2. **Create changeset** in `.changeset/` directory
   - Auto-generates filename `0000-<type>-release.md` with semver and changelog
3. **Update docs** in `docs/releases/` with release notes
4. **Git operations**
   - Stage changes
   - Commit with message: "release: v{version}"
   - Create git tag: `v{version}`
   - Push to remote
5. **Create GitHub Release**
   - Creates release on GitHub with changelog from changeset
   - Marks as latest if on main branch

## Usage
```
/release
```

Prompts you for:
- **Semver type**: patch, minor, or major
- **Release notes**: changes, fixes, new features

## Reference
- Current version in `mapwidgets/__init__.py` (`VERSION` tuple) — single source of truth, `setup.py` parses it
- Changelog format follows `.changeset/` convention
- Requires `gh` CLI for GitHub operations
- Public repo: `erdem/django-map-widgets`

## Notes
- Will not push if CI checks haven't passed
- Always creates a new commit (never amends)
