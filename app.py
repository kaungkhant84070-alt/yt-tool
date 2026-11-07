from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Template folder မပါဘဲ တိုက်ရိုက်ဖတ်မယ်
    return send_file('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': 'best[ext=mp4]/best',
    }
    
    os.makedirs('downloads', exist_ok=True)
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if not os.path.exists(filename):
                base, ext = os.path.splitext(filename)
                filename = base + '.mp4'
                
            return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(port=5000)