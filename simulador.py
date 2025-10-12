# Cole este código completo em simulator.py

import asyncio
import httpx
import random
import logging
from faker import Faker
from datetime import date, timedelta, datetime

# --- Configuração ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("SIMULATOR")

API_AUTH_URL = "http://localhost:8000"
API_REGULATION_URL = "http://localhost:8001"
API_REVIEW_URL = "http://localhost:8002"
API_COMMUNICATION_URL = "http://localhost:8003" # Adicionado para chamadas diretas se necessário

REGULADOR_USER = "regulador"
REGULADOR_PASSWORD = "hackathon_password"

fake = Faker('pt_BR')

class APIClient:
    """Um cliente para interagir com nossa arquitetura de microsserviços."""
    def __init__(self):
        self._client = httpx.AsyncClient(timeout=30.0)
        self.token = None

    async def authenticate(self):
        """Obtém um token de autenticação e o armazena."""
        logger.info("[AUTH] Tentando autenticar...")
        try:
            response = await self._client.post(
                f"{API_AUTH_URL}/token",
                data={"username": REGULADOR_USER, "password": REGULADOR_PASSWORD}
            )
            response.raise_for_status()
            self.token = response.json()["access_token"]
            logger.info("[AUTH] Autenticação bem-sucedida.")
        except httpx.RequestError as e:
            logger.error(f"[AUTH] Erro ao autenticar: {e}")
            self.token = None

    @property
    def _headers(self):
        if not self.token:
            raise Exception("Cliente não autenticado.")
        return {"Authorization": f"Bearer {self.token}"}

    async def make_request(self, method, url, **kwargs):
        """Helper para fazer requisições autenticadas."""
        try:
            response = await self._client.request(method, url, headers=self._headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Erro na requisição para {url}: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Erro de conexão para {url}: {e}")
        return None

# --- Atores Assíncronos ---

async def solicitante_e_regulador_actor(client: APIClient, state: dict):
    """ATOR 1 & 2: Cria uma solicitação e imediatamente a aprova ou nega."""
    while True:
        logger.info("[SOLICITANTE] Ator iniciado...")
        payload = {
            "paciente_id": f"PACIENTE_{fake.unique.random_int(min=1000, max=9999)}",
            "unidade_solicitante_id_cnes": f"CNES_{random.randint(1, 10)}",
            "procedimento_id": f"PROC_{random.randint(1, 4)}"
        }
        solicitacao = await client.make_request("post", f"{API_REGULATION_URL}/solicitacoes", json=payload)
        
        if solicitacao:
            logger.info(f"[REGULADOR] Analisando solicitação {solicitacao['id']}...")
            if random.random() < 0.10: # 10% de chance de negar
                justificativas = ["Dados incompletos.", "Prioridade baixa.", "Encaminhamento incorreto."]
                await client.make_request(
                    "put", f"{API_REGULATION_URL}/solicitacoes/{solicitacao['id']}/status",
                    json={"status": "NEGADA", "justificativa": random.choice(justificativas)}
                )
            else:
                await client.make_request(
                    "put", f"{API_REGULATION_URL}/solicitacoes/{solicitacao['id']}/status",
                    json={"status": "ACEITA"}
                )
        await asyncio.sleep(120) # A cada 2 minutos

async def gerador_de_ofertas_actor(client: APIClient, state: dict):
    """ATOR 3: Cria novas ofertas de vagas periodicamente."""
    while True:
        logger.info("[GERADOR DE OFERTAS] Ator iniciado...")
        for _ in range(random.randint(2, 5)): # Cria de 2 a 5 novas ofertas
            payload = {
                "unidade_id": random.randint(1, 10),
                "procedimento_id": random.randint(1, 4),
                "data_agendamento": (date.today() + timedelta(days=random.randint(1, 45))).isoformat(),
                "vagas_disponiveis": random.randint(10, 20),
                "horario": f"{random.randint(8, 17):02d}:{random.choice(['00', '30'])}"
            }
            await client.make_request("post", f"{API_REGULATION_URL}/ofertas", json=payload)
        logger.info("[GERADOR DE OFERTAS] Novas ofertas criadas.")
        await asyncio.sleep(300) # A cada 5 minutos

# ... (outros atores seguiriam o mesmo padrão) ...

async def main():
    """Função principal que inicia todos os atores."""
    client = APIClient()
    await client.authenticate()
    
    if not client.token:
        logger.fatal("Não foi possível autenticar. Encerrando o simulador.")
        return

    state = {"marcacoes_pendentes": [], "marcacoes_concluidas": []} 

    logger.info("🚀 Iniciando todos os atores do simulador...")
    # Cria e inicia as tarefas
    task1 = asyncio.create_task(solicitante_e_regulador_actor(client, state))
    task2 = asyncio.create_task(gerador_de_ofertas_actor(client, state))
    
    await asyncio.gather(task1, task2)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Simulador encerrado pelo usuário.")
