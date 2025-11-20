from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response, HTMLResponse
import edge_tts

app = FastAPI()

@app.get("/")
async def root():
    return JSONResponse(
        content={
            "status_code": 200,
            "developer": "El Impaciente"
        },
        status_code=200
    )

@app.get("/documentacion", response_class=HTMLResponse)
@app.get("/documentacion.html", response_class=HTMLResponse)
async def documentacion():
    html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Microsoft TTS API - El Impaciente</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 50px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        h1 { color: #667eea; font-size: 36px; margin-bottom: 10px; }
        .subtitle { color: #666; font-size: 18px; margin-bottom: 40px; }
        .section { margin-bottom: 40px; }
        h2 {
            color: #333;
            font-size: 24px;
            margin-bottom: 15px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        .info-block {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }
        .info-block strong { color: #667eea; display: inline-block; min-width: 120px; }
        .code-block {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            margin: 10px 0;
        }
        .example-url {
            background: #e7f3ff;
            padding: 15px;
            border-radius: 8px;
            word-break: break-all;
            color: #0066cc;
            font-family: monospace;
            margin: 10px 0;
        }
        .voice-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }
        .voice-item {
            background: #f8f9fa;
            padding: 10px 15px;
            border-radius: 6px;
            font-size: 14px;
            border-left: 3px solid #667eea;
        }
        .badge {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 12px;
            margin-left: 5px;
        }
        .optional-badge {
            display: inline-block;
            background: #6c757d;
            color: white;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 12px;
            margin-left: 5px;
        }
        .response-example {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #eee;
            color: #666;
        }
        .btn-test {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            margin-top: 20px;
            transition: transform 0.2s;
        }
        .btn-test:hover { transform: translateY(-2px); }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎙️ Microsoft TTS API</h1>
        <p class="subtitle">Convierte texto a audio con 400+ voces neuronales de Microsoft</p>

        <div class="section">
            <h2>📋 Información General</h2>
            <div class="info-block">
                <strong>Base URL:</strong> <code>https://convertidor-impaciente-de-microsoft.vercel.app/api/tts</code>
            </div>
            <div class="info-block"><strong>Método:</strong> GET</div>
            <div class="info-block"><strong>Formato:</strong> Audio MP3 (24kHz)</div>
            <div class="info-block"><strong>Precio:</strong> ✅ GRATIS</div>
            <div class="info-block"><strong>Desarrollador:</strong> El Impaciente</div>
        </div>

        <div class="section">
            <h2>🔮 Parámetros</h2>
            <div class="info-block">
                <strong>text</strong> <span class="badge">requerido</span><br>
                Texto a convertir en audio
            </div>
            <div class="info-block">
                <strong>voice</strong> <span class="optional-badge">opcional</span><br>
                Nombre de la voz neural (por defecto: en-US-GuyNeural)<br>
                Ejemplo: es-MX-DaliaNeural
            </div>
            <div class="info-block">
                <strong>rate</strong> <span class="optional-badge">opcional</span><br>
                Velocidad del audio (por defecto: +0%)<br>
                Ejemplos: +50% (más rápido), -25% (más lento)
            </div>
            <div class="info-block">
                <strong>pitch</strong> <span class="optional-badge">opcional</span><br>
                Tono de voz (por defecto: +0Hz)<br>
                Ejemplos: +10Hz (más agudo), -5Hz (más grave)
            </div>
            <div class="info-block">
                <strong>volume</strong> <span class="optional-badge">opcional</span><br>
                Volumen del audio (por defecto: +0%)<br>
                Ejemplos: +20% (más alto), -10% (más bajo)
            </div>
            <div class="info-block">
                <strong>file_name</strong> <span class="optional-badge">opcional</span><br>
                Nombre del archivo de salida (por defecto: generated_mp3.mp3)
            </div>
        </div>

        <div class="section">
            <h2>💡 Ejemplos de Uso</h2>
            
            <h3 style="color: #667eea; margin-top: 20px;">Básico</h3>
            <div class="example-url">
                /api/tts?text=Hola mundo&voice=es-MX-DaliaNeural
            </div>
            
            <h3 style="color: #667eea; margin-top: 20px;">Con velocidad personalizada</h3>
            <div class="example-url">
                /api/tts?text=Hola mundo&voice=es-MX-DaliaNeural&rate=+50%
            </div>
            
            <h3 style="color: #667eea; margin-top: 20px;">Completo con todos los parámetros</h3>
            <div class="example-url">
                /api/tts?text=Hola mundo&voice=es-MX-DaliaNeural&rate=+25%&pitch=-5Hz&volume=+10%&file_name=mi_audio.mp3
            </div>

            <a href="/api/tts?text=Hola, esta es una prueba con todos los parámetros&voice=es-MX-DaliaNeural&rate=+20%&volume=+10%" 
               class="btn-test" target="_blank">🎵 Probar Ahora</a>
        </div>

        <div class="section">
            <h2>📤 Respuestas</h2>
            <div class="response-example">
                <strong>✅ Éxito (200):</strong><br>
                Devuelve el archivo de audio MP3 directamente con headers completos
            </div>
            <div class="response-example">
                <strong>❌ Error (400) - Texto faltante:</strong>
                <div class="code-block">{
  "status_code": 400,
  "message": "Text is required"
}</div>
            </div>
            <div class="response-example">
                <strong>❌ Error (500) - Sin audio generado:</strong>
                <div class="code-block">{
  "status_code": 500,
  "message": "No audio chunks received from TTS service"
}</div>
            </div>
            <div class="response-example">
                <strong>❌ Error (500) - Audio vacío:</strong>
                <div class="code-block">{
  "status_code": 500,
  "message": "Empty audio data received"
}</div>
            </div>
            <div class="response-example">
                <strong>❌ Error (500) - Error general:</strong>
                <div class="code-block">{
  "status_code": 500,
  "message": "Error: [detalle del error]"
}</div>
            </div>
        </div>

        <div class="section">
            <h2>🎤 Voces Populares</h2>
            
            <h3 style="color: #667eea; margin-top: 20px;">🇪🇸 Español</h3>
            <div class="voice-list">
                <div class="voice-item">es-MX-DaliaNeural 👩<br><small>México</small></div>
                <div class="voice-item">es-MX-JorgeNeural 👨<br><small>México</small></div>
                <div class="voice-item">es-ES-ElviraNeural 👩<br><small>España</small></div>
                <div class="voice-item">es-ES-AlvaroNeural 👨<br><small>España</small></div>
                <div class="voice-item">es-AR-ElenaNeural 👩<br><small>Argentina</small></div>
                <div class="voice-item">es-CO-SalomeNeural 👩<br><small>Colombia</small></div>
            </div>

            <h3 style="color: #667eea; margin-top: 20px;">🇺🇸 English</h3>
            <div class="voice-list">
                <div class="voice-item">en-US-JennyNeural 👩<br><small>USA</small></div>
                <div class="voice-item">en-US-GuyNeural 👨<br><small>USA</small></div>
                <div class="voice-item">en-GB-LibbyNeural 👩<br><small>UK</small></div>
                <div class="voice-item">en-GB-RyanNeural 👨<br><small>UK</small></div>
            </div>

            <h3 style="color: #667eea; margin-top: 20px;">🌍 Otros Idiomas</h3>
            <div class="voice-list">
                <div class="voice-item">fr-FR-DeniseNeural 👩<br><small>Français</small></div>
                <div class="voice-item">de-DE-KatjaNeural 👩<br><small>Deutsch</small></div>
                <div class="voice-item">it-IT-ElsaNeural 👩<br><small>Italiano</small></div>
                <div class="voice-item">pt-BR-FranciscaNeural 👩<br><small>Português</small></div>
                <div class="voice-item">zh-CN-XiaoxiaoNeural 👩<br><small>中文</small></div>
                <div class="voice-item">ja-JP-NanamiNeural 👩<br><small>日本語</small></div>
                <div class="voice-item">ko-KR-SunHiNeural 👩<br><small>한국어</small></div>
                <div class="voice-item">ru-RU-SvetlanaNeural 👩<br><small>Русский</small></div>
            </div>

            <div class="info-block" style="margin-top: 20px;">
                <strong>Ver todas:</strong> 
                <a href="/api/voices" style="color: #667eea;">400+ voces disponibles</a>
            </div>
        </div>

        <div class="section">
            <h2>💻 Ejemplos de Código</h2>
            
            <h3 style="color: #667eea; margin-top: 20px;">JavaScript</h3>
            <div class="code-block">const url = "https://convertidor-impaciente-de-microsoft.vercel.app/api/tts";
const params = new URLSearchParams({
  text: "Hola mundo",
  voice: "es-MX-DaliaNeural",
  rate: "+25%",
  volume: "+10%"
});

fetch(`${url}?${params}`)
  .then(res => res.blob())
  .then(blob => {
    const audio = new Audio(URL.createObjectURL(blob));
    audio.play();
  });</div>

            <h3 style="color: #667eea; margin-top: 20px;">Python</h3>
            <div class="code-block">import requests

url = "https://convertidor-impaciente-de-microsoft.vercel.app/api/tts"
params = {
    "text": "Hola mundo",
    "voice": "es-MX-DaliaNeural",
    "rate": "+25%",
    "pitch": "-5Hz",
    "volume": "+10%"
}

response = requests.get(url, params=params)
with open("audio.mp3", "wb") as f:
    f.write(response.content)</div>

            <h3 style="color: #667eea; margin-top: 20px;">cURL</h3>
            <div class="code-block">curl "https://convertidor-impaciente-de-microsoft.vercel.app/api/tts?text=Hola&voice=es-MX-DaliaNeural&rate=+25%" -o audio.mp3</div>

            <h3 style="color: #667eea; margin-top: 20px;">PHP</h3>
            <div class="code-block">$url = "https://convertidor-impaciente-de-microsoft.vercel.app/api/tts";
$params = http_build_query([
    "text" => "Hola mundo",
    "voice" => "es-MX-DaliaNeural",
    "rate" => "+25%"
]);

file_put_contents("audio.mp3", file_get_contents($url . "?" . $params));</div>
        </div>

        <div class="section">
            <h2>✨ Características</h2>
            <div class="voice-list">
                <div class="voice-item">✅ Totalmente gratis</div>
                <div class="voice-item">✅ Sin autenticación</div>
                <div class="voice-item">✅ 400+ voces neuronales</div>
                <div class="voice-item">✅ 30+ idiomas</div>
                <div class="voice-item">✅ Alta calidad (24kHz)</div>
                <div class="voice-item">✅ Control de velocidad</div>
                <div class="voice-item">✅ Control de tono</div>
                <div class="voice-item">✅ Control de volumen</div>
                <div class="voice-item">✅ Respuesta instantánea</div>
                <div class="voice-item">✅ Headers HTTP completos</div>
                <div class="voice-item">✅ Errores detallados</div>
                <div class="voice-item">✅ Nombres personalizables</div>
            </div>
        </div>

        <div class="footer">
            <p><strong>👨‍💻 Desarrollador:</strong> El Impaciente</p>
            <p style="margin-top: 10px; font-size: 14px;">
                ⭐ Si te gusta esta API, compártela con otros desarrolladores
            </p>
        </div>
    </div>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

@app.get("/tts")
@app.get("/api/tts")
async def text_to_speech(
    text: str = None,
    voice: str = "en-US-GuyNeural",
    rate: str = "+0%",
    pitch: str = "+0Hz",
    volume: str = "+0%",
    file_name: str = "generated_mp3.mp3"
):
    # Validación de texto requerido
    if not text or text.strip() == "":
        return JSONResponse(
            content={
                "status_code": 400,
                "message": "Text is required"
            },
            status_code=400
        )
    
    try:
        # Asegurar valores predeterminados válidos
        rate = rate if rate else "+0%"
        volume = volume if volume else "+0%"
        pitch = pitch if pitch else "+0Hz"
        voice = voice if voice else "en-US-GuyNeural"
        file_name = file_name if file_name and file_name.strip() else "generated_mp3.mp3"
        
        # Asegurar extensión .mp3
        if not file_name.lower().endswith(".mp3"):
            file_name += ".mp3"
        
        # Crear comunicación con edge-tts
        communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume, pitch=pitch)
        
        # Recolectar chunks de audio
        audio_chunks = []
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_chunks.append(chunk["data"])
        
        # Validar que se recibieron chunks
        if not audio_chunks:
            return JSONResponse(
                content={
                    "status_code": 500,
                    "message": "No audio chunks received from TTS service"
                },
                status_code=500
            )
        
        # Concatenar audio
        audio_data = b"".join(audio_chunks)
        
        # Validar que el audio no esté vacío
        if len(audio_data) == 0:
            return JSONResponse(
                content={
                    "status_code": 500,
                    "message": "Empty audio data received"
                },
                status_code=500
            )
        
        # Retornar respuesta con headers completos
        return Response(
            content=audio_data,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"inline; filename={file_name}",
                "Content-Length": str(len(audio_data)),
                "Accept-Ranges": "bytes"
            }
        )
        
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "message": f"Error: {str(e)}"
            },
            status_code=500
        )

@app.get("/voices")
@app.get("/api/voices")
async def list_voices():
    try:
        voices = await edge_tts.list_voices()
        
        # Ordenar voces por locale y nombre
        sorted_voices = sorted(voices, key=lambda x: (x.get("Locale", ""), x.get("ShortName", "")))
        
        # Formatear con toda la información
        formatted_voices = []
        for v in sorted_voices:
            formatted_voices.append({
                "ShortName": v.get("ShortName", "N/A"),
                "FriendlyName": v.get("FriendlyName", v.get("ShortName", "N/A")),
                "Gender": v.get("Gender", "Unknown"),
                "Locale": v.get("Locale", "N/A")
            })
        
        return JSONResponse(
            content={
                "status_code": 200,
                "developer": "El Impaciente",
                "total": len(formatted_voices),
                "voices": formatted_voices
            }
        )
        
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 500,
                "message": str(e)
            },
            status_code=500
        )
