# Brèche · lab « La planque » (module 1). Volontairement mal rangé, jamais exposé au réseau.
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends less file procps && rm -rf /var/lib/apt/lists/* \
 && useradd -m -s /bin/bash stagiaire && useradd -m -s /bin/bash jfaure && chmod 755 /home/jfaure
COPY --chown=jfaure:jfaure jfaure/ /home/jfaure/
RUN mkdir -p /opt/.archives-labo/2024 && echo "Mesures du banc optique : RAS." > /opt/.archives-labo/2024/banc.txt \
 && echo "BRECHE{l4_pl4nqu3_n_3st_j4m41s_v1d3}" > /opt/.archives-labo/2024/.note-perso && chmod -R a+rX /opt/.archives-labo \
 && echo "Bienvenue sur srv-test-03 (Verrerie Morel). Usage interne uniquement." > /etc/motd
USER stagiaire
WORKDIR /home/stagiaire
CMD ["bash", "-l"]
