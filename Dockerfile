# syntax=docker/dockerfile:1.7

ARG UBUNTU_VERSION=24.04
ARG CPPCHECK_VERSION=2.21.1

# ---------------------------------------------------------------------------
# Stage 1: build cppcheck from source
# ---------------------------------------------------------------------------
FROM ubuntu:${UBUNTU_VERSION} AS builder

ARG CPPCHECK_VERSION
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        ninja-build \
        git \
        ca-certificates \
        libpcre3-dev \
        python3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src
RUN git clone --depth 1 --branch "${CPPCHECK_VERSION}" \
        https://github.com/danmar/cppcheck.git .

RUN cmake -S . -B build -G Ninja \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/opt/cppcheck \
        -DHAVE_RULES=ON \
        -DUSE_MATCHCOMPILER=ON \
        -DFILESDIR=/opt/cppcheck/share/cppcheck \
    && cmake --build build --parallel \
    && cmake --install build

RUN /opt/cppcheck/bin/cppcheck --version

# ---------------------------------------------------------------------------
# Stage 2: minimal runtime image
# ---------------------------------------------------------------------------
FROM ubuntu:${UBUNTU_VERSION} AS runtime

ARG CPPCHECK_VERSION
ARG DEBIAN_FRONTEND=noninteractive

LABEL org.opencontainers.image.title="cppcheck" \
      org.opencontainers.image.description="Static analysis tool for C/C++ (cppcheck) on Ubuntu" \
      org.opencontainers.image.source="https://github.com/danmar/cppcheck" \
      org.opencontainers.image.licenses="GPL-3.0-or-later"

RUN apt-get update && apt-get install -y --no-install-recommends \
        libpcre3 \
        python3 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/cppcheck /opt/cppcheck

# Bundle the MISRA C:2012 rule-texts file supplied by MISRA under
# CC BY-NC-ND 4.0 and register a shim addon `misra-c2012` that runs
# cppcheck's misra.py with --rule-texts pre-supplied. Callers invoke
# `cppcheck --enable=style --addon=misra-c2012 <src>` and receive rule
# violations tagged with the readable MISRA guideline text.
#
# A shim .py (rather than a .json config) is required because cppcheck's
# `--addon=<name>` resolver only looks for `<name>.py`.
COPY documents/assets/misra_c_2012_for_cppcheck.txt \
     /opt/cppcheck/share/cppcheck/misra_c_2012_for_cppcheck.txt
RUN printf '%s\n' \
    '#!/usr/bin/env python3' \
    'import os, sys' \
    'here = os.path.dirname(os.path.abspath(__file__))' \
    'rule_texts = "/opt/cppcheck/share/cppcheck/misra_c_2012_for_cppcheck.txt"' \
    'os.execvp(sys.executable, [sys.executable, os.path.join(here, "misra.py"),' \
    '                           "--rule-texts=" + rule_texts, *sys.argv[1:]])' \
    > /opt/cppcheck/share/cppcheck/addons/misra-c2012.py \
 && chmod +x /opt/cppcheck/share/cppcheck/addons/misra-c2012.py

ENV PATH="/opt/cppcheck/bin:${PATH}"

RUN useradd --create-home --shell /bin/bash cppcheck
USER cppcheck
WORKDIR /work

ENTRYPOINT ["cppcheck"]
CMD ["--help"]
