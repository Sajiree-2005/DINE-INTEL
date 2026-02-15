from flask import Flask, render_template, request, jsonify
from knowledge_base import knowledge
from difflib import get_close_matches

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ---------------- Tableau Visualization Pages ----------------
@app.route("/viz1")
def viz1():
    return render_template("viz1.html")

@app.route("/viz2")
def viz2():
    return render_template("viz2.html")

@app.route("/viz3")
def viz3():
    return render_template("viz3.html")

@app.route("/viz4")
def viz4():
    return render_template("viz4.html")

@app.route("/viz5")
def viz5():
    return render_template("viz5.html")

# ---------------- Chatbot Endpoint ----------------
@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_message = request.json.get("message", "").lower().strip()
    
    # Attempt exact keyword match first
    for key in knowledge:
        if key in user_message:
            return jsonify({"reply": knowledge[key]})

    # Fuzzy match with keywords (for typos / partial phrases)
    matches = get_close_matches(user_message, knowledge.keys(), n=1, cutoff=0.6)
    if matches:
        return jsonify({"reply": knowledge[matches[0]]})

    # Default fallback response
    fallback = (
        "Sorry, I didn't understand that. "
        "Please contact a DINE-INTEL employee for further assistance."
    )
    return jsonify({"reply": fallback})

if __name__ == "__main__":
    app.run(debug=True)
