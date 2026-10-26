FROM ubuntu:18.04

USER root
RUN mkdir /app && chown nobody /app 
RUN apt update && apt install -y python3 python3-pip
RUN pip3 install -U discord.py==1.7.3
RUN pip3 install -U python-dotenv==0.20.0

COPY --chown=nobody:root app/bot.py /app/bot.py

USER nobody
WORKDIR /app
CMD python3 /app/bot.py 


