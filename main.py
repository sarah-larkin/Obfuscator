from input.validators import ObfuscationRequest
from services.obfuscation_service import ObfuscationService

def main(input_json: str):
    request = ObfuscationRequest(input_json)
    service = ObfuscationService()
    service.run(request)