from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests

app = Flask(_name_)
CORS(app)

WEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"

def predict_crop():
    return {
        "crop": "Wheat",
        "disease": "Healthy",
        "suggestion": "Maintain irrigation and use balanced fertilizer"
    }

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Krishi Mitra</title>
<style>
body { font-family: Arial; background:#e8f5e9; padding:20px }
button { background:green; color:white; padding:8px; border:none; margin:5px }
input { padding:6px; margin:5px }
video { width:300px; border:2px solid green }
</style>
</head>

<body>
<h2>🌱 Krishi Mitra</h2>

<h3>Crop Scan</h3>
<input type="file" id="img">
<button onclick="scan()">Scan</button>
<p id="scanResult"></p>

<h3>Weather Check</h3>
<input type="text" id="city" placeholder="Enter city">
<button onclick="weather()">Check</button>
<p id="weatherResult"></p>

<h3>Query to Krishi Vibhag</h3>
<input type="text" id="query" placeholder="Ask question">
<button onclick="ask()">Send</button>
<p id="response"></p>

<h3>Video Call</h3>
<button onclick="call()">Start Video</button><br><br>
<video id="video" autoplay></video>

<script>
function scan(){
    let formData = new FormData();
    formData.append("image", document.getElementById("img").files[0]);

    fetch("/scan", {method:"POST", body:formData})
    .then(r=>r.json())
    .then(d=>{
        document.getElementById("scanResult").innerText =
        "Crop: "+d.crop+" | Disease: "+d.disease+" | Advice: "+d.suggestion;
    })
}

function weather(){
    let city = document.getElementById("city").value;
    fetch("/weather?city="+city)
    .then(r=>r.json())
    .then(d=>{
        document.getElementById("weatherResult").innerText =
        "Temp: "+d.main.temp+"°C , "+d.weather[0].description;
    })
}

function ask(){
    fetch("/query", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({question:document.getElementById("query").value})
    })
    .then(r=>r.json())
    .then(d=>{
        document.getElementById("response").innerText = d.response;
    })
}

function call(){
    navigator.mediaDevices.getUserMedia({video:true,audio:true})
    .then(stream=>{
        document.getElementById("video").srcObject = stream;
    })
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/scan", methods=["POST"])
def scan():
    return jsonify(predict_crop())

@app.route("/weather")
def weather():
    city = request.args.get("city")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    return jsonify(requests.get(url).json())

@app.route("/query", methods=["POST"])
def query():
    return jsonify({"response":"Krishi Vibhag officer will contact you via video call."})

if _name_ == "_main_":
    app.run(debug=True)