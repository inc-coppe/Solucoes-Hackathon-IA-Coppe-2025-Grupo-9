from sqlalchemy.orm import Session
from . import models, crud
from .logging_config import logger
from math import radians, sin, cos, sqrt, atan2
from datetime import date
from . import communication_client

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calcula a distância em km entre dois pontos geográficos."""
    R = 6371  # Raio da Terra em km

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat / 2)**2 + cos(lat1) * cos(lat2) * sin(dLon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def find_best_slot(db: Session, solicitacao: models.Solicitacao):
    """
    O coração do agente inteligente. Encontra a melhor oferta para uma solicitação.
    Critérios:
    1. Procedimento correto.
    2. Data mais próxima a partir de hoje.
    3. Menor distância como critério de desempate.
    """
    logger.info(f"Agente iniciado para a solicitação ID: {solicitacao.id}")
    
    # Simular a localização do paciente (em um sistema real, viria de um cadastro)
    # Para o MVP, vamos usar a localização da unidade solicitante como proxy.
    unidade_solicitante = db.query(models.Unidade).filter(
        models.Unidade.cnes_id == solicitacao.unidade_solicitante_id_cnes
    ).first()
    
    if not unidade_solicitante:
        logger.warning(f"Não foi possível encontrar a unidade solicitante com CNES {solicitacao.unidade_solicitante_id_cnes}. Abortando.")
        return None

    paciente_lat = unidade_solicitante.latitude
    paciente_lon = unidade_solicitante.longitude

    # Encontra o procedimento no banco
    procedimento = db.query(models.Procedimento).filter(
        models.Procedimento.procedimento_id == solicitacao.procedimento_id
    ).first()

    if not procedimento:
        logger.warning(f"Procedimento com ID {solicitacao.procedimento_id} não encontrado. Abortando.")
        return None

    # Busca todas as ofertas válidas (procedimento correto, data futura, vagas > 0)
    hoje = date.today()
    ofertas_validas = db.query(models.OfertaProgramada).join(models.Unidade).filter(
        models.OfertaProgramada.procedimento_id == procedimento.id,
        models.OfertaProgramada.data_agendamento >= hoje,
        models.OfertaProgramada.vagas_disponiveis > 0
    ).all()

    if not ofertas_validas:
        logger.info(f"Nenhuma oferta encontrada para o procedimento {procedimento.nome}.")
        return None

    # Calcula a distância para cada oferta e armazena os candidatos
    candidatos = []
    for oferta in ofertas_validas:
        unidade_oferta = db.query(models.Unidade).get(oferta.unidade_id)
        distancia = haversine_distance(paciente_lat, paciente_lon, unidade_oferta.latitude, unidade_oferta.longitude)
        candidatos.append({
            "oferta": oferta,
            "data": oferta.data_agendamento,
            "distancia": distancia
        })
    
    # Ordena os candidatos: primeiro pela data mais próxima, depois pela menor distância
    candidatos_ordenados = sorted(candidatos, key=lambda c: (c['data'], c['distancia']))
    
    melhor_oferta = candidatos_ordenados[0]["oferta"]
    logger.info(f"Melhor oferta encontrada: ID {melhor_oferta.id} na data {melhor_oferta.data_agendamento} (Distância: {candidatos_ordenados[0]['distancia']:.2f} km)")
    
    return melhor_oferta