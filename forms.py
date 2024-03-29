from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, validators
import json
from functools import cached_property
import os

# Class with date from the candidate for the job
class Candidate:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __str__(self) -> str:
        return f"Name: {self.name} | Address: {self.address}"

# Class with root page's the forms fields
class InitialForm(FlaskForm):

    # ``candidate_index`` and ``base_cover_letter`` are updated below using ``__init__``, ``get_candidate_choices`` and ``get_base_cover_letter_choices``
    candidate_index = SelectField('Candidate', [validators.DataRequired()], choices=[])
    base_cover_letter = SelectField('Base Cover Letter', [validators.DataRequired()], choices=[])
    company_name = StringField('Company Name', [validators.DataRequired()])
    job_title = StringField('Job Title', [validators.DataRequired()])
    hiring_manager = StringField('Hiring Manager (optional)')
    job_ad = TextAreaField('Job Ad', [validators.DataRequired()], render_kw={'rows': 15})
    about_company = TextAreaField('About Company (optional)', render_kw={'rows': 10})
    # The address is going to a new form later
    # company_address = TextAreaField("Company's Address", [validators.DataRequired()])

    # Initialize dynamic choices for the ``base_cover_letter`` field
    def __init__(self, *args, **kwargs):
        super(InitialForm, self).__init__(*args, **kwargs)
        
        self.candidate_index.choices = self.get_candidate_choices()
        self.base_cover_letter.choices = self.get_base_cover_letter_choices()

    # Read the candidate options
    @cached_property
    def candidates_data(self):
        # Path candidates JSON file
        candidates_file = 'candidates.json'

        # Read the JSON file
        with open(candidates_file, 'r') as file:
            data = json.load(file)

        # Get all candidates objects
        candidates = [Candidate(candidate['name'], candidate['address']) for candidate in data['candidates']]

        return candidates

    def get_candidate_choices(self):
        # Make the choices as needed for SelectField
        choices = [('', 'Choose one:')] + [(index, str(candidate)) for index, candidate in enumerate(self.candidates_data)]
        
        return choices

    # Read xml files in the folder and create list of choices
    @staticmethod
    def get_base_cover_letter_choices():
        xml_files = [file[:-4] for file in os.listdir('base_cover_letters') if file.endswith('.xml')]
        choices = [('', 'Choose one:')] + [(file, file) for file in xml_files]
        return choices
    
# Class with root page's the forms fields
class CoverLetterTxt(FlaskForm):
    content = TextAreaField('Cover Letter', [validators.DataRequired()])

class PlainTextForm(FlaskForm):
    hiring_manager = StringField('Hiring Manager', [validators.DataRequired()])
    body = TextAreaField('Body', [validators.DataRequired()])
    closing_expression = StringField('Closing expression', [validators.DataRequired()])
    candidate_name = StringField('Candidate', [validators.DataRequired()])

    def set_default_values(self, data : dict):
        self.hiring_manager.data = data['hiring_manager']
        self.body.data = data['body']
        self.closing_expression.data = data['closing_expression']
        self.candidate_name.data = data['candidate_name']

class PdfForm(FlaskForm):
    company_address = TextAreaField('Company Address', [validators.DataRequired()])