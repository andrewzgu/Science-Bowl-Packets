#!/usr/bin/env bash

if [[ ! -f config.cfg ]] ; then
  echo 'File "config.cfg" is missing. Making blank config file. Please add in the missing values.'
  echo 'NUMBER_OF_ROUNDS=' > config.cfg
  exit
fi

IFS="="
while read -r name value
do
  export "$name"="$value"
done < config.cfg

if [[ -z "$NUMBER_OF_ROUNDS" ]]; then
  echo 'Config file is missing NUMBER_OF_ROUNDS, aborting.'
  exit
fi

while getopts "d" opt; do
  case $opt in
    d)
      draft=true
      ;;
    *)
      echo "Unrecognized flag"
      ;;
  esac
done

rm -rf compiled
mkdir -p compiled

echo "Making $NUMBER_OF_ROUNDS rounds. Please check config.cfg if this is incorrect."

for (( i=1; i<=NUMBER_OF_ROUNDS; i++ ))
do
  filecontents="\\newcommand{\\roundnumber}{$i} \\input{roundtemplate.tex}"
  if [ "$draft" = true ]; then
    filecontents="\\def\\draftmode{1} ${filecontents}"
  fi
  pdflatex -output-directory compiled \
    -interaction=batchmode \
    -jobname="round$i" \
    "$filecontents"
done
