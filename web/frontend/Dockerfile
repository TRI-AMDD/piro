ARG APP_DIR="/home/dockeruser"

FROM node:20-slim AS run-dev
ARG APP_DIR
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

RUN useradd -m dockeruser
WORKDIR ${APP_DIR}
USER dockeruser

RUN --mount=type=cache,id=pnpm,target=/pnpm/store \
    --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=pnpm-lock.yaml,target=pnpm-lock.yaml \
    pnpm install --frozen-lockfile

COPY --chown=dockeruser:dockeruser . .

CMD ["pnpm", "run", "dev"]

FROM run-dev AS build-prod
RUN pnpm run build

FROM scratch AS export-prod
ARG APP_DIR
COPY --from=build-prod ${APP_DIR}/dist /

# production environment
FROM nginx:latest
COPY --from=build-prod ${APP_DIR}/dist /usr/share/nginx/html
COPY nginx/default.conf.template /etc/nginx/templates/default.conf.template

CMD ["nginx", "-g", "daemon off;"]