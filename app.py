from flask import Flask,render_template, redirect,url_for,send_file,request,jsonify,make_response
import os,sys
from pydub import AudioSegment
from pydub.utils import which

app=Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    return render_template("index.html")

app.config["UPLOADS"] = "static/upload"
app.config["CONVERTED"] = "static/converted"

AudioSegment.converter = which("ffmpeg")


@app.route("/upload-audio", methods=["GET", "POST"])
def upload_audio():
    try:
        if request.method == "POST":
            audio = request.files["audio"]
            audio.save(os.path.join(app.config["UPLOADS"], audio.filename))
            print(audio)
            if request.files:
                if request.form['format'] == 'wav':
                    song = AudioSegment.from_file(os.path.join(app.config["UPLOADS"], audio.filename)).export("static/converted/converted.wav", format="wav")
                    print("DONE!")
                    return send_file(app.config["CONVERTED"]+"/converted.wav", as_attachment=True)
                    # return "converting....."
                else:
                    return "Format Unsupported"
    except IsADirectoryError:
        return redirect(url_for("index"))
if __name__ == '__main__':
    app.run(debug=True)