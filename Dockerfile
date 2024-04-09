FROM python:3.11

# WORKDIR /

 COPY . .
RUN apt-get install -y xclip xvfb
ENV DISPLAY=:99
RUN nohup bash -c "Xvfb :99 -screen 0 1280x720x16 &"
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "antarli.py","--server.port", "8501", "--server.fileWatcherType", "none"]