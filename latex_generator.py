import os
import subprocess
from datetime import datetime

class LatexMixin:
    @property
    def latex_directory(self):
        # It starts with the date
        today = datetime.now()
        date = today.strftime("%Y-%m-%d")

        # The style of the company name and job title is PascalCase
        def to_pascal_case(text):
            # Split the text by spaces or underscores
            words = text.replace('_', ' ').split()

            # Capitalize the first letter of each word and join them together
            camel_case = ''.join(word.lower().capitalize() for word in words)

            return camel_case

        # Accessing company name and job title from self.data dictionary
        return f"cover_letters/{date}_{to_pascal_case(self.data['company_name'])}_{to_pascal_case(self.data['job_title'])}"

    @property
    def latex_macros_file(self):
        file = (
            r"\newcommand{\geometryConditions}{\geometry{margin=1in}}" + "\n" +
            r"\newcommand{\candidateName}{" + self.data['candidate_name'] + r"}" + "\n" +
            # Note that we edit the address to have "\\" instead of "\n"
            r"\newcommand{\candidateAddress}{" + self.data['candidate_address'].replace("\n", r"\\") + r"}" + "\n" +
            r"\newcommand{\companyAddress}{" + self.data['company_address'] + r"}" + "\n" +
            r"\newcommand{\hiringManager}{" + self.data['hiring_manager'] + r"}" + "\n"
        )

        return file

    def create_latex_files(self):
        # Ensure the directory exists
        if not os.path.exists(self.latex_directory):
            os.makedirs(self.latex_directory)

        # Create main file, whose content never changes
        main_file = os.path.join(self.latex_directory, "CoverLetter.tex")
        with open(main_file, 'w') as file:
            file.write(self.latex_main_file)

        # Create macros file
        macros_file = os.path.join(self.latex_directory, "macros.tex")
        with open(macros_file, 'w') as file:
            file.write(self.latex_macros_file)

        # Create body of the letter file, assuming without XML tags
        if self.data['body'] is None:
            self.create_cover_letter()

        body_file = os.path.join(self.latex_directory, "body.tex")
        with open(body_file, 'w') as file:
            file.write(self.data['body'])

        # Compile the LaTeX file into a PDF
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', "CoverLetter.tex"],
            capture_output=True,
            text=True,
            cwd=self.latex_directory  # Set the working directory to where your LaTeX files are
        )

        # Check if pdflatex succeeded
        if result.returncode == 0:
            print("LaTeX compilation successful.")
        else:
            print("LaTeX compilation failed.")
            print("stdout:", result.stdout)
            print("stderr:", result.stderr)

        return result.returncode
