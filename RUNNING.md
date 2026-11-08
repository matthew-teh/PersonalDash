## How to run locally (Linux only)
- Supported python versions : 3.11, 3.12, 3.13, 3.14 . Recommended 3.14
- Make sure you have **python** and **git** installed  
- Run command below  

**Personal Dashboard V2 Docker(Install docker first.)** [Click when you done command below](http://localhost:65003)
```bash
docker network create reflex-net
docker run -d --network reflex-net -p 65500:123/udp --name ntp-server cturra/ntp:latest
docker run -d --network reflex-net -p 65503:65503 --name Reflex-PDash-V2 nuggetteh/personal-dashboard:reflex-app-v2
```
  
**Personal Dashboard V1:**
  ```bash
  git clone https://github.com/matthew-teh/PersonalDash.git
  cd PersonalDash
  git checkout 05a6fd8e5769cb36a0944308589637a7759f0b08
  curl -LsSf https://astral.sh/uv/install.sh | sh   # Install UV
  uv add reflex requests openmeteo-requests
  uv run reflex run
  ```
Personal Dashboard V1 Only:  
1. `git clone https://github.com/Pymmdrza/Cryptocurrency_Logos.git`
2. Copy the folder PNG to PersonalDash/assets
3. Rename the folder to `cryptoimages`
4. `git clone https://github.com/Makin-Things/weather-icons`
5. Copy the folder `animated` to PersonalDash/assets
6. Rename the folder to `weatherimages`
7. Delete original folder of `weather-icons` and `Cryptocurrency_Logos`

**Personal Dashboard Beta:**
  ```bash 
  git clone https://github.com/matthew-teh/PersonalDash.git
  cd PersonalDash
  git checkout 8b1d5b7c279e807a0b755b27cc1fe3dd21ea8e52
  curl -LsSf https://astral.sh/uv/install.sh | sh  # Install UV
  uv add reflex
  uv run reflex run
  ```