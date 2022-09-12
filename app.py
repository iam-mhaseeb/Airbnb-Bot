from flask import Flask, render_template, request

from main import run

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():  # put application's code here
    if request.method == 'POST':
        host_id = request.form['host_id']
        message = request.form['message']
        users = request.form['users']
        print(host_id)
        print(message)
        print(users)
        try:
            run([host_id], message)
        except Exception as e:
            raise e

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
