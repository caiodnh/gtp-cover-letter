import os
from openai import OpenAI
from forms import CoverLetterForm

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)
    
class CoverLetterData:
    def __init__(self,form: CoverLetterForm) -> None:
        self.candidate = form.candidates_data[int(form.candidate_index.data)]
        self.base_cover_letter_content = self._get_cover_letter_content(form)
        self.hiring_manager = form.hiring_manager or "Hiring Manager"
        self.job_ad = form.job_ad.data
        self.company_name = form.company_name.data
        self.job_title = form.job_title.data
        self.about_company = form.about_company.data

    @staticmethod
    def _get_cover_letter_content(form):
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

        self.new_cover_letter = chat_completion.choices[0].message.content
