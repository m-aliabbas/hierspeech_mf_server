from fastapi import FastAPI, HTTPException,WebSocket
from fastapi.responses import StreamingResponse
import uvicorn
from inference import *  # Assuming this includes required classes and methods
import io
import soundfile as sf
from pydantic import BaseModel 
import wave
# Reusing your existing Config and TTS_SERVER classes
class Config:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)
config_dict = {
    'output_sr': 48000,
    'denoiser_ckpt': 'denoiser/g_best',
    'ckpt': 'logs/hierspeechpp_eng_kor/hierspeechpp_v1.1_ckpt.pth',
    'ckpt_sr48': './speechsr48k/G_100000.pth',
    'scale_norm': 'max',
    'ckpt_text2w2v': 'logs/ttv_libritts_v1/ttv_lt960_ckpt.pth',
    'noise_scale_vc': 0.333,
    'noise_scale_ttv': 0.333,
    'denoise_ratio': 0.0,
    'duratuion_length': 0.7,
    'duratuion_temperature':0.8,
    'ckpt_sr': './speechsr24k/G_340000.pth',
    'input_prompt':'example/3_rick_gt.wav',
    'output_dir':'temp',
}
config = Config(config_dict)

class TTS_SERVER:
    def __init__(self, config) -> None:
        self.config = config
        self.model = main(self.config)

    def generate_speech(self, text=''):
        text = [text]
        wav = tts(text, self.config, self.model)
        return wav

app = FastAPI()
tts_server = TTS_SERVER(config=config)
class SynthesizeRequest(BaseModel):
    text: str  # Define a request model that expects 'text' as a string

@app.post("/synthesize_post/")
async def synthesize_speech(request: SynthesizeRequest):  # Use Pydantic model to parse body
    try:
        audio_array = tts_server.generate_speech(request.text)
        buffer = io.BytesIO()
        # Write array to a buffer as a WAV file
        sf.write(file=buffer, data=audio_array, samplerate=config.output_sr, format='WAV')
        buffer.seek(0)  # Rewind the buffer to the beginning
        return StreamingResponse(buffer, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.websocket("/synthesize")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive text, voice, and lngsteps from client
            data = await websocket.receive_json()
            text = data.get('text')
            print(text)
            # Simulate synthesizing speech (actual API call would be here)
            # Example response format based on the provided structure
            audio_data = tts_server.generate_speech(text=text)
            
            
            # Convert to WAV format
            buffer = io.BytesIO()
            sample_rate = config.output_sr
            sf.write(file=buffer, data=audio_data, samplerate=config.output_sr, format='WAV')
            # Send the WAV bytes to the client
            buffer.seek(0) 
            await websocket.send_bytes(buffer.getvalue())

    except Exception as e:
        # await websocket.send_text(f"Error: {str(e)}")
        print(e)
    finally:
        await websocket.close()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)
