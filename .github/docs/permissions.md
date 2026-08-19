# GitHub Actions Permissions Inventory

Permissions are part of the reusable workflow contract and must be documented
alongside secrets and inputs.

| Workflow | Permissions |
|---|---|
| `reusable-test.yml` | `contents: read` |
| `reusable-codeql.yml` | `actions: read`, `contents: read`, `security-events: write` |
| `reusable-sonarqube.yml` | `contents: read`, `actions: read` |
| `reusable-docker-build.yml` | `contents: read`, `packages: write` |
| `reusable-docker-push.yml` | `contents: read`, `packages: write` |
| `reusable-trivy.yml` | `contents: read`, `security-events: write` |
| `reusable-notification.yml` | `contents: read` |
| `reusable-deploy.yml` | `contents: read` |
| `reusable-sync.yml` | `contents: read` |

## Security rule

Use the smallest permission set required by each reusable workflow.

Do not add:

```yaml
permissions: write-all
```

or:

```yaml
permissions:
  contents: write
```

unless the workflow genuinely needs it.

## OIDC

If a future reusable workflow authenticates to a cloud provider using GitHub
OIDC, that specific job should additionally request:

```yaml
id-token: write
```

Keep this permission limited to the OIDC job.
