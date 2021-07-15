from flask import Flask,render_template, redirect,url_for,send_file,request,flash
import os,sys
from pydub import AudioSegment
from pydub.utils import which

app=Flask(__name__)
app.secret_key="8f2cfea6b4c54e5b9cb21f6f70b7b8ce"


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
                    store= send_file(app.config["CONVERTED"]+"/converted.wav", as_attachment=True)
                    # return "converting....."
                    #flash("Successfully Converted") 
                    #return redirect(url_for("index"))
                    return store

                else:
                    return "Format Unsupported"
    except IsADirectoryError:
        flash("Error occured, try again!")
        return redirect(url_for("index"))
    #finally:
          #flash("Successfully Converted....")
if __name__ == '__main__':
    app.run(debug=True)