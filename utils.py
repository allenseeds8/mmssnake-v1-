import re
import logging
import requests
from services.instagram_service import get_instagram_service
from database import Session
from models.base import Payments

# Configuração básica do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Configuração da API SMM
SMM_CONFIG = {
    'machinesmm': {'base_url': 'https://machinesmm.com/api/v2', 'api_key': '7933dcebc18d85d7486c1666a1ae3d4d'},
    'worldsmm': {'base_url': 'https://worldsmm.com.br/api/v2', 'api_key': '1287cfd6baf5e432500591201bc121e3'},
    'smmclouduk': {'base_url': 'https://smmcloud.uk/api/v2', 'api_key': '1c900607f193909296d6c8a5573fa4c1'}
}

logger = logging.getLogger(__name__)  # Para usar com from utils import logger


# Apagar pedido após entregue
def delete_payment_internal(payment_id):
    """Função auxiliar para uso interno na aplicação."""
    from database import Session  # Ajuste conforme necessário
    session = Session()
    try:
        payment = session.query(Payments).filter_by(id=payment_id).first()
        if not payment:
            return False, "Pagamento não encontrado"
        
        session.delete(payment)
        session.commit()
        return True, "Pagamento deletado"
    
    except Exception as e:
        session.rollback()
        return False, str(e)
    
    finally:
        session.close()




#Sanitizar username conforme a Yampi 
def sanitize_customization(customization):
    # Padrão atualizado para capturar os casos específicos
    match = re.match(
        r'^(?:@|httpswww\.instagram\.com|www\.instagram\.com)([^?]*)', 
        customization
    )
    
    if match:
        # Retorna o username capturado (grupo 1)
        return match.group(1)
    else:
        # Remove caracteres não permitidos (exceto letras, números, underscores e pontos)
        return re.sub(r'[^\w\.]', '', customization)
