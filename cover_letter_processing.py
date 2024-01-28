import os
from openai import OpenAI
from forms import CoverLetterForm
from latex_generator import LatexMixin

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)
    
class CoverLetterData(LatexMixin):
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
            
    def create_cover_letter(self):
        prompt = f'''
        Your task is to adapt a generic cover letter to an actual job openning. \
                The generic cover letter is given between XML-style <CoverLetterBody> tag. \
                Each section of the cover letter is also enclosed by XML tags, named semantically. \
                The job ad is delimited by the <JobAd> tag, the company name is delimited by <CompanyName>, \
                the position name by <PositionName>. There may be some extra information about the company \
                delimited by <AboutCompany> tag. Your response should consist only of the body of the \
                cover letter, without the openning ("Dear Hiring Manager,"), closing sentence ("Yours sincerely,") nor \
                signature.
                {self.base_cover_letter_content}
                <CompanyName>
                {self.company_name}
                </CompanyName>
                <PositionName>
                {self.job_title}
                </PositionName>
                <JobAd>
                {self.job_ad}
                </JobAd>
                <AboutCompany>
                {self.about_company}
                </AboutCompany>
        '''

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )

        self.gpt_cover_letter = chat_completion.choices[0].message.content
