from app import create_app, socketio

app = create_app()

# Push an application context by default for gunicorn
ctx = app.app_context()
ctx.push()

if __name__ == '__main__':
    socketio.run(app, debug=True)