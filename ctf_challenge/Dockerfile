FROM debian:11.4

WORKDIR /app

RUN apt update

RUN apt install -y curl gnupg

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt update

RUN ACCEPT_EULA=Y apt install -y msodbcsql18

RUN ACCEPT_EULA=Y apt install -y mssql-tools18

RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc

RUN apt install -y unixodbc-dev python3 python3-pip

RUN pip install pyodbc

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "5", "-b", "0.0.0.0:8000", "routes:app"]
