#!/bin/bash
# uso: ./run_pass.sh <nome> [paginas.json]
#   gera build/<nome>.docx (Word, legendas por campo) e build/<nome>_audit.docx/.pdf
#   (legendas estáticas, renderizado pelo LibreOffice para conferir a paginação)
# Variável opcional: SOFFICE (padrão: soffice, do LibreOffice)
set -e
cd "$(dirname "$0")"
mkdir -p build
python3 build.py "build/$1.docx" $2
AUDIT_STATIC_CAPTIONS=1 python3 build.py "build/$1_audit.docx" $2
cd build && rm -f "$1_audit.pdf"
timeout 300 "${SOFFICE:-soffice}" --headless --convert-to pdf "$1_audit.docx" >/dev/null 2>&1
pdfinfo "$1_audit.pdf" | grep Pages
