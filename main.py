from restfull.video.views import video_blueprint
from restfull import app

app.register_blueprint(video_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
