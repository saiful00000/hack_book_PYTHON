FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]




# FROM python:3.9

# # COPY ./app /src/app
# COPY ./requirements.txt /src
# # COPY ./.env /src

# WORKDIR /src

# RUN pip3 install -r requirements.txt

# # copy all source code to 
# COPY . .

# EXPOSE 8000
# EXPOSE 5432

# # 
# CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--reload"]
