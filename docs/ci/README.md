# Enable GitHub Actions

The initial publisher could create the public repository but its OAuth token did not include GitHub's `workflow` scope. No automatic CI run is claimed. The 15 core tests were run locally, along with JavaScript syntax, documentation-link and actual macOS audio-build checks.

The pinned workflow is in [ci.yml](ci.yml). A maintainer with workflow write access can copy it to `.github/workflows/ci.yml` and commit it. It runs the standard-library test suite on Python 3.10 and 3.13, checks player JavaScript and documentation, and builds the source-only skill ZIP. It requests only `contents: read` and does not publish lessons or use model credentials.

```sh
mkdir -p .github/workflows
cp docs/ci/ci.yml .github/workflows/ci.yml
git add .github/workflows/ci.yml
git commit -m "Enable core CI"
git push
```

Use an existing authorized credential with workflow write access; this repository's installer does not request or store GitHub credentials.
