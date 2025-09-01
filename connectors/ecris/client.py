import os
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

from zeep import Client, Settings
from zeep.transports import Transport
import httpx

load_dotenv()

DEFAULT_WSDL = os.getenv(
    "PORTAL_ECRIS_WSDL",
    "https://portal.just.ro/Services/Portal.svc?wsdl"
)
TIMEOUT = float(os.getenv("PORTAL_ECRIS_TIMEOUT", "30"))

@dataclass
class EcrisConfig:
    wsdl_url: str = DEFAULT_WSDL
    timeout: float = TIMEOUT
    verify_ssl: bool = True  # dacă apar erori TLS local, poți seta False

class EcrisClient:
    """Client minim pentru serviciul web al portalului instanțelor (ECRIS)."""

    def __init__(self, config: Optional[EcrisConfig] = None):
        self.config = config or EcrisConfig()
        self._client = self._build_client()

    def _build_client(self) -> Client:
        settings = Settings(strict=False, xml_huge_tree=True)
        http = httpx.Client(timeout=self.config.timeout, verify=self.config.verify_ssl)
        transport = Transport(client=http)
        return Client(wsdl=self.config.wsdl_url, settings=settings, transport=transport)

    def get_case_by_number(self, numar_unic: str) -> Dict[str, Any]:
        """Returnează detalii dosar pentru `numar_unic` (ex: '12345/3/2024')."""
        svc = self._client.service
        try:
            return svc.CautaDosare(numarUnic=numar_unic)
        except Exception:
            return svc.CautaDosare(numar_unic=numar_unic)

    def get_hearings(self, id_instanta: int, data_sedinta: str) -> List[Dict[str, Any]]:
        """Lista ședințelor pentru `id_instanta` și `data_sedinta` (YYYY-MM-DD)."""
        svc = self._client.service
        resp = svc.CautaSedinte(instanta=id_instanta, data=data_sedinta)
        if resp is None:
            return []
        if isinstance(resp, list):
            return [dict(x) for x in resp]
        try:
            return [dict(resp)]
        except Exception:
            return [resp]

    def debug_introspection(self) -> str:
        return self._client.wsdl.dump()
