from flask import Flask, request, render_template, redirect, url_for, jsonify
import xml.etree.ElementTree as ET
import re
from forms import InitialForm, PlainTextForm
from cover_letter_processing import CoverLetterData
from flask import send_from_directory

app = Flask(__name__)
# We are using ``Flask-WTF`` in ``forms``, so CSRF protection is automatically enabled
app.secret_key = 'your_very_secret_key_here'
# It can be desabled by uncommenting the following line:
# app.config['WTF_CSRF_ENABLED'] = False

# A global variable that will be used since the application is local and single-user
cover_letter_data = None

# Root page, where the details about the candidate, company and job ad should be entered
@app.route('/', methods=['GET', 'POST'])
def home():
    form = InitialForm()
    my_form = PlainTextForm()

    if request.method == 'POST' and form.validate_on_submit():
        cover_letter_data = CoverLetterData(form)
        print("oiiii")
        print(cover_letter_data.base_cover_letter_content)

        pre_filled = "Hi! My name Monster Truck."

        return jsonify({'pre_filled': pre_filled})

        # print("Create gpt cover letter")
        # cover_letter.create_cover_letter()
        # print("Create latex files")
        # cover_letter.create_latex_files()

        # latex_directory = cover_letter.latex_directory
        # filename = "CoverLetter.pdf"

        # return send_from_directory(directory=latex_directory, path=filename, as_attachment=False)

    elif request.method == 'GET':
        return render_template('main.html', form=form, my_form=my_form)

@app.route('/cover_letter_as_txt', methods=['GET', 'POST'])
def cover_letter_as_txt():
    form = PlainTextForm(content=cover_letter_data.base_cover_letter_content)
    return render_template('cover_letter_as_txt.html', form = form)

# Function used in ``/test`` to make the form labels more readable
def decamelize(s):
    """Converts a camel case string into a space-separated string."""
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', s)

# Page showing a base cover letter xml file
@app.route('/test')
def test():
    # Parse the XML file
    tree = ET.parse('base_cover_letters/software_engineer.xml')
    root = tree.getroot()

    # Create a list of dictionaries for each XML element
    form_data = []
    for element in root:
        # Convert camel case tag name to a more readable format
        label = decamelize(element.tag)
        # Process text content: split into paragraphs and strip whitespace
        paragraphs = [para.strip() for para in element.text.split('\n') if para.strip()]
        value = '\n'.join(paragraphs)
        form_data.append({
            'label': label,
            'value': value
        })

    # Pass the processed data to the test template
    return render_template('test.html', form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)

