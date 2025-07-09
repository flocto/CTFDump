from flask import Flask, request
from time import sleep

app = Flask(__name__)

@app.route('/get_file')
def get_file():
    file_name = request.args.get('file')
    if file_name:
        file_name = file_name[1:]
        if file_name == 'wait.txt':
            # Simulate a delay for the file request
            sleep(5)
        elif file_name.endswith('TestStorage.jar'):
            f = open('TestStorage.jar', 'rb')
            content = f.read()
            f.close()
            return content, 200, {'Content-Type': 'application/java-archive'}
        print(f"Requested file: {file_name}")
        return f"File requested: {file_name}"
    else:
        return "No file parameter provided", 400

if __name__ == '__main__':
    app.run(debug=False)