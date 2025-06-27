from flask import Flask, render_template
# from home import home_bp  # Import the blueprint

app = Flask(__name__)

# Register the blueprint
# app.register_blueprint(home_bp)

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/prompt-template-system')
def prompt_template_system():
    return render_template("prompt-template-system_v2.html")

@app.route('/prompt-tracking')
def prompt_tracking():
    return render_template("prompt-tracking.html")
@app.route('/analytics')
def analytics():
    return render_template("analytics.html")



if __name__ == "__main__":
    app.run(debug=True)
