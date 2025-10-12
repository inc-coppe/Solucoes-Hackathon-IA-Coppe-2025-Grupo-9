from faker import Faker
from sqlalchemy.orm import Session
from . import models
from .logging_config import logger
from random import choice, randint
from datetime import date, timedelta

fake = Faker('pt_BR')

def generate_fake_data(db: Session):
    if db.query(models.Unidade).count() > 0:
        logger.info("Dados já existem no banco. Geração de dados pulada.")
        return

    logger.info("Gerando dados sintéticos...")

    # Gerar Unidades de Saúde (usando um método mais robusto do Faker)
    unidades = []
    for i in range(10):
        # Gera uma tupla com (latitude, longitude, cidade, país, timezone) para o Brasil
        lat, lon, _, _, _ = fake.local_latlng(country_code='BR')
        unidade = models.Unidade(
            cnes_id=f"CNES_{i+1}",
            nome=fake.company() + " - Unidade de Saúde",
            latitude=float(lat),
            longitude=float(lon)
        )
        unidades.append(unidade)
    db.add_all(unidades)
    db.commit()

    # Gerar Procedimentos
    procedimentos_nomes = ["CONSULTA CARDIOLOGIA", "RAIO-X DE TORAX", "EXAME DE SANGUE", "FISIOTERAPIA MOTORA"]
    procedimentos = []
    for i, nome in enumerate(procedimentos_nomes):
        proc = models.Procedimento(procedimento_id=f"PROC_{i+1}", nome=nome)
        procedimentos.append(proc)
    db.add_all(procedimentos)
    db.commit()

    # Gerar Ofertas Programadas (Agenda)
    ofertas = []
    today = date.today()
    for unidade in db.query(models.Unidade).all():
        for _ in range(5):
            proc = choice(db.query(models.Procedimento).all())
            data_oferta = today + timedelta(days=randint(1, 30))
            oferta = models.OfertaProgramada(
                unidade_id=unidade.id,
                procedimento_id=proc.id,
                data_agendamento=data_oferta,
                vagas_disponiveis=randint(1, 5)
            )
            ofertas.append(oferta)
    db.add_all(ofertas)
    db.commit()

    logger.info("Geração de dados sintéticos concluída.")