#!/usr/bin/env bash
for i in {1..13}
do
  sed "s/ROUNDNUMBERVAR/$i/g" roundtemplate.tex > compiled/round$i.tex 
  pdflatex -output-directory compiled -interaction=nonstopmode compiled/round$i.tex
done
