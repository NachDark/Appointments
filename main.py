from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# 🔹 Dummy DB
FAKE_DB = {
    "12345678": {
        "nombre": "Ignacio Pérez"
    },
    "87654321": {
        "nombre": "María González"
    }
}


@app.post("/webhook")
async def dialogflow_webhook(request: Request):
    body = await request.json()

    # 🔍 Datos desde Dialogflow ES
    intent = body["queryResult"]["intent"]["displayName"]
    parameters = body["queryResult"].get("parameters", {})

    dni = parameters.get("identityDocument")


    if intent == "Identificarme Intent":
        if not dni:
            response_text = "No recibí tu DNI. ¿Podés repetírmelo?"
        else:
            dni_str = str(int(dni))  
            user = FAKE_DB.get(dni_str)

            if user:
                response_text = f"Gracias. Te identifico como {user['nombre']}."
            else:
                response_text = "No encontré a nadie con ese DNI."
    else:
        response_text = "Intent no reconocido.{intent}"

    return JSONResponse(
        content={
            "fulfillmentText": response_text
        }
    )