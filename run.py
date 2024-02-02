from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import xml.etree.ElementTree as ET
import re
from forms import InitialForm, PlainTextForm
from cover_letter_processing import CoverLetter
from flask import send_from_directory

app = Flask(__name__)
# We are using ``Flask-WTF`` in ``forms``, so CSRF protection is automatically enabled
app.secret_key = 'your_very_secret_key_here'
# It can be desabled by uncommenting the following line:
# app.config['WTF_CSRF_ENABLED'] = False

# Root page, where the details about the candidate, company and job ad should be entered
@app.route('/', methods=['GET', 'POST'])
def home():
    # Create forms
    initial_form = InitialForm()
    plain_txt_form = PlainTextForm()

    if request.method == 'GET':
        # Check if session data exists and pass it to the template or handle it as needed
        stored_data = session.get('cover_letter_data', None)
        return render_template('main.html', initial_form=initial_form, plain_txt_form=plain_txt_form, stored_data=stored_data)

    if initial_form.validate_on_submit():
        # Process the initial_form data; it resets all entries in cover_letter.data
        cover_letter = CoverLetter()
        cover_letter.process_initial_form(initial_form)

        # Temporary, to save money with the openai api when testing
        cover_letter.data['body'] = 'Yaaaaahoooooo!!!'

        # Saves the processed data
        session['cover_letter_data'] = cover_letter.data

        # Show new part of the 
        return redirect(url_for('home'))

        data_for_next_form = {
            'hiring_manager': cover_letter.hiring_manager,
            'cover_letter_body': "xxx",
            'closing_expression': cover_letter.closing_expression,
            'candidate': cover_letter.candidate_name,
        }

        return jsonify(data_for_next_form)

        # print("Create gpt cover letter")
        # cover_letter.create_cover_letter()
        # print("Create latex files")
        # cover_letter.create_latex_files()

        # latex_directory = cover_letter.latex_directory
        # filename = "CoverLetter.pdf"

        # return send_from_directory(directory=latex_directory, path=filename, as_attachment=False)

    elif request.method == 'GET':
        return render_template('main.html', initial_form=initial_form, plain_txt_form=plain_txt_form)

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

