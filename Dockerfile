FROM python:3.11

# WORKDIR /

 COPY . .
# RUN sudo apt install xclip
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "antarli.py","--server.port", "8501", "--server.fileWatcherType", "none"]