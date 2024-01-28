from openai import OpenAI
import os

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

class GptMixin:
            
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

