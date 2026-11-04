# assembles the short from head + shared helpers + scenes + tail
cd "$(dirname "$0")"
cat _head.py _common.py _scenes.py _tail.py > jshort.py
