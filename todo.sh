"$(dirname "$0")/.venv/bin/yt-dlp" --write-auto-subs --sub-langs "en" --skip-download \
  --sub-format vtt \
  --js-runtimes node \
  --sleep-subtitles 5 \
  "$1"