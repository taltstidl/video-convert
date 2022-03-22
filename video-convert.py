import argparse
import os
from pathlib import Path
from typing import Union

import ffmpeg
from PIL import Image


def check_video(video_path: Union[str, bytes, os.PathLike]) -> Path:
    """ Check input video (.mp4). """
    video_path = Path(video_path)
    if not video_path.exists():
        exit('Video {} does not exist'.format(video_path))
    if not video_path.is_file() or not video_path.suffix == '.mp4':
        exit('Video {} is not a valid video (.mp4)'.format(video_path))
    return video_path


def check_subtitle(subtitle_path: Union[str, bytes, os.PathLike]) -> Path:
    """ Check input subtitles (.srt). """
    subtitle_path = Path(subtitle_path)
    if not subtitle_path.exists():
        exit('Subtitle {} does not exist'.format(subtitle_path))
    if not subtitle_path.is_file() or not subtitle_path.suffix == '.srt':
        exit('Subtitle {} is not a valid subtitle (.srt)'.format(subtitle_path))
    return subtitle_path


def check_output(output_path: Union[str, bytes, os.PathLike]) -> Path:
    """ Check output folder. """
    output_path = Path(output_path)
    if not output_path.exists():
        output_path.mkdir(parents=True)
    if not output_path.is_dir() or any(output_path.iterdir()):
        exit('Output folder {} is not an empty directory'.format(output_path))
    return output_path


def rescale_video(in_path: Path, out_path: Path, height: int):
    """ Rescale video to requested height using ffmpeg. """
    flags = {
        'vf': 'scale=-2:{}'.format(height),  # Rescale
        'movflags': 'faststart',  # Metadata at front
    }
    ffmpeg.input(str(in_path)) \
        .output(str(out_path), **flags) \
        .run()


def convert_srt_to_vtt(in_path: Path, out_path: Path):
    """ Convert .srt subtitles by Kdenlive to .vtt files for web. """
    ffmpeg.input(str(in_path)) \
        .output(str(out_path)) \
        .run()


def extract_thumbnails(in_path: Path, out_path: Path, height: int):
    """ Extract thumbnail images of requested height using ffmpeg. """
    flags = {
        'vf': 'fps=1,scale=-1:{}'.format(height),  # One frame per second, rescale
    }
    ffmpeg.input(str(in_path)) \
        .output(str(out_path), **flags) \
        .run()


def extract_poster(in_path: Path, out_path: Path):
    """ Extract poster image at the beginning using ffmpeg. """
    ffmpeg.input(str(in_path), ss=1) \
        .output(str(out_path), vframes=1) \
        .run()


def format_timestamp(seconds: int) -> str:
    """ Format timestamp compatible with .vtt format. """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return '{:02d}:{:02d}:{:02d}.000'.format(h, m, s)


def create_thumbnails(path: Path, height: int, grid: int):
    """ Create thumbnail sprites and associated .vtt file. """
    width = round(height * 16 / 9)
    images = sorted(path.iterdir())
    thumbs_vtt = open(path / '{}p-thumbs.vtt'.format(height), 'w')
    thumbs_vtt.write('WEBVTT\n')
    sprite_i, sprite = 0, None
    for i, image in enumerate(images):
        if i % (grid * grid) == 0:  # Create new sprite
            sprite_i += 1
            sprite = Image.new('RGB', size=(grid * width, grid * height))
        j = i % (grid * grid)  # Sub-index within grid
        x, y = j % grid * width, j // grid * height  # Position of thumbnail within grid
        thumbs_vtt.write('\n')
        thumbs_vtt.write('{} --> {}\n'.format(format_timestamp(i), format_timestamp(i + 1)))
        thumbs_vtt.write('{}p-{:03d}.jpg#xywh={},{},{},{}\n'.format(height, sprite_i, x, y, width, height))
        sprite.paste(Image.open(image), box=(x, y))
        if (i + 1) % (grid * grid) == 0 or (i + 1) == len(images):  # Save sprite
            sprite.save(path / '{}p-{:03d}.jpg'.format(height, sprite_i))
    thumbs_vtt.close()


def main():
    # Get command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', type=str, required=True, help='Input video (.mp4)')
    parser.add_argument('-s', '--subtitle', required=True, type=str, help='Input subtitles (.srt)')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output folder')
    args = parser.parse_args()
    # Check command line arguments
    video = check_video(args.video)
    subtitle = check_subtitle(args.subtitle)
    output = check_output(args.output)
    # Generate derivative videos
    rescale_video(video, output / '1080p.mp4', 1080)
    rescale_video(video, output / '720p.mp4', 720)
    rescale_video(video, output / '576p.mp4', 576)
    # Extract thumbnails
    (output / '240p').mkdir()
    extract_thumbnails(video, output / '240p' / 'frame%03d.png', 240)
    create_thumbnails(output / '240p', 240, 5)
    (output / '100p').mkdir()
    extract_thumbnails(video, output / '100p' / 'frame%03d.png', 100)
    create_thumbnails(output / '100p', 100, 7)
    # Extract poster
    extract_poster(video, output / 'poster.jpg')
    # Convert .srt subtitles to .vtt subtitles suitable for web
    convert_srt_to_vtt(subtitle, output / 'subtitles.vtt')


if __name__ == '__main__':
    main()
