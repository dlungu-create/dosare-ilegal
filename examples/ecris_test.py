import os
from connectors.ecris.client import EcrisClient, EcrisConfig

def main():
    cfg = EcrisConfig(
        wsdl_url=os.getenv("PORTAL_ECRIS_WSDL", "https://portal.just.ro/Services/Portal.svc?wsdl"),
        timeout=float(os.getenv("PORTAL_ECRIS_TIMEOUT", "30")),
        verify_ssl=True
    )
    client = EcrisClient(cfg)

    print("=== Introspecție WSDL (scurt) ===")
    try:
        print(client.debug_introspection())
    except Exception as e:
        print("Eroare la introspecție:", e)

    sample_case = "48518/3/2012"  # exemplu
    try:
        resp = client.get_case_by_number(sample_case)
        print("=== Răspuns căutare dosar ===")
        print(resp)
    except Exception as e:
        print("Eroare la CautaDosare:", e)

    try:
        hearings = client.get_hearings(id_instanta=2, data_sedinta="2025-09-01")
        print("=== Răspuns ședințe ===")
        print(hearings)
    except Exception as e:
        print("Eroare la CautaSedinte:", e)

if __name__ == "__main__":
    main()
