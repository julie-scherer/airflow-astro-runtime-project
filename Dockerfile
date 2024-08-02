FROM quay.io/astronomer/astro-runtime:10.5.0

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ffmpeg && \
    rm -rf /var/lib/apt/lists/*

USER astro
