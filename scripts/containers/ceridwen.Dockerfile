FROM python:3.11.16-slim-bookworm AS build
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir uv==0.7.20
COPY scripts/containers/requirements.txt /opt/ceridwen-requirements.txt
RUN uv venv /opt/ceridwen && uv pip install --no-cache --python /opt/ceridwen/bin/python \
    -r /opt/ceridwen-requirements.txt && uv pip check --python /opt/ceridwen/bin/python

FROM python:3.11.16-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server rsync curl ca-certificates procps libgomp1 \
    && rm -rf /var/lib/apt/lists/* && mkdir -p /run/sshd
COPY --from=build /opt/ceridwen /opt/ceridwen
COPY --from=build /usr/local/bin/uv /usr/local/bin/uv
COPY --from=build /opt/ceridwen-requirements.txt /opt/ceridwen-requirements.txt
ENV NVIDIA_VISIBLE_DEVICES=all NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV VIRTUAL_ENV=/opt/ceridwen PATH=/opt/ceridwen/bin:$PATH
RUN JAX_PLATFORMS=cpu /opt/ceridwen/bin/python -c \
    "import jax, blackjax, h5py, nbclient, specutils; import tensorflow_probability.substrates.jax; assert jax.config.x64_enabled is False"
LABEL org.opencontainers.image.source="https://github.com/potatoist314/cosmic-chronometers-jwst"
EXPOSE 22
CMD ["/bin/bash"]
