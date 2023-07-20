# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2022-present Artic

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

__author__ = 'Artic'
__version__ = '1.0.0'
__description__ = 'A simple .m3u8 video downloader.'

import os
from utils import *

EXIT_FAILURE: int = 1
EXIT_SUCCESS: int = 0

class FFMPEGnotInstalled(Exception): ...

class color:
    VIOLET: str = '\033[95m'
    CYAN: str = '\033[96m'
    DARK_CYAN: str = '\033[36m'
    BLUE: str = '\033[94m'
    GREEN: str = '\033[92m'
    YELLOW: str = '\033[93m'
    RED: str = '\033[91m'
    WHITE: str = '\033[37m'
    BLACK: str = '\033[30m'
    GRAY: str = '\033[38;2;125;125;125m'
    MAGENTA: str = '\033[35m'
    BOLD: str = '\033[1m'
    DIM: str = '\033[2m'
    NORMAL: str = '\033[22m'
    UNDERLINED: str = '\033[4m'
    STOP: str = '\033[0m'


def main() -> None:
    os.system("cls" if os.name == "nt" else "clear")
    print(f'      {color.GREEN}{color.BOLD}M3U8 VIDEO DOWNLOADER{color.STOP}\n({color.DARK_CYAN}{color.UNDERLINED}https://github.com/ArticOff/.m3u8{color.STOP})\n')
    if not ffmpeg_isInstalled():
        print(f"[ {color.RED}!{color.STOP} ] FFMPEG is not installed. (https://ffmpeg.org/download.html)")
        return exit(EXIT_FAILURE)

    m3u8: str = input(f"[ {color.MAGENTA}?{color.STOP} ] {color.GRAY}URL of the video (.m3u8 or .ts only):{color.STOP}\n[ {color.YELLOW}>{color.STOP} ] ")
    file: str = input(f"[ {color.MAGENTA}?{color.STOP} ] {color.GRAY}Name of your file (with the extension):{color.STOP}\n[ {color.YELLOW}>{color.STOP} ] ")
    file = get_full_filepath(file)

    if os.path.exists(file):
        print(f'[ {color.YELLOW}*{color.STOP} ] {color.YELLOW}File "{file}" was removed (already exists){color.STOP}')
        os.remove(file)

    make_ffmpeg_command(f"ffmpeg -reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 2 -protocol_whitelist file,http,https,tcp,tls,crypto -i \"{m3u8}\" {file}",
                            duration=get_audio_duration(m3u8)
                        )
    clear_last_line()
    print(f"[ {color.GREEN}>{color.STOP} ] {color.GREEN}{file}{color.STOP} ")
    print(f"[ {color.MAGENTA}*{color.STOP} ] {color.GRAY}Thanks for using our video downloader!{color.STOP}")
    return exit(EXIT_SUCCESS)

if __name__ == "__main__":
    main()
