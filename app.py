from flask import Flask, request, render_template, Response
from ollama import chat

app = Flask(__name__)

def system():
    return {
        'role': 'system',
        'content': (
            "You are Min Yoongi from the boy band BTS."
            "You are non-challant but also secretly caring."
            "Your birthday is March 9, 1995."
        )
    }


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_with_ai():
    user_message = request.form.get('message', '')

    if not user_message:
        return Response("Error: No message provided", status=400, content_type='text/plain')

    def generate_response():
        messages = [system(), {'role': 'user', 'content': user_message}]
        try:
            stream = chat(
                model='llama3.2',
                messages=messages,
                stream=True,
            )
            for chunk in stream:
                yield chunk['message']['content']
        except Exception as e:
            yield f"\nError: {str(e)}"

    return Response(generate_response(), content_type='text/plain')




if __name__ == '__main__':
    app.run(debug=True, port=5035, host='::')
