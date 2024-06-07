# Modified Style TTS
This is modified style tts design specifically for efficency and scalability. We have incorporated Streaming and HTTP server for integration with LLM. 
Also, we add a functionality to run tts in memory only one.

# How to install.

```
sudo apt install espeak-ng
conda create -n tts_env python=3.10
conda activate tts_env
pip install -r requirements.txt
```
# Download pretrained weights
1. You need to download pretrained weights from following url:

2. After downloading weights; extract them.

3. Paste the logs/ folder (it will be containing weights to your DIR).



# How to Run
For running server
```
python tts_server.py
```
For noramal use you can use `inference.py`

For gradio app
```
python app.py
```


# Credit 
Mohammad Ali Abbas
Sr. ML Engr Idrak ai