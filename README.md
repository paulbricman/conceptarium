---
title: conceptarium
emoji: 💡
colorFrom: green
colorTo: gray
sdk: streamlit
app_file: frontend/main.py
pinned: false
---

| screenshot 1                                                                                                                                  | screenshot 2                                                                                                                                  |
| --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| ![Screenshot from 2022-02-01 12-19-30](https://user-images.githubusercontent.com/20104026/151968818-df3521d8-ea04-48a1-a21b-8cbb54f84bea.png) | ![Screenshot from 2022-02-01 12-24-48](https://user-images.githubusercontent.com/20104026/151970146-2895a808-26af-4761-b087-57314b59a3b3.png) |

# 💡 Conceptarium

The conceptarium is an **experimental** personal knowledge base designed to weave AI capabilities into knowledge work. Its main features include:

- powerful multi-modal search across ideas
- sharing [microverses of knowledge](https://paulbricman.com/reflections/sharing-searches) with peers
- ranking items by Anki-like activation, so as to promote serendipity

## Installation

#### Docker

After installing `docker` and `docker-compose`, run:

```
# install with:
curl -fsS https://raw.githubusercontent.com/paulbricman/conceptarium/main/docker-compose.yml -o docker-compose.yml
mkdir knowledge
docker-compose up -d

# stop with:
docker-compose stop

# update with:
docker-compose stop
docker-compose rm -f
docker-compose pull
docker-compose up -d
```

Note that you'll have to wait a bit initially for the models to be downloaded in the docker container. Use `docker logs <backend container ID>` or watch the process's memory for feedback on that. Or just try using it until it via the API or UI until it works (see usage).

#### Source

After pulling this repo run:

```
python3 -m pip install -r frontend/requirements.txt
python3 -m pip install -r backend/requirements.txt
streamlit run frontend/main.py

# in a separate session:
cd backend
python3 -m uvicorn main:app --reload

# update by pulling from repo again
```

Missing dependencies? Please have a look at `frontend/Dockerfile` and `backend/Dockerfile`. ARM architecture (e.g. Raspberry Pi)? Remove the `torch` entries from `requirements.txt`, and install a [custom-built version](https://github.com/ljk53/pytorch-rpi).

## Usage

The web app should then be available at `localhost:8501`, while the API at `localhost:8000` (with docs at `localhost:8000/docs`). The backend component takes a few minutes to get the ML models at first.

To access your local instance, enter the conceptarium URL (i.e. `localhost:8000` if you ran from source, `backend.docker:8000` if you used docker), and your desired token. Remember your token, as you'll have to use it to authenticate in future sessions.
