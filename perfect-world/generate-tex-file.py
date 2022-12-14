#!/usr/bin/env python3
import os

TEX_HEADER = r'''\documentclass[zihao=5,openright]{ctexbook}
\usepackage{xcolor}
\usepackage{geometry}
\usepackage{newtxmath}
\usepackage{xpatch}
\makeatletter
\xpatchcmd{\chapter}
  {\if@openright\cleardoublepage\else\clearpage\fi}{\par\relax}
  {}{}
\makeatother
\geometry{top=5em, bottom=5em, left=5em, right=5em}
\renewcommand{\thesection}{\arabic{section}}
\ctexset{
  section/nameformat += \S,
  section/name = {第,章},
  section/numberformat = \color{blue}\zihao{-4}\emph,
}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyfoot[C]{\textbf{--~\thepage~--}} % except the center
\fancyhead[L]{\sectionmark}
\fancyhead[L]{ssayno}
\renewcommand{\headrulewidth}{0.4pt}%
\renewcommand{\footrulewidth}{0pt}%
\setlength{\headheight}{12.64723pt}
\addtolength{\topmargin}{-0.64723pt}
\usepackage{fourier-orns}
\renewcommand\footrule{%
    \hrulefill
	\raisebox{-2.1pt}
	{\quad\decofourleft\decotwo\decofourright\quad}%
	\hrulefill
}
\setmainfont{PingFang SC}
\usepackage{hyperref}
\usepackage{graphicx}
\setlength{\parskip}{0.8\baselineskip}%
\setlength{\parindent}{2\ccwd}
\begin{document}
'''
TEX_TAIL = r'''\end{document}
'''
def main(path):
    with open("main.tex", 'w+', encoding='U8') as f:
        f.write(TEX_HEADER)
        temp = {}
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if item.startswith('.') or not os.path.isfile(item_path):
                continue
            number = int(item.split('-')[0])
            include_string = f'\include{{{item_path}}}\n'
            temp[number] = include_string
        for i in sorted(temp.items()):
            f.write(i[1])
        f.write(TEX_TAIL)



if __name__ == '__main__':
    input_path = 'Perfect-World-TeX'
    main(input_path)
