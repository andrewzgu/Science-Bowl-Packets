#!/usr/bin/env bash

while getopts "d" opt; do
  case $opt in
    d)
      draft=true
      ;;
  esac
done

draftstr="\\def\\draftmode{1}"

rm -rf compiled
mkdir -p compiled

for i in {1..13}
do
  filecontents="\\newcommand{\\roundnumber}{$i} \\input{roundtemplate.tex}"
  if [ "$draft" = true ]; then
    filecontents="${draftstr} ${filecontents}"
  fi
  echo "${filecontents}"
  pdflatex -output-directory compiled \
    -interaction=nonstopmode \
    -jobname="round$i" \
    $filecontents
done
