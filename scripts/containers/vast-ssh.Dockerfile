# Vast's SSH launch builds a derived image on each new host and installs these
# packages in it (about 20 s). Installed here, that step finds nothing to do.
ARG BASE
FROM ${BASE}
RUN apt-get update && apt-get install --no-install-recommends -y \
    openssh-server tmux git wget curl less locales sudo software-properties-common rsync \
    && rm -rf /var/lib/apt/lists/*
