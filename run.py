from flask import Flask, request, render_template, render_template_string

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

if __name__ == '__main__':
    app.run(debug=True)

