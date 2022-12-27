from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, after_this_request
from pytube import YouTube
from moviepy import editor
import shutil
import os

app = Flask(__name__)

app.secret_key = "fb4ab1huindasckn23e12ewq8978tg2iubcd9"

begin = True


# @app.route('/', methods=['POST', "GET"])
# def hello_world():
#     start = True
#     if request.method == "POST":
#         email = request.form.get('email').lower()
#         passwd = request.form.get('passwd')
#         if email == 'leia@comadre.com' and passwd == "madison":
#             return redirect(url_for('music'))
#         else:
#             flash("The Password  or Email are Incorrect Please Try again")
#             return redirect(url_for('hello_world'))
#
#     return render_template('index.html', start=start, begin=begin)


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
            new_path = f"/Users/sammy/PycharmProjects/flask_comadre_music/{name_song}.mp3"
            shutil.move(path_mp3, new_path)

            @after_this_request
            def delete_file(response):
                os.remove(new_path)
                return response

            return send_file(new_path, mimetype='mp3', as_attachment=True)

    return render_template('index.html', begin=begin)


if __name__ == '__main__':
    app.run()
