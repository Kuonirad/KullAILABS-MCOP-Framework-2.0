# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:                |

## Reporting a Vulnerability

We are committed to the security of MCOP Framework 2.0. If you discover a security vulnerability, please report it responsibly.

### Reporting Process

**DO NOT report security vulnerabilities through public GitHub issues.**

Please email your findings to: **security@kullailabs.example.com**

If you use PGP, you may encrypt your communications. Our PGP key fingerprint is:
`[PGP KEY FINGERPRINT TO BE ADDED]`

### What to Include in Your Report

- Type of vulnerability (e.g., XSS, CSRF, injection, etc.)
- Full paths of affected source file(s)
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact assessment and potential severity

### Response Timeline

We adhere to a 90-day responsible disclosure policy. When a report is received, we will:

1. **Acknowledge receipt** within 48 hours
2. **Initial assessment** within 7 days
3. **Investigate and develop a patch** within 30 days
4. **Coordinate public disclosure** with the researcher once a patch is released or if the 90-day period elapses

### Disclosure Policy

- We will work with you to understand and validate your report
- We will coordinate with you on the timing of public disclosure
- We will credit you in any public acknowledgment (unless you prefer to remain anonymous)
- We will not take legal action against security researchers who follow this policy

## Security Best Practices

### For Contributors

- **Never commit secrets**: API keys, tokens, passwords should never be committed
- **Pin dependencies**: Always pin exact versions of critical dependencies
- **Review third-party code**: Audit any new dependencies before adding them
- **Follow least privilege**: Request minimum necessary permissions

### For Users

- **Keep updated**: Always use the latest supported version
- **Enable Dependabot**: Use automated dependency updates
- **Review configurations**: Audit any custom configurations for security implications
- **Monitor advisories**: Subscribe to security advisories for this repository

## Security Features

### Supply Chain Security

- All GitHub Actions are pinned to specific commit SHAs
- Dependencies are audited regularly via `npm audit`
- SBOM (Software Bill of Materials) is generated for releases

### CI/CD Security

- Branch protection rules enforce code review
- Signed commits are encouraged
- Secret scanning is enabled
- Dependabot alerts are configured

## Bug Bounty Program

We are considering establishing a bug bounty program. If you are interested in participating, please contact us at the security email address above.

## Acknowledgments

We thank all security researchers who help keep MCOP Framework 2.0 secure. Security contributors will be acknowledged in our release notes.

---

*This security policy is subject to change. Last updated: 2025-12-13*
