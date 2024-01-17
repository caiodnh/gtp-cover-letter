from flask import Flask, request, render_template
import xml.etree.ElementTree as ET
import re

app = Flask(__name__)

# Route for handling the root page
@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Save form data into variables
        name = request.form['name']
        summary = request.form['summary']
        print(f"Name: {name}, Summary: {summary}")  # Log the received data
        # Respond with received data (for demonstration purposes)
        return f"Received: Name - {name}, Summary - {summary}"
    # Render the main form template on GET request
    return render_template('main.html')

def decamelize(s):
    """Converts a camel case string into a space-separated string."""
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', s)

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

