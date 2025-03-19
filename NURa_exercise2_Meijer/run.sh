#!/bin/bash

echo "Run handin exercise 2"

echo "Clearing/creating the plotting directory"
if [ ! -d "plots" ]; then
  mkdir plots
fi
rm -rf plots/*

# Script for question 1
echo "Run question 1 ..."
python3 question1.py

# Scripts for question 1
echo "Run randomnumbergenerator ... (ignore warning about overflow)"
python3 randomnumbergenerator.py
echo "Run question 1 ..."
python3 question1.py
echo "Run question 1a ..."
python3 question1a.py
echo "Run question 1b ... (ignore warning about overflow)"
python3 question1b.py
echo "Run question 1c ... (ignore warning about overflow)"
python3 question1c.py
echo "Run question 1d ..."
python3 question1d.py


# Scripts for question 2
echo "Run question 2a ..."
python3 question2a.py
echo "Run question 2b ..."
python3 question2b.py

echo "Generating the pdf"

pdflatex NUR_exercise2_Meijer.tex
bibtex NUR_exercise2_Meijer.aux
pdflatex NUR_exercise2_Meijer.tex
pdflatex NUR_exercise2_Meijer.tex


