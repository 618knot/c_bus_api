FROM python:3.9
USER root
WORKDIR /c_bus_api
COPY ./requirements.txt /c_bus_api/
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ /c_bus_api
RUN pip install --no-cache-dir uvicorn
EXPOSE 3000

ENTRYPOINT ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "3000"]

# uvicorn main:app --reload --host 0.0.0.0 --port 3000