# Cole este mesmo conteúdo nos dois arquivos Dockerfile

# Use uma imagem base oficial do Python
FROM python:3.10-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY ./requirements.txt /app/requirements.txt

# Instale as dependências
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copie o código da aplicação para o container
COPY ./src /app/src

# Comando para executar a aplicação com Uvicorn
# --host 0.0.0.0 é crucial para expor a aplicação fora do container
# --reload irá reiniciar o servidor automaticamente quando houver mudanças no código (ótimo para desenvolvimento)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]