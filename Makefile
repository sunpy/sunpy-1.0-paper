LATEX       = pdflatex -interaction=nonstopmode -halt-on-error
LATEXMK     = latexmk -pvc -pdf
BASH        = bash -c
ECHO        = echo
RM          = rm -rf
TMP_SUFFS   = pdf aux bbl blg log dvi ps eps out brf
CHECK_RERUN =

NAME = main

.PHONY: latexmk

all: python ${NAME}.pdf

python: ./figures/*.py
	pip install -r ./figures/requirements.txt
	python ./figures/*.py
	echo "Created Python plots."

${NAME}.pdf: ${NAME}.tex *.bib
	${LATEX} ${NAME}
	bibtex ${NAME}
	${LATEX} ${NAME}
	( grep "Rerun to get" ${NAME}.log && ${LATEX} ${NAME} ) || echo "Done."
	( grep "Rerun to get" ${NAME}.log && ${LATEX} ${NAME} ) || echo "Done."

latexmk: ${NAME}.tex *.bib
	${LATEXMK} ${NAME}.tex

clean:
	${RM} $(foreach suff, ${TMP_SUFFS}, ${NAME}.${suff})
	${RM} *.aux
