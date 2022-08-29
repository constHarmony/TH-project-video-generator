docker build -t moviepy .devcontainer/
docker run --rm -it -v %cd%:/usr/src/project -t moviepy /bin/bash -c "cd /usr/src/project/ && python main.py"