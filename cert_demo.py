import certification
from solders.pubkey import Pubkey
from anchorpy import Program, Provider, Wallet, Idl, Context
from solana.rpc.async_api import AsyncClient
import asyncio
import json
import os
import time

async def main():
    provider = Provider(AsyncClient("http://127.0.0.1:8899"), Wallet.local())

    # Load the old format IDL file
    path = os.path.join("certification", "volunteer_cert_old_format.json")
    with open(path) as f:
        idl_dict = json.load(f)
    
    # Convert to Idl object
    idl = Idl.from_json(json.dumps(idl_dict))
    
    program_id = Pubkey.from_string("4LxPhsLVgDxYKuyfy7dAcmYjF79osBMbUN7SsHt7F2zp")
    program = Program(idl, program_id, provider)

    # Bo4CTGafJzyvcij4ee3tyZyMnhLnn9uSgcNFd8dKZqn5
    recipient_pubkey = Pubkey.from_string(input("Enter recipient public key: "))
    event_id = input("Enter event ID for the certificate: ")

    cert_pubkey = await certification.issue_certificate(recipient_pubkey, event_id, 28, program, provider)

    print(f"Issued certificate account: {cert_pubkey}")

    time.sleep(2)  # Wait a moment for the transaction to finalize

    certs = await certification.get_user_certificates(recipient_pubkey, provider, program)

    print(f"Certificates for user {recipient_pubkey}:")
    print(json.dumps(certs, indent=2))

asyncio.run(main())
