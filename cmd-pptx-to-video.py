import make_video
import argparse

# Parse arguments
parser = argparse.ArgumentParser(description='Convert pptx to video')
parser.add_argument('pptx_file', help='pptx file')
parser.add_argument('output_file', help='output video file, in mp4 format')
args = parser.parse_args()

# Check pptx file exists
import os
if not os.path.exists(args.pptx_file):
    print(f'File {args.pptx_file} not found')
    exit(1)

# make video
make_video.pptx_to_video(args.pptx_file, args.output_file)
