import json, base64
from pathlib import Path
import json, os
from scipy.io import wavfile


def loop_len(wav):
    if os.path.exists(wav):
        return round(len(wavfile.read(wav)[1]) / 44100, 4)
    return json.load(open('loops.json'))[os.path.basename(wav)[:-4]]

def build_page(data, songs, title, out_path, pause_wav, title_wav='ch_title.wav'):
    s = Path('chapter_engine.html').read_text().replace('__TITLE__', title)
    enc = {k: base64.b64encode(open(v, 'rb').read()).decode() for k, v in songs.items()}
    loops = {'title': loop_len(title_wav), 'pause': loop_len(pause_wav), 'main': 9999}
    out = s.replace('__DATA__', json.dumps(data, separators=(',', ':'))).replace('__SONGS__', json.dumps(enc, separators=(',', ':'))).replace('__LOOPS__', json.dumps(loops))
    Path(out_path).write_text(out)
    Path('check.js').write_text(out.split('<script>')[1].split('</script>')[0])
    return round(len(out) / 1e6, 2)
