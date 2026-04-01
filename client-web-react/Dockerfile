# Stage 1: Build
ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}node:25.8.0-alpine AS builder

WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
COPY . .
RUN pnpm run build

# Stage 2: Copy build output
FROM ${REGISTRY_PREFIX_DOCKER_HUB}alpine:latest
COPY --from=builder /app/dist /output/
