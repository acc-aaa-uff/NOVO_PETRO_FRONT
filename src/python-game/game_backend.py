from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class GameBackend:

    def __init__(self):
        self.desvios = 0
        self.velocidade = 0

    def registrar_desvio(self):
        self.desvios += 1

    def atualizar_velocidade(self, velocidade: int):
        self.velocidade = velocidade

    @property
    def score(self):
        return self.desvios * self.velocidade

game_data = GameBackend()

@app.post("/registrar_desvio")
def registrar_desvio():
    game_data.registrar_desvio()
    return {"success": True}

@app.post("/atualizar_velocidade/{velocidade}")
def atualizar_velocidade(velocidade: int):
    game_data.atualizar_velocidade(velocidade)
    return {"success": True}

@app.get("/score")
def get_score():
    return {"score": game_data.score}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000, log_level="info", reload=False)







