import time
import pysrt
import process_text

# Create srt from notes
def make_srt(notes, srt_file):
    subtitle = pysrt.SubRipFile()
    ts = 0
    for i, note in enumerate(notes):
        start = ts
        ts += int(note['duration']*1000)
        end = ts
        subtitle.append(pysrt.SubRipItem(i, start=start, end=end, text=note['text']))
    subtitle.save(srt_file)
    pass

# Translate srt to other language
def translate_srt(srt_file, out_file, from_lang, to_lang):
    import googletrans
    srt = pysrt.open(srt_file)
    translator = googletrans.Translator()
    print(f"Translating {srt_file} from {from_lang} to {to_lang}...")
    for sub in srt:
        if sub.text:    # skip empty subtitles
            try_count = 0
            while try_count < 5:
                time.sleep(0.3)
                try:
                    sub.text = translator.translate(sub.text, dest=to_lang, src=from_lang).text
                    break   # break while loop
                except:
                    print(f"Error translating \"{sub.text}\" from {from_lang} to {to_lang}, retrying...")
                    time.sleep(1.1)
                    try_count += 1
                    pass
    srt.save(out_file)
    pass


