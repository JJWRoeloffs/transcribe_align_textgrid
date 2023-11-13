# Transcribe Allign TextGrid

A small wrapper package around [whisper-timestamped](https://github.com/linto-ai/whisper-timestamped). Create force-alligned transcription TextGrids from raw audio.

## Installation

## Requirements
* `Python3.8` to `python3.11`.
    * Use the executable `python3.x` on Unix, available in most package managers, or `py -3.x` on Windows.
    * This command line executable of will be referred to as `[python-executable]` for the rest of the instructions
    * Install pip on old python versions with `[python-executable] -m ensurepip --default-pip`
* `ffmpeg` Usually preinstalled on Linux. For windows see instructions for installation on the [whisper repository](https://github.com/openai/whisper)
* `git` Usually preinstalled on Linux. For windows, visit [the git site](https://git-scm.com/download/win).
    * Needed for installation of whisper-timestamped, as it is not available on pypi
    * Note that it needs to be available from the command line; git-bash might not work.

## Installing Torch

Torch, on which Whisper is built, is quite a low-level library, meaning which version you'll need depends on your OS and type of GPU. On Mac and Windows, pip will by default install a non-accelerated CPU version of the library. If you are on Linux, it will presume you have a CUDA-capable (which is to say Nvidia branded) GPU. If you are on Windows and have an Nvidia GPU you can use, or are on Linux and either do not have a GPU or have an AMD GPU, you should check out the more detailed torch installation instructions [here](https://pytorch.org/get-started/locally/).

This should be done *before* installing `transcribe_allign_textgrid` and `whisper_timestamped`.

## Installing
Once the requirements are satisfied, you can install whisper-timestamped and this package:

Whisper-timestamped is not on pypi, so the seperate `git+` install is needed. (If you only want to use the package as a library instead of a cli, whisper-timestamped is not a dependency, and this manual install of ir is not needed.)
```bash
[python-executable] -m pip install git+https://github.com/linto-ai/whisper-timestamped
[python-executable] -m pip install transcribe_allign_textgrid
```

# Running from the command line
Once the application is installed, you can run it with:
```bash
[python-executable] -m transcribe_allign_textgrid [path]
```

here `path` is the path to the audio files.
* If a directory path is passed, all audio files in the directory will be transcribed, and force-alligned transcription textgrids of the same name will be generated in this directory.
* If a file path is passed, a force-alligned transcription textgrid will be generated into the same directory with the same name as the original file.
* If a glob is passed, the glob will be resoled and all matches will be processed as if the files were passed individually
* By default, if a non-audio file is passed, an error is raised. To skip those instead, pass the `--skip` flag.

## Selecting a different model
By default, this will run on the smallest, that is, least accurate and fastest, model, `tiny`. To run with another model, pass it as an argument:
```bash
[python-executable] -m transcribe_allign_textgrid [path] --model [model]
```

The available models are:

|  name  | Parameters | Required VRAM | Relative speed |
|:------:|:----------:|:-------------:|:--------------:|
|  tiny  |    39 M    |     ~1 GB     |      ~32x      |
|  base  |    74 M    |     ~1 GB     |      ~16x      |
| small  |   244 M    |     ~2 GB     |      ~6x       |
| medium |   769 M    |     ~5 GB     |      ~2x       |
| large  |   1550 M   |    ~10 GB     |       1x       |

## Specifying what language to use
By default, the application will try to detect what langage is used automatically. However, you can also specify this manually:
```bash
[python-executable] -m transcribe_allign_textgrid [path] --language [language]

# Or also specifying waht model to use:
[python-executable] -m transcribe_allign_textgrid [path] --model [model] --language [language]
```

To see what languages are available, please see the [tokenizer.py](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py) file in the Whisper source (Yes, the OpenAI team themselves recommends finding it this way, too.)

# Using as a library
The tool can also be used as a library. It exports one function: `whisper_to_textgrid()` Which takes in a transcription object (nested dict) from [whisper-timestamped](https://github.com/linto-ai/whisper-timestamped) and returns a Textgrid object from [praatio](https://github.com/timmahrt/praatIO). The typical Json output from whisper-timestamped works, too.

This library part of the package does not depend on whisper-timestamped, to make it fully installable and usable as a requirement via pipy.

# Output
The output TextGrids have four TextGridTiers:
* `segments_text` The text in a given segment (Speaker's turn)
* `segments_confidence` The confidence the model has that this is the correct labeling and segmentation for the segment
* `words_text` The text of a given word
* `words_confidence` The confidence the model has that this is the corrent labeling and segmentation for this word.

If one of these tiers would have been completely empty per the output of whisper-timestamped, to statisfy Praat's error handeling, a tier with an empty interval (0.0, 0.1) is generated.

In praat, it will look a little like this:
<p allign="center">
  <img src=".assets/sample_output.png" />
</p>

# Development
The package is quite trivial, but, if you do want work on it, here are some instructions


## Style
All code is formatted with the [Black](https://github.com/psf/black) code-formatter. As for casing, python standards are used except in cases where dependencies don't.

I am dyslectic, and quite likely to make spelling errors in variables. If you find any, don't hesitate to send me a pull request!

## Running Tests
After clonging the repository, moving into it, and installing `pytest` and `pytest-cov` with pip, run tests with:
```bash
# Install current version of package locally to be able to test it.
[python-executable] -m pip install -e .

[python-executable] -m pytest --cov=transcribe_allign_textgrid tests/
```
