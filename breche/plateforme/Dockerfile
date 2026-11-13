# Brèche · image de la plateforme
FROM node:22-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev && npm cache clean --force
COPY . .
RUN mkdir -p /donnees && chown node:node /donnees
USER node
ENV NODE_ENV=production PORT=8080 BRECHE_BASE=/donnees/breche.sqlite
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://127.0.0.1:8080/sante || exit 1
CMD ["node", "--no-warnings", "server.js"]
