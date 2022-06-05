class WebInterface:
    # import

    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def index(self):
        return 'Hello world'


if __name__ == '__main__':
    webInterface = WebInterface()
    webInterface.app.run(debug=True, port=80, host='0.0.0.0')




