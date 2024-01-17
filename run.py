from flask import Flask, request, render_template, render_template_string
import xml.etree.ElementTree as ET
import re

app = Flask(__name__)

# HTML template for the web page
html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Form Page</title>
    </head>
    <body>
        <form method="POST">
            Name: <input type="text" name="name"><br>
            Summary: <textarea name="summary"></textarea><br>
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
'''

# Route for handling the root page
@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Save form data into variables
        name = request.form['name']
        summary = request.form['summary']
        print(f"Name: {name}, Summary: {summary}")  # You can process the data as needed
        return f"Received: Name - {name}, Summary - {summary}"
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
        # Make the tag name more readable
        label = decamelize(element.tag)
        # Split the text into paragraphs and strip each paragraph
        paragraphs = [para.strip() for para in element.text.split('\n') if para.strip()]
        value = '\n'.join(paragraphs)
        form_data.append({
            'label': label,
            'value': value 
        })

    # Pass the data to the template
    return render_template('test.html', form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)

