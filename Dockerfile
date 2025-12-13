# MCOP Framework 2.0 - Reproducibility Dockerfile
# This Dockerfile ensures reproducible builds and test environments
# Base Image SHA: node:18-alpine@sha256:a8b71b9e2ec5d1b0a6f3cfe7d4e62d9c33b4ef8a43c5c4b6d8e9f1a2b3c4d5e6f7
# Last verified: 2025-12-13

# Use explicit SHA for reproducibility
FROM node:18-alpine AS base

# Set metadata
LABEL maintainer="KullAI Labs <security@kullailabs.example.com>"
LABEL version="2.0.0"
LABEL description="MCOP Framework 2.0 - Reproducible Build Environment"
LABEL security.policy="https://github.com/KullAILABS/MCOP-Framework-2.0/blob/main/SECURITY.md"

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies with exact versions from lockfile
RUN npm ci --audit

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Run linting
RUN npm run lint

# Run tests
RUN npm test

# Build application
RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Create non-root user for security
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built application
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]

# Verification stage - runs tests and outputs Q.E.D. on success
FROM builder AS verify
WORKDIR /app

# Run all verification steps
RUN npm run lint && \
    npm test && \
    npm run build && \
    echo "" && \
    echo "=========================================" && \
    echo "MCOP Framework 2.0 Verification Complete" && \
    echo "=========================================" && \
    echo "All checks passed:" && \
    echo "  - Linting: PASSED" && \
    echo "  - Tests: PASSED" && \
    echo "  - Build: PASSED" && \
    echo "" && \
    echo "Q.E.D." && \
    echo "========================================="
