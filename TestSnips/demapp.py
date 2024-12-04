import plotly.express as px
from flask import Flask, Markup, render_template

# Create a Flask app
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    # Create a Plotly bar chart
    fig = px.bar(x=[1, 2, 3], y=[4, 5, 6])

    # Convert the chart to HTML
    chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # Render the template with the chart
    return render_template('home.html', chart_html=Markup(chart_html))

if __name__ == '__main__':
    app.run(debug=True)
