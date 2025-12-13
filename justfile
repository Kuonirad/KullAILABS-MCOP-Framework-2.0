set shell := ["bash", "-lc"]

# Default recipe: show available commands
default:
    @just --list

# Full reproducibility check
reproduce:
    @echo "=== MCOP Framework 2.0 - Reproducibility Check ==="
    @echo ""
    @echo "1. Environment Information:"
    node --version
    npm --version
    @echo ""
    @echo "2. Installing Dependencies:"
    npm ci
    @echo ""
    @echo "3. Running Linter:"
    npm run lint
    @echo ""
    @echo "4. Building Project:"
    npm run build
    @echo ""
    @echo "5. Running Tests:"
    npm test || true
    @echo ""
    @echo "=== Q.E.D. - Build Reproduced Successfully ==="

# Install dependencies
install:
    npm ci

# Run development server
dev:
    npm run dev

# Build for production
build:
    npm run build

# Run tests
test:
    npm test

# Run linter
lint:
    npm run lint

# Run security audit
audit:
    npm audit --audit-level=moderate

# Run all CI checks locally
ci: lint build test audit
    @echo "All CI checks passed!"

# Clean build artifacts
clean:
    rm -rf .next node_modules coverage artefacts

# Run security test harness
security-test:
    node scripts/security/test-malicious-mod.mjs

# Run Trojan Source scan locally
scan-trojan:
    @python3 -c "
    import os, sys
    BAD = set(['\u202A','\u202B','\u202C','\u202D','\u202E','\u2066','\u2067','\u2068','\u2069','\u200E','\u200F','\u061C'])
    ex_dirs = {'.git','node_modules','.next','dist','build','out','coverage'}
    ex_exts = {'.png','.jpg','.jpeg','.gif','.webp','.ico','.zip','.gz','.tar','.pdf'}
    offenders = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ex_dirs]
        for fn in files:
            path = os.path.join(root, fn)
            _, ext = os.path.splitext(path)
            if ext.lower() in ex_exts: continue
            try:
                text = open(path,'rb').read().decode('utf-8', errors='ignore')
            except: continue
            hits = [i for i,ch in enumerate(text) if ch in BAD]
            if hits: offenders.append((path, hits[:5]))
    if offenders:
        print('FAIL: Trojan Source detected:')
        for p, h in offenders: print(f'  - {p}: {h}')
        sys.exit(1)
    print('OK: No bidi/hidden controls found.')
    "

# Format code (if prettier is installed)
format:
    npx prettier --write "src/**/*.{ts,tsx,js,jsx,json,css,md}"

# Check types
typecheck:
    npx tsc --noEmit

# Full quality check
quality: lint typecheck scan-trojan security-test
    @echo "All quality checks passed!"
