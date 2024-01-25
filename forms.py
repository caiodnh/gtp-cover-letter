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

    def pretty_print(self):
        return f"Name: {self.name} | Address: {self.address}"

# Class with the form fields
class CoverLetterForm(FlaskForm):
    ## Form Definition Section ##

    # ``candidate_index`` and ``base_cover_letter`` are updated below using ``__init__``, ``get_candidate_choices`` and ``get_base_cover_letter_choices``
    candidate_index = SelectField('Candidate', [validators.DataRequired()], choices=[])
    base_cover_letter = SelectField('Base Cover Letter', [validators.DataRequired()], choices=[])
    job_ad = TextAreaField('Job Ad', [validators.DataRequired()])
    company_address = TextAreaField("Company's Address", [validators.DataRequired()])
    company_name = StringField('Company Name', [validators.DataRequired()])
    job_title = StringField('Job Title', [validators.DataRequired()])
    about_company = TextAreaField('About Company (optional)')
    hiring_manager = StringField('Hiring Manager (optional)')

    # Initialize dynamic choices for the ``base_cover_letter`` field
    def __init__(self, *args, **kwargs):
        super(CoverLetterForm, self).__init__(*args, **kwargs)
        
        self.candidate.choices = self.get_candidate_choices()
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
        choices = [('', 'Choose one:')] + [(index, candidate.pretty_print()) for index, candidate in enumerate(self.candidates_data)]
        
        return choices


    # Read xml files in the folder and create list of choices
    @staticmethod
    def get_base_cover_letter_choices():
        xml_files = [file[:-4] for file in os.listdir('base_cover_letters') if file.endswith('.xml')]
        choices = [('', 'Choose one:')] + [(file, file) for file in xml_files]
        return choices
    
    ## Post-Submission Processing Section ##
    # Properties and methods below are for processing and accessing data after form submission

    # Get the contents of the chosen base cover letter
    @property
    def base_cover_letter_content(self):
        with open(f'base_cover_letters/{self.base_cover_letter.data}.xml', 'r') as file:
            lines = file.readlines()  # Read all lines into a list
            if lines and lines[0].startswith('<?xml'):
                return '\n'.join(lines[1:])  # Join all lines except the first one
            else:
                return '\n'.join(lines)  # Join all lines if no XML declaration
            
    # Get the correct string for addressing the hiring manager
    @property
    def hiring_manager_string(self):
        return self.hiring_manager.data or "Hiring Manager"