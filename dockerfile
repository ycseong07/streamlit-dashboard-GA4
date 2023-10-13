FROM python:3.8

RUN apt-get update

RUN pip install streamlit \
pandas \
numpy \
python-multipart \
streamlit-modal \
python-dotenv \
altair

#install geopandas
RUN apt-get install fonts-nanum*
RUN pip install google-cloud-bigquery

WORKDIR /app

COPY .streamlit/ /root/

EXPOSE 8501

ENTRYPOINT ["streamlit","run", "app.py"]
