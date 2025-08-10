import re
import textwrap
from flask import Flask, request, render_template_string

# Correct way to initialize Flask
app = Flask(__name__)

# Template for the Python code we will display
CODE_TO_GENERATE = textwrap.dedent("""\
import re

# The input string containing the phone number(s)
input_string = {input_string_literal}

# Regex pattern to find a 10-digit Indian mobile number starting with 6-9
pattern = {pattern_literal}

# Find all occurrences of the pattern in the input string
matches = re.findall(pattern, input_string)

if matches:
    for phone_number in matches:
        print(f"Extracted Phone Number: {{phone_number}}")
else:
    print("No phone number found.")
""")

# HTML for the front-end
HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Phone Number Code Extractor</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 2rem; background:#f4f4f9; color:#222 }
    textarea { width: 90%; max-width:600px; height:90px; padding:10px; font-size:15px; border-radius:6px; border:1px solid #ccc; }
    input[type=submit]{ padding:10px 18px; border-radius:6px; background:#007bff; color:#fff; border:none; cursor:pointer }
    pre{ background:#2d2d2d; color:#f8f8f2; padding:12px; border-radius:6px; overflow:auto; white-space:pre-wrap }
  </style>
</head>
<body>
  <h2>Enter text containing a 10-digit Indian mobile number</h2>
  <form method="post">
    <textarea name="user_input" placeholder="e.g., You can reach me at 9876543210">{{ input_text }}</textarea><br><br>
    <input type="submit" value="Generate Python Code">
  </form>

  {% if matches %}
    <h3>Phone numbers found:</h3>
    <p>{{ matches | join(', ') }}</p>
  {% endif %}

  {% if generated_code %}
    <h3>Generated Python Code:</h3>
    <pre><code>{{ generated_code }}</code></pre>
  {% endif %}
</body>
</html>
"""

# Main route
@app.route('/', methods=['GET', 'POST'])
def home():
    generated_code = ""
    input_text = ""
    matches = []

    if request.method == 'POST':
        input_text = request.form.get('user_input', '').strip()
        # Updated regex to handle numbers mixed with text (e.g., 9876543210abc)
        phone_pattern = r'(?<!\d)([6-9]\d{9})(?!\d)'

        matches = re.findall(phone_pattern, input_text)

        if matches:
            input_literal = repr(input_text)
            pattern_literal = repr(phone_pattern)
            generated_code = CODE_TO_GENERATE.format(
                input_string_literal=input_literal,
                pattern_literal=pattern_literal
            )
        elif input_text:
            generated_code = "# No 10-digit phone number found in the provided text."

    return render_template_string(
        HTML_TEMPLATE,
        generated_code=generated_code,
        input_text=input_text,
        matches=matches
    )

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
