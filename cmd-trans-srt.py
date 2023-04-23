import os
import make_srt
import argparse

SUPPORT_LANGS = ['af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb', 'ny', 'zh', 'zh-cn', 'zh-tw', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'tl', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'he', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jw', 'kn', 'kk', 'km', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'or', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'te', 'th', 'tr', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu']

# Get input arguments
parse = argparse.ArgumentParser()
parse.add_argument('pptx_file', help='pptx file to translate')
parse.add_argument('output_dir', help='output directory')
parse.add_argument('-sl', '--source-lang', help='language of input srt file', default='en')
parse.add_argument('-tl', '--target-langs', help='target languages', default='zh,es,en,pt,ru,ja,de,ko,fr,tr,vi,th,id')
args = parse.parse_args()
pptx_file = args.pptx_file
output_dir = args.output_dir
source_lang = args.source_lang
target_langs = args.target_langs.split(',')

# Check input arguments
assert source_lang in SUPPORT_LANGS, f'Unsupported source language: {source_lang}'
assert set(target_langs).issubset(set(SUPPORT_LANGS)), f'Unsupported target language: {set(target_langs).difference(set(SUPPORT_LANGS))}'

# Create directory if not exist
os.makedirs(output_dir, exist_ok=True)
base_name = os.path.basename(pptx_file)

# Translate srt to popular languages
for lang in target_langs:
    out_file = f'{output_dir}/{base_name}.{lang}'
    # googletrans package does not support zh, use zh-cn instead
    if (lang == 'zh'):
        lang = 'zh-cn'
    if source_lang == lang:
        os.system(f'cp {pptx_file} {out_file}')
    else:
        make_srt.translate_srt(pptx_file, out_file, source_lang, lang)

