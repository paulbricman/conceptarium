# Conceptarium
A fluid medium for storing, relating, and surfacing thoughts. [Read more...](https://psionica.org/tools/conceptarium/)

# Instructions
The conceptarium takes up about **1GB RAM** when running. Clone the repository, and install the requirements using:

```
python3 -m pip install -r requirements.txt
```
**Note**: If you plan to deploy your conceptarium on a Raspberry Pi 4, you'll need a version of `pytorch` compiled for ARM devices, such as [pytorch-rpi](https://github.com/ljk53/pytorch-rpi/blob/master/torch-1.9.0a0%2Bgitd69c22d-cp39-cp39-linux_aarch64.whl). 

Start the web server using:
```
python3 -m uvicorn main:app --reload
```

This will make your conceptarium available at `127.0.0.1:8000`. Go to `127.0.0.1:8000/docs` to get an overview of the available endpoints.

**Note**: If you want to access your conceptarium remotely, have a look at [ngrok](https://ngrok.com/).

Simple ways of getting the most out of your conceptarium are by configuring adding it as a search engine via [browser extensions](https://addons.mozilla.org/en-US/firefox/addon/swift-selection-search/), or by creating some [AutoKey](https://github.com/autokey/autokey) / [AutoHotKey](https://www.autohotkey.com/) scripts to interact with it via hotkeys.
