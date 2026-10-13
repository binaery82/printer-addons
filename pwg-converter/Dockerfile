FROM ghcr.io/home-assistant/base:latest

# Ghostscript für PWG-Raster-Konvertierung
RUN apk add --no-cache \
    python3 \
    ghostscript

WORKDIR /app
COPY server.py /app/server.py
COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD ["/run.sh"]
