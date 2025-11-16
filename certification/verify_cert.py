from solders.pubkey import Pubkey
from anchorpy import Program, Provider, Wallet, Idl
from solana.rpc.async_api import AsyncClient
import asyncio
import json

async def main():
    provider = Provider(AsyncClient("http://127.0.0.1:8899"), Wallet.local())
    
    with open("volunteer_cert_old_format.json") as f:
        idl_dict = json.load(f)
    idl = Idl.from_json(json.dumps(idl_dict))
    
    program_id = Pubkey.from_string("4LxPhsLVgDxYKuyfy7dAcmYjF79osBMbUN7SsHt7F2zp")
    program = Program(idl, program_id, provider)
    
    # The certificate PDA we just created
    certificate_pubkey = Pubkey.from_string("2QHooPzMA6A6bM4XukHYfNSchN69MprPUxRfDCAy2sbv")
    
    # Fetch the certificate data
    cert = await program.account["Certificate"].fetch(certificate_pubkey)
    
    print("📜 Certificate Details:")
    print("="*60)
    print(f"Issuer: {cert.issuer}")
    print(f"Recipient: {cert.recipient}")
    print(f"Event ID: {cert.event_id}")
    print(f"Hours: {cert.hours}")
    print(f"Issued At: {cert.issued_at}")
    print(f"Revoked: {cert.revoked}")

asyncio.run(main())