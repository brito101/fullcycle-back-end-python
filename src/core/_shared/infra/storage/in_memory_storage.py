from pathlib import Path
from typing import Dict

from src.core._shared.infra.storage.abstract_storage import AbstractStorage


class InMemoryStorage(AbstractStorage):
    """
    Implementação de storage em memória para testes.
    Armazena arquivos em um dicionário em memória.
    """
    
    def __init__(self):
        self._storage: Dict[str, bytes] = {}
    
    def store(self, file_path: Path, content: bytes, content_type: str = "") -> str:
        """Armazena um arquivo em memória"""
        key = str(file_path)
        self._storage[key] = content
        return f"memory://{key}"
    
    def retrieve(self, file_path: Path) -> bytes:
        """Recupera um arquivo da memória"""
        key = str(file_path)
        if key not in self._storage:
            raise FileNotFoundError(f"File {file_path} not found in memory storage")
        return self._storage[key]
    
    def clear(self):
        """Limpa todo o storage em memória"""
        self._storage.clear()
