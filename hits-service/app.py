from flask import Flask, request
import redis
import os

redis = redis.Redis(decode_responses=True, password=os.environ["DB_PASSWORD"], host=os.environ["DB_HOST"])
app = Flask(__name__)

@app.route('/api/hits/<id>')
def get(id):
    return {"status": "0", "hits": str(redis.get(id)), "total": str(redis.get("total"))}

@app.route('/api/hits', methods=['POST'])
def hit():
    data = request.json

    redis.setnx(data['id'], 0)
    redis.incr(data['id'], 1)

    redis.setnx('total', 0)
    redis.incr('total', 1)

    return {"status": "0", "data": "ok"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)