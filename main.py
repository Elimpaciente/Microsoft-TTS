from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
import edge_tts
from io import BytesIO

app = FastAPI()

@app.get("/")
async def root():
    return JSONResponse(
        content={"success": True},
        status_code=200
    )

@app.get("/tts")
async def text_to_speech(voice: str = "", text: str = ""):
    if not voice or not text or voice.strip() == "" or text.strip() == "":
        return JSONResponse(
            content={"success": False, "message": "Voice and text parameters are required"},
            status_code=400
        )
    
    try:
        communicate = edge_tts.Communicate(text, voice)
        audio_buffer = BytesIO()
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
        
        if audio_buffer.tell() == 0:
            return JSONResponse(
                content={"success": False, "message": "Could not generate audio"},
                status_code=400
            )
        
        audio_buffer.seek(0)
        
        return StreamingResponse(
            audio_buffer,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=audio.mp3"}
        )
        
    except Exception:
        return JSONResponse(
            content={"success": False, "message": "Error processing request"},
            status_code=400
        )

@app.get("/voices")
async def list_voices():
    try:
        voices = await edge_tts.list_voices()
        formatted_voices = [
            {
                "name": voice["ShortName"],
                "gender": voice["Gender"],
                "locale": voice["Locale"]
            }
            for voice in voices
        ]
        
        return JSONResponse(
            content={"success": True, "total": len(formatted_voices), "voices": formatted_voices},
            status_code=200
        )
        
    except Exception:
        return JSONResponse(
            content={"success": False, "message": "Error retrieving voices"},
            status_code=400
        )
