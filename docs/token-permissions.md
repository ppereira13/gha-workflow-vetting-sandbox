# Permissions of the GITHUB_TOKEN

Related zizmor rule: excessive-permissions

Every workflow run receives an automatic, short-lived token called `GITHUB_TOKEN`. Steps
and actions use it to talk to the repository. When a workflow has no `permissions:`
block, the token gets the repository's default permissions, which can include write
access to code, issues, pull requests and packages.

This finding is about that automatic token. It is not about secrets defined by the user,
such as a deploy token.

If any step in the job is compromised, for example a malicious third-party action or an
injected command, it can use the token with all the permissions it was given. A token
that can only read limits the damage.

## Fix

Declare the minimum permissions at the top of the workflow, and widen them only in the
jobs that need more:

```yaml
permissions:
  contents: read
```

A job that needs to comment on pull requests would add `pull-requests: write` for that
job only. `permissions: {}` removes all permissions.

Source: GitHub Docs, "Security hardening for GitHub Actions" and "Controlling
permissions for GITHUB_TOKEN".
