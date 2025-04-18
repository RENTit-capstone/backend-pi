# How to start Raspberry pi server?
run script below:
```sh
source ./run.sh
```
...then it will start to...:
1. Check and create virtual environment(venv).
2. Install every dependencies to start.
3. Start FastAPI Server

# What this project is about?
It's a python server using *FastAPI* for *RENTit*, a rent service for every university.

Run in Raspberry PI, get signals from front, and manage GPIO using *gpiozero*.

And communicate with RabbitMQ server using *asyncio-mqtt*.

