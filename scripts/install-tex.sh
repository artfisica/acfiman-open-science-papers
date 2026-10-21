#!/usr/bin/env bash
set -euo pipefail
sudo apt-get update
sudo apt-get install -y --no-install-recommends make python3 git latexmk texlive-xetex texlive-latex-extra texlive-fonts-recommended texlive-lang-spanish fonts-lmodern poppler-utils
