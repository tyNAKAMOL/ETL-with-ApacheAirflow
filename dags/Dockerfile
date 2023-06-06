FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY transform.py .


# COPY extract.py .
# COPY load.py .
# COPY Hello.py .
# COPY Hello2.py .
# ADD hello.py .

# CMD [ "python", "extract.py" ]