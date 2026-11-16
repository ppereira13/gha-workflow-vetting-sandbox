# Credentials left behind by actions/checkout

Related zizmor rule: artipacked

By default, `actions/checkout` writes the job's `GITHUB_TOKEN` into the local git
configuration of the checked-out repository (inside the `.git` directory), so that later
steps can run authenticated git commands.

The token therefore sits in a file on the runner for the rest of the job. Any later step
can read it. If the workspace, including the `.git` directory, is uploaded as an
artifact or packed into a release, the token is published with it. The rule name
"artipacked" comes from this: credentials packed into artifacts.

This finding is about the automatic token stored by the checkout step. It is unrelated
to user-defined secrets such as a deploy token.

## Fix

Tell the checkout step not to keep the credentials, unless a later step really needs to
push with git:

```yaml
- uses: actions/checkout@<full commit SHA>
  with:
    persist-credentials: false
```

Sources: `actions/checkout` README (persist-credentials input); zizmor audit
documentation, "artipacked".
