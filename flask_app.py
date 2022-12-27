from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, after_this_request
from pytube import YouTube
from moviepy import editor
import shutil
import os

app = Flask(__name__)

app.secret_key = "SECRET KEY"

begin = True



@app.route('/', methods=['POST', "GET"])
def music():
    if request.method == "POST":
        url_link = request.form.get('link')
        if url_link == "":
            flash("You Need to Enter a link")
            return redirect(url_for("music"))
        else:
            yt = YouTube(url_link)
            name_song = yt.title
            song = yt.streams.get_audio_only()
            my_song = song.download()
            path_mp4 = os.path.abspath(my_song)
            path_mp3 = path_mp4.replace(".mp4", ".mp3")
            convert = editor.AudioFileClip(path_mp4)
            convert.write_audiofile(path_mp3)
            convert.close()
            os.remove(path_mp4)
            new_path = f"/Pathfile/{name_song}.mp3"
            shutil.move(path_mp3, new_path)

            @after_this_request
            def delete_file(response):
                os.remove(new_path)
                return response

            return send_file(new_path, mimetype='mp3', as_attachment=True)

    return render_template('index.html', begin=begin)


if __name__ == '__main__':
    app.run()
