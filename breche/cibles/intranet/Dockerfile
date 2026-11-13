# Brèche · cible « Intranet Morel » (modules 6 et 7). VOLONTAIREMENT VULNÉRABLE.
# À ne lancer que sur ta machine, publiée sur 127.0.0.1 uniquement.
FROM python:3.12-slim
RUN pip install --no-cache-dir flask==3.0.3 playwright==1.47.0 \
 && playwright install --with-deps chromium \
 && useradd -m intranet && mkdir -p /app && chown intranet:intranet /app \
 && cp -r /root/.cache/ms-playwright /home/intranet/.cache-pw && chown -R intranet:intranet /home/intranet/.cache-pw
ENV PLAYWRIGHT_BROWSERS_PATH=/home/intranet/.cache-pw
WORKDIR /app
COPY --chown=intranet:intranet . /app
USER intranet
EXPOSE 8091
CMD ["python", "app.py"]
