from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['endpoint'])

@app.route('/')
def index():
    REQUEST_COUNT.labels(endpoint='/').inc()
    raise Exception("Bug volontaire pour tester le rollback !")  # 💥

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)