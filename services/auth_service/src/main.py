# Cole este código completo no seu arquivo services/auth_service/src/main.py

import os
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

# --- Configuração ---
# Carregamos os segredos e configurações a partir das variáveis de ambiente definidas no .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # O token expirará em 60 minutos (1 hora)

# --- Modelos (Schemas) Pydantic ---
# Este modelo define a estrutura da resposta do nosso endpoint de token
class Token(BaseModel):
    access_token: str
    token_type: str

# --- Instância do FastAPI ---
app = FastAPI(
    title="Auth Service",
    description="Serviço para autenticação e geração de tokens JWT.",
    version="1.0.0"
)

# --- Funções de Lógica de Negócio ---

def verify_credentials(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Valida as credenciais do usuário.
    Para o MVP, usamos as credenciais fixas do arquivo .env.
    Em um sistema real, aqui entraria a lógica de buscar o usuário no banco
    de dados e comparar o hash da senha.
    """
    mvp_user = os.getenv("MVP_USER")
    mvp_password = os.getenv("MVP_PASSWORD")

    # Comparamos o usuário e senha recebidos com os do .env
    if not (form_data.username == mvp_user and form_data.password == mvp_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return form_data.username

def create_access_token(data: dict):
    """
    Cria o token JWT.
    """
    to_encode = data.copy()
    # Adiciona o timestamp de expiração ao payload do token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Codifica o token com nosso payload, chave secreta e algoritmo
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Endpoint da API ---

@app.post("/token", response_model=Token)
async def login_for_access_token(
    # Annotated e Depends injetam os dados do formulário de login (username/password)
    # e validam as credenciais usando nossa função
    username: Annotated[str, Depends(verify_credentials)]
):
    """
    Endpoint de login. Recebe usuário e senha, valida, e se ok,
    retorna um access_token JWT.
    """
    # Se a função verify_credentials passou, significa que o usuário é válido.
    # Agora criamos o token para ele.
    access_token = create_access_token(
        data={"sub": username} # 'sub' é o nome padrão do "subject" (sujeito) do token
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return {"message": "Auth Service is running. Acesse /docs para a documentação interativa."}