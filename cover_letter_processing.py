from forms import InitialForm, PlainTextForm
from gpt_interface import GptMixin
from latex_generator import LatexMixin
    
# Here we are using the Mixin design pattern to separate part of the code into other files
# This does only the form preprocessing
class CoverLetter(GptMixin, LatexMixin):
    def __init__(self) -> None:
        # Initialize all data within a single dictionary
        self.data = {
            'candidate_name': None,
            'candidate_address': None,
            'company_name': None,
            'company_address': None,
            'about_company': None,
            'job_title': None,
            'job_ad': None,
            'hiring_manager': "Hiring Manager",  # Default value
            'closing_expression': "Sincerely",  # Default value
            'base_cover_letter_content': None,
            'body': None,
        }

    def process_initial_form(self, form: InitialForm) -> None:
    # The form comes with a list of candidates read from JSON and the index of the chosen one (as a string)
    # The choice is to use candidate_name instead of candidate.name for uniformity
        candidate = form.candidates_data[int(form.candidate_index.data)]
        self.data['candidate_name'] = candidate.name
        self.data['candidate_address'] = candidate.address

        # base_cover_letter_content is read from a file
        self.data['base_cover_letter_content'] = self._get_base_cover_letter_content(form)

        # if no hiring manager is provided, we use "Hiring Manager" as default
        self.data['hiring_manager'] = form.hiring_manager.data or "Hiring Manager"

        # For the following is simply reading the data
        self.data['job_ad'] = form.job_ad.data
        self.data['company_name'] = form.company_name.data
        self.data['job_title'] = form.job_title.data
        self.data['about_company'] = form.about_company.data

        # The following start with None - ensure this aligns with your initial data setup
        self.data['body'] = None  # Assuming you meant to use self.data['body'] instead of self.body
        self.data['company_address'] = None

        # The following has a standard value
        self.data['closing_expression'] = "Sincerely"

    @staticmethod
    def _get_base_cover_letter_content(form):
        with open(f'base_cover_letters/{form.base_cover_letter.data}.xml', 'r') as file:
            lines = file.readlines()  # Read all lines into a list
            if lines and lines[0].startswith('<?xml'):
                return '\n'.join(lines[1:])  # Join all lines except the first one
            else:
                return '\n'.join(lines)  # Join all lines if no XML declaration