FROM node:24-alpine AS dependencies
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

FROM dependencies AS development
COPY . .
EXPOSE 5173
ENV HOST=0.0.0.0
ENV PORT=5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]

FROM dependencies AS build
COPY . .
RUN npm run build

FROM node:24-alpine AS production
WORKDIR /app
ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000
COPY --from=build --chown=node:node /app/.output ./.output
USER node
EXPOSE 3000
HEALTHCHECK --interval=15s --timeout=3s --retries=5 CMD wget -q --spider http://127.0.0.1:3000/healthz || exit 1
CMD ["node", ".output/server/index.mjs"]
