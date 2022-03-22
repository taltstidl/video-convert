# Video Conversion Toolkit

Opinionated preprocessing pipeline for videos built on FFmpeg. It is meant to prepare videos for web hosting and targeted towards usage with [Plyr](https://github.com/sampotts/plyr), a "simple, lightweight, accessible and customizable media player". Most of the functionality should also be useful for other media players.

The pipeline is written in Python and its only dependencies are `ffmpeg-python` and `Pillow`. It is recommended you prepare a virtual environment and install those dependencies there. For a tutorial visit the official [Python Documentation](https://docs.python.org/3/tutorial/venv.html). In addition, the pipeline assumes that FFmpeg is available on your system. If that is not the case, please download the binaries from the [FFmpeg website](https://www.ffmpeg.org/download.html).

The arguments of the pipeline `video-convert.py` are summarized below. An example of how you could execute the script is:

```cmd
$ python video-convert.py -v sample.mp4 -s sample.srt -o sample
```

| Name | Value | Description |
| ---- | ------ | ----------- |
| `-v`, `--video` | Path to `.mp4` file | **Required.** Specifies the location of the input video, which is assumed to be a MP4 video with a resolution of 1920x1080 pixels and an approximate frame rate of 30 FPS. |
| `-s`, `--subtitle` | Path to `.srt` file | Optional. Specifies the location of the input subtitles, which are assumed to be in [SubRip](https://en.wikipedia.org/wiki/SubRip) format. This is, for example, the format supported by Kdenlive. |
| `-o`, `--output` | Path to new folder | **Required.** Specifies the location for the output files. For additional documentation on the generated files within that folder, check below. |

## Generated files

For each video, the following file structure will be generated in the output folder.

* `576p.mp4`: A MP4 video with a resolution of 1024x576 pixels.
* `720p.mp4`: A MP4 video with a resolution of 1280x720 pixels.
* `1080p.mp4`: A MP4 video with a resolution of 1920x1080 pixels (original size).
* `subtitles.vtt`: The subtitles in [WebVTT](https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API) format. Missing if input not specified.
* `poster.jpg`: The full size thumbnail grabbed 1 second into the video.
* `100p`: Folder for small size preview thumbnails.
  * `frame%03d.png`: The small 178x100 thumbnails taken from the video at a rate of 1 per second.
  * `100p-%03d.jpg`: The 7x7 grid sprites generated from the thumbnails.
  * `100p-thumbs.vtt`: The index file referencing the sprites. Compatible with the [preview thumbnails](https://github.com/sampotts/plyr#preview-thumbnails) feature.
* `240p`: Folder for medium size preview thumbnails.
  * `frame%03d.png`: The medium 427x240 thumbnails taken from the video at a rate of 1 per second.
  * `240p-%03d.jpg`: The 5x5 grid sprites generated from the thumbnails.
  * `240p-thumbs.vtt`: The index file referencing the sprites. Compatible with the [preview thumbnails](https://github.com/sampotts/plyr#preview-thumbnails) feature.
