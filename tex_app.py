import os
import subprocess

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

