from flask import Flask, render_template, jsonify
import psutil

app = Flask(__name__)

@app.route('/')
def home():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    return render_template("index.html",
                           cpu=cpu,
                           memory=memory,
                           disk=disk)

@app.route('/cpu')
def cpu_data():
    return jsonify({'cpu': psutil.cpu_percent()})

if __name__ == '__main__':
    app.run(debug=True)
