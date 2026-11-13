# Brèche · cible « Morel Optique » (modules 3, 4 et 5). VOLONTAIREMENT VULNÉRABLE.
# À ne lancer que sur ta machine, publiée sur 127.0.0.1 uniquement.
FROM python:3.12-slim
RUN pip install --no-cache-dir flask==3.0.3 && useradd -m boutique && mkdir -p /app && chown boutique:boutique /app
WORKDIR /app
COPY --chown=boutique:boutique . /app
USER boutique
EXPOSE 8090
CMD ["python", "app.py"]
