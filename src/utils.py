import shutil
import subprocess
import os
import sys
import re

def ffmpeg_isInstalled() -> bool:
    output: str = os.popen(
        cmd="ffmpeg -version"
    ).read()
    return "gcc" in output

def get_audio_duration(file) -> float:
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, encoding=os.device_encoding(0))
    return float(result.stdout)

def durationToSeconds(hms) -> float:
    a = hms.split(":")
    seconds = (int(a[0])) * 60 * 60 + (int(a[1])) * 60 + (float(a[2]));
    return seconds

def display_progress_bar(
    current: int, filesize: int, ch: str = "█", scale: float = 0.5
) -> None:
    columns = shutil.get_terminal_size().columns
    max_width = int(columns * scale)
    filled = int(round(max_width * current / float(filesize)))
    remaining = max_width - filled
    progress_bar = ch * filled + " " * remaining
    percent = round(100.0 * current / float(filesize), 1)
    text = f" ↳ |{progress_bar}| {percent}%\r"
    sys.stdout.write(text)
    sys.stdout.flush()

def make_ffmpeg_command(command, duration, on_progress=None):
    process = subprocess.Popen(command, encoding=os.device_encoding(0), universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    history = []
    with process.stdout as pipe:
        for line in pipe:
            line = line.strip()
            history.append(line)
            if "time=" in line:
                try:
                    result = re.search(r"\.*time=(.*?) ", line)
                    seconds = durationToSeconds(result.group(1))
                    if on_progress:
                        on_progress(seconds, duration)
                    else:
                        display_progress_bar(seconds, duration)
                except: None

    return process.wait(), history
