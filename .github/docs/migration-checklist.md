# Reusing These Workflows in Another Repository

Use this checklist when migrating the reusable CI/CD platform to another
repository.

- [ ] Confirm the repository can access the reusable workflow repository.
- [ ] Pin the reusable workflow to a release tag rather than `main`.
- [ ] Copy only the caller-side workflow configuration.
- [ ] Identify which reusable workflows are actually used.
- [ ] Configure all required `workflow_call` inputs.
- [ ] Create only the secrets required by those workflows.
- [ ] Create non-sensitive configuration as repository/environment variables.
- [ ] Create `development`, `staging` and/or `production` environments as needed.
- [ ] Add environment-specific secrets for deployment.
- [ ] Configure the correct self-hosted runner labels for k3s deployments.
- [ ] Configure GitHub Actions permissions required by each workflow.
- [ ] Verify CodeQL has `security-events: write`.
- [ ] Verify Trivy SARIF upload has `security-events: write`.
- [ ] Verify GHCR publishing has `packages: write`.
- [ ] Verify SonarQube URL and token.
- [ ] Verify Docker registry credentials.
- [ ] Verify Kubernetes credentials if Kubernetes deployment is used.
- [ ] Verify SSH credentials if Docker Compose deployment is used.
- [ ] Verify notification webhook only if notifications are enabled.
- [ ] Verify repository-sync token only if sync is enabled.
- [ ] Never copy actual secret values into Git.
- [ ] Rotate credentials if their origin or exposure history is uncertain.
- [ ] Test the workflow on a non-production environment first.
- [ ] Promote the tested workflow version to production.

## Recommended future improvements

- [ ] Publish versioned reusable workflow releases.
- [ ] Prefer `GITHUB_TOKEN` for GHCR when possible.
- [ ] Move `sonar-host-url` from Secret to Variable.
- [ ] Replace long-lived cloud credentials with OIDC.
- [ ] Consider GitHub App authentication for repository synchronization.
- [ ] Review the current `DEPLOY_KEY` requirement in SonarQube and deployment
      workflows.
- [ ] Remove debug steps that expose token lengths/prefixes.
- [ ] Avoid `StrictHostKeyChecking=no`; use managed SSH known-hosts where
      possible.
