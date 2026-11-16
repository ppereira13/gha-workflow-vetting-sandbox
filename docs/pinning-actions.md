# Pinning third-party actions

Related zizmor rule: unpinned-uses

A step such as `uses: actions/checkout@v4` refers to the action by a tag. Tags and
branches are mutable: whoever controls the action's repository can move `v4` to a
different commit at any time. If the maintainer's account is compromised, the attacker
can repoint the tag to malicious code, and every workflow that uses the tag runs that
code on its next execution, with access to the repository contents and to any secrets
available to the job. This happened in March 2025 with `tj-actions/changed-files`,
where retargeted tags caused secrets to be printed in the logs of many repositories.

A more specific tag such as `v4.0.0` is still a tag and can still be moved. It does not
solve the problem.

## Fix

Pin the action to a full-length commit SHA, which identifies immutable content, and keep
the human-readable version in a comment:

```yaml
- uses: actions/checkout@<full 40-character commit SHA> # v4.2.2
```

Use a tool such as Dependabot or Renovate to propose updates to the pinned SHA, so that
pinning does not mean staying on old versions forever.

Source: GitHub Docs, "Security hardening for GitHub Actions", section on using
third-party actions.
