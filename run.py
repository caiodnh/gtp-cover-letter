from flask import Flask, request, render_template
import xml.etree.ElementTree as ET
import re
from forms import CoverLetterForm
from cover_letter_processing import CoverLetterData

app = Flask(__name__)
# We are using ``Flask-WTF`` in ``forms``, so CSRF protection is automatically enabled
app.secret_key = 'your_very_secret_key_here'
# It can be desabled by uncommenting the following line:
# app.config['WTF_CSRF_ENABLED'] = False

# Root page, where the details about the candidate, company and job ad should be entered
@app.route('/', methods=['GET', 'POST'])
def home():
    form = CoverLetterForm()

    if request.method == 'POST' and form.validate_on_submit():
        cover_letter = CoverLetterData(form)
        cover_letter.create_cover_letter()
        return cover_letter.new_cover_letter 
    
    return render_template('main.html', form=form)

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

