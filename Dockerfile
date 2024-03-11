# Select a minimal base image with Python 3.11 (adjust if needed)
FROM python:3.11-slim-buster
MAINTAINER Narasimhan M.G. github.com/Naras 
COPY ./Amarakosha.db /usr/local/Amarakosha/Amarakosha.db
COPY ./Bandarkar.txt /usr/local/Amarakosha/Bandarkar.txt
COPY ./source/Controller /usr/local/Amarakosha/source/Controller
COPY ./source/Model /usr/local/Amarakosha/source/Model
COPY  ./requirements_rest_docker.txt /usr/local/Amarakosha/requirements.txt

# Set working directory and copy app contents, excluding unnecessary files
WORKDIR /usr/local/Amarakosha/
# Install Python dependencies from requirements.txt
RUN pip3 install -r requirements.txt

RUN rm -rf .git .idea venv requirements.txt  # Remove unwanted files
# Expose the REST API port (adjust if different)
EXPOSE 5002
# Set the entrypoint and command for running the app
# ENTRYPOINT ["python", "app.py"]  # Replace "app.py" with your main script
CMD python3 source/Controller/restService.py

