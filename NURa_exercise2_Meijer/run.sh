#!/bin/bash

echo "Run handin exercise 2"

echo "Clearing/creating the plotting directory"
if [ ! -d "plots" ]; then
  mkdir plots
fi
rm -rf plots/*

#echo "Download points for Vandermonde matrix ..."
#if [ ! -e Vandermonde.txt ]; then
#  wget https://home.strw.leidenuniv.nl/~daalen/Handin_files/Vandermonde.txt
#fi

# Script for question 1
echo "Run question 1 ..."
python3 question1.py

# Script for question 2
#echo "Run question 2 ..."
#python3 question2.py

# Script for question 2d
#echo "Run question 2d ..."
#python3 question2d.py

echo "Generating the pdf"

pdflatex NUR_exercise2_Meijer.tex
bibtex NUR_exercise2_Meijer.aux
pdflatex NUR_exercise2_Meijer.tex
pdflatex NUR_exercise2_Meijer.tex


