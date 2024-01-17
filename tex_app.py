import os
import subprocess
from datetime import datetime

main_document = r'''
\documentclass[11pt]{letter}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}

% Input file with macros
\input{macros}

% Macro using ``geometry``
\geometry_conditions

\date{}
\signature{\applicant_name}

\begin{document}

\begin{letter}{\company_address}

\opening{Dear \hiring_manager,}

% Input letter's main body
\input{body}

\closing{Sincerely,}

\end{letter}
\end{document}

'''

def make_file_name(company, job):
    def to_pascal_case(text):
        # Split the text by spaces or underscores
        words = text.replace('_', ' ').split()

        # Capitalize the first letter of each word and join them together
        camel_case = ''.join(word.lower().capitalize() for word in words)

        return camel_case

    today = datetime.now()
    date = today.strftime("%Y-%m-%d")

    return f"{date}_{to_pascal_case(company)}_{to_pascal_case(job)}"

print(make_file_name("caSa do CaraLho", "comedor de putas"))
pass

# LaTeX document content
latex_content = r'''
\documentclass{article}
\begin{document}
Hello, world!
\end{document}
'''

# Temporary dir name for testing
job = 'DATE_COMPANY_JOB'

# Create a directory for the LaTeX project if it doesn't exist
directory = f"cover_letters/{job}"
if not os.path.exists(directory):
    os.makedirs(directory)

# Path to the LaTeX file
file_path = os.path.join(directory, "document.tex")

# Write the LaTeX content to the file
with open(file_path, 'w') as file:
    file.write(latex_content)

# Compile the LaTeX file into a PDF
# This requires pdflatex to be installed on your system
compile_command = f"pdflatex -output-directory={directory} {file_path}"
subprocess.run(compile_command, shell=True, check=True)

print(f"LaTeX document compiled: {os.path.join(directory, 'document.pdf')}")

