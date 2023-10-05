FROM python:3.8

RUN apt-get update

RUN pip install streamlit \
pandas \
numpy \
pillow \
python-multipart \
streamlit-modal \
python-dotenv \
altair \ 
plotly

#install geopandas
RUN echo Y |  apt-get install libgdal-dev
RUN echo Y | apt install libspatialindex-dev
RUN pip install --upgrade pip
RUN pip install pandas fiona shapely pyproj rtree
RUN pip install geopandas folium
RUN python -m pip install -U pip
RUN python -m pip install -U matplotlib
RUN pip install seaborn
RUN pip install pydeck
RUN apt-get install fonts-nanum*
RUN pip install google-cloud-bigquery

WORKDIR /app

COPY .streamlit/ /root/

EXPOSE 8501

ENTRYPOINT ["streamlit","run", "app.py"]
