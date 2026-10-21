ARG TEX_IMAGE
FROM ${TEX_IMAGE}
# Preserve the pinned TeX distribution and add only a non-root workspace account.
RUN if ! id -u vscode >/dev/null 2>&1; then useradd --create-home --shell /bin/bash vscode; fi
USER vscode
