import openai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers=["*"],
)

# Configura la clave de la API de OpenAI
openai.api_key = "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"

@app.get("/")
def root():
    return {
        "Service": "Integracion Back OpenAI"
    }

@app.post("/chat")
def chat(pregunta: dict):
    try:
        # Contexto inicial para las conversaciones

        contexto = (
            "Hola,por favor haz una revisión de todas las tablas en la base de datos Chinook."
            "Entiende que todas las preguntas que te haga son para obtener consultas de SQL Server."
            "Por favor, responde solo con la consulta de SQL Server a las preguntas que te haga sobre la base de datos Chinook"
            "y nada más. Comienza a hacerlo con esta pregunta también."
            "Aquí algunas de las tablas clave en la base de datos Chinook:"
            "1. Album\n"
            "2. Artist\n"
            "3. Customer\n"
            "4. Employee\n"
            "5. Genre\n"
            "6. Invoice\n"
            "7. InvoiceLine\n"
            "8. MediaType\n"
            "9. Playlist\n"
            "10. PlaylistTrack\n"
            "11. Track"
        )

        # Imprime la pregunta recibida
        print(pregunta)

        # Envía la pregunta al modelo de OpenAI
        response = openai.Completion.create(
            engine="text-davinci-002",  # Modelo actualizado
            prompt=contexto + pregunta["pregunta"],
            temperature=0.7,
            max_tokens=256
        )

        # Obtiene la respuesta del modelo
        print(f"Respuesta completa:'{response['choices'][0]['text']}'")

        # Obtén la respuesta del modelo y elimina espacios en blanco al principio y al final
        respuesta_chat = response['choices'][0]['text'].strip()

        # Verifica si se obtuvo una respuesta
        if not respuesta_chat:
            raise HTTPException(status_code=500, detail="No se obtuvo una respuesta válida del modelo.")

        return {
            "Respuesta": respuesta_chat
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

