import logging
import sys

def setup_logging():
    """Configura o logger para garantir que as mensagens apareçam no Docker."""
    
    # Obtém o logger raiz
    logger = logging.getLogger()
    
    # Define o nível de log. INFO significa que mensagens de INFO, WARNING, ERROR, CRITICAL serão exibidas.
    logger.setLevel(logging.INFO)
    
    # Cria um handler que envia os logs para a saída padrão (o terminal)
    # sys.stdout garante que a saída não seja bufferizada, resolvendo nosso problema.
    handler = logging.StreamHandler(sys.stdout)
    
    # Define o formato da mensagem de log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Adiciona o handler ao logger
    # Checamos se já não existem handlers para não duplicar logs
    if not logger.handlers:
        logger.addHandler(handler)

    return logger

# Cria uma instância do logger para ser importada por outros módulos
logger = setup_logging()