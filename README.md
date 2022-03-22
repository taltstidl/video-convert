# Video Conversion Toolkit

Opinionated preprocessing pipeline for videos built on FFmpeg. It is meant to prepare videos for web hosting and targeted towards usage with [Plyr](https://github.com/sampotts/plyr), a "simple, lightweight, accessible and customizable media player". Most of the functionality should also be useful for other media players.

The pipeline is written in Python and its only dependencies are `ffmpeg-python` and `Pillow`. It is recommended you prepare a virtual environment and install those dependencies there. For a tutorial visit the official [Python Documentation](https://docs.python.org/3/tutorial/venv.html). In addition, the pipeline assumes that FFmpeg is available on your system. If that is not the case, please download the binaries from the [FFmpeg website](https://www.ffmpeg.org/download.html).

The arguments of the pipeline `video-convert.py` are summarized below. An example of how you could execute the script is:

```cmd
$ python video-convert.py -v sample.mp4 -s sample.srt -o sample
```

| Name | Target | Description |
| ---- | ------ | ----------- |
| `-v`, `--video` | Path to `.mp4` file | **Required.** Specifies the location of the input video, which is assumed to be MP4 video with a resolution of 1920x1080 pixels and an approximate frame rate of 30 FPS. |
| `-s`, `--subtitle` | Path to `.srt` file | Optional. Specifies the location of the input subtitles, which are assumed to be in [SubRip](https://en.wikipedia.org/wiki/SubRip) format. This is, for example, the format supported by Kdenlive. |
| `-o`, `--output` | Path to output folder | **Required.** Specified the location for the output files. For additional documentation on the generated content, check below. |

## Generated files

Documentation on generated files will be added at a later point.
