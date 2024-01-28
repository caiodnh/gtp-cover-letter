from forms import CoverLetterForm
from gpt_interface import GptMixin
from latex_generator import LatexMixin
    
# Here we are using the Mixin design pattern to separate part of the code into other files
# This does only the form preprocessing
class CoverLetterData(GptMixin, LatexMixin):
    def __init__(self,form: CoverLetterForm) -> None:
        # The form comes with a list of candidates read from JSON and the index of the chosen one (as a string)
        # The choice is to use candidate_name instead of candidate.name for uniformity
        candidate = form.candidates_data[int(form.candidate_index.data)]
        self.candidate_name = candidate.name
        self.candidate_address = candidate.address

        # base_cover_letter_content is read from a file
        self.base_cover_letter_content = self._get_base_cover_letter_content(form)

        # if no hiring manager is provided, we use "Hiring Manager" as default
        self.hiring_manager = form.hiring_manager.data or "Hiring Manager"

        # The remaining is simply reading the data
        self.job_ad = form.job_ad.data
        self.company_name = form.company_name.data
        self.company_address = form.company_address.data
        self.job_title = form.job_title.data
        self.about_company = form.about_company.data

        # The body of the cover letter maybe generated many times, and start with None
        self.gpt_cover_letter = None

    @staticmethod
    def _get_base_cover_letter_content(form):
        with open(f'base_cover_letters/{form.base_cover_letter.data}.xml', 'r') as file:
            lines = file.readlines()  # Read all lines into a list
            if lines and lines[0].startswith('<?xml'):
                return '\n'.join(lines[1:])  # Join all lines except the first one
            else:
                return '\n'.join(lines)  # Join all lines if no XML declaration