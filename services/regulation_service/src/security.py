# Cole este código em TODOS os seus arquivos security.py
# (regulation-service, communication-service, review-service)

import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel

# --- Modelo Pydantic (continua o mesmo) ---
class TokenData(BaseModel):
    username: str | None = None

# --- Esquema de Segurança (continua o mesmo) ---
security_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    """
    Dependência de segurança que lê as variáveis de ambiente no momento da execução.
    """
    # --- LEITURA TARDIA DAS VARIÁVEIS DE AMBIENTE ---
    # Movemos a leitura para DENTRO da função.
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("JWT_ALGORITHM")

    # Adicionamos uma verificação para garantir que as chaves foram carregadas
    if not secret_key or not algorithm:
        raise HTTPException(
            status_code=500,
            detail="Configuração interna do servidor incompleta (chaves de segurança não encontradas)."
        )

    token = credentials.credentials
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm]) # Usamos as variáveis locais
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    return {"payload": token_data, "token_string": token}