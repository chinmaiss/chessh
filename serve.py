# from flask import Flask, request, render_template, Response #import main Flask class and request object

# app = Flask(__name__) #create the Flask app

# def event_stream():
#     pubsub = red.pubsub()
#     pubsub.subscribe('chat')
#     for message in pubsub.listen():
#         print(message)
#         yield 'data: %s\n\n' % message['data']

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/query-example')
# def query_example():
#     return 'Todo...'

# @app.route('/form-example')
# def formexample():
#     return 'Todo...'

# @app.route('/json-example')
# def jsonexample():
#     return 'Todo...'

# @app.route('/stream')
# def stream():
#     return Response(event_stream(),mimetype="text/event-stream")


# # server sude stuff that might work
##BEGIN------------------------------------------------------------------------
# def get_message():
#     '''this could be any function that blocks until data is ready'''
#     time.sleep(1.0)
#     s = time.ctime(time.time())
#     return s

# @app.route('/')
# def root():
#     return render_template('index.html')

# @app.route('/stream')
# def stream():
#     def eventStream():
#         while True:
#             # wait for source data to be available, then push it
#             yield 'data: {}\n\n'.format(get_message())
#     return Response(eventStream(), mimetype="text/event-stream")
##END----------------------------------------------------------------------------
# # js
# # begin 
# var targetContainer = document.getElementById("target_div");
# var eventSource = new EventSource("/stream")
#   eventSource.onmessage = function(e) {
#   targetContainer.innerHTML = e.data;
# };
# # end

# if __name__ == '__main__':
#     app.run(debug=True, threaded = True, port=5000) #run app in debug mode on port 5000


#chat app (may impliment in real chess)
  
#!/usr/bin/env python
import datetime
import flask
import redis


app = flask.Flask(__name__)
app.secret_key = 'asdf'
red = redis.StrictRedis()


def event_stream():
    pubsub = red.pubsub()
    pubsub.subscribe('chat')
    # TODO: handle client disconnection.
    for message in pubsub.listen():
        print(message)
        yield 'data: %s\n\n' % message['data']


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        flask.session['user'] = flask.request.form['user']
        return flask.redirect('/')
    return '<form action="" method="post">user: <input name="user">'


@app.route('/post', methods=['POST'])
def post():
    message = flask.request.form['message']
    user = flask.session.get('user', 'anonymous')
    now = datetime.datetime.now().replace(microsecond=0).time()
    red.publish('chat', u'[%s] %s: %s' % (now.isoformat(), user, message))
    return flask.Response(status=204)


@app.route('/stream')
def stream():
    return flask.Response(event_stream(),
                          mimetype="text/event-stream")


@app.route('/')
def home():
    if 'user' not in flask.session:
        return flask.redirect('/login')
    return """
        <!doctype html>
        <title>chat</title>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
        <style>body { max-width: 500px; margin: auto; padding: 1em; background: black; color: #fff; font: 16px/1.6 menlo, monospace; }</style>
        <p><b>hi, %s!</b></p>
        <p>Message: <input id="in" /></p>
        <pre id="out"></pre>
        <script>
            function sse() {
                var source = new EventSource('/stream');
                var out = document.getElementById('out');
                source.onmessage = function(e) {
                    // XSS in chat is fun
                    out.innerHTML =  e.data + '\\n' + out.innerHTML;
                };
            }
            $('#in').keyup(function(e){
                if (e.keyCode == 13) {
                    $.post('/post', {'message': $(this).val()});
                    $(this).val('');
                }
            });
            sse();
        </script>
    """ % flask.session['user']


if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)