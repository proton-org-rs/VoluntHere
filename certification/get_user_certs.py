from solders.pubkey import Pubkey
from anchorpy import Program, Provider, Wallet, Idl
from solana.rpc.async_api import AsyncClient
import asyncio
import json

async def get_user_certificates(user_pubkey: Pubkey, provider: Provider, program: Program):
    """
    Fetch all certificates issued to a specific user.
    
    Args:
        user_pubkey: The public key of the user/recipient
        provider: Anchorpy Provider instance
        program: Anchorpy Program instance
        
    Returns:
        List of dictionaries containing certificate data
    """
    certificates = []
    
    try:
        # Fetch all Certificate accounts from the program
        all_certs = await program.account["Certificate"].all()
        
        # Filter certificates where recipient matches the user
        for cert_account in all_certs:
            if cert_account.account.recipient == user_pubkey:
                certificates.append({
                    "address": str(cert_account.public_key),
                    "issuer": str(cert_account.account.issuer),
                    "recipient": str(cert_account.account.recipient),
                    "event_id": cert_account.account.event_id,
                    "hours": cert_account.account.hours,
                    "issued_at": cert_account.account.issued_at,
                    "revoked": cert_account.account.revoked
                })
        
        return certificates
    
    except Exception as e:
        print(f"Error fetching certificates: {e}")
        return []


async def main():
    # Setup
    provider = Provider(AsyncClient("http://127.0.0.1:8899"), Wallet.local())
    
    with open("volunteer_cert_old_format.json") as f:
        idl_dict = json.load(f)
    idl = Idl.from_json(json.dumps(idl_dict))
    
    program_id = Pubkey.from_string("4LxPhsLVgDxYKuyfy7dAcmYjF79osBMbUN7SsHt7F2zp")
    program = Program(idl, program_id, provider)
    
    # Example: Get all certificates for a user
    user_address = "Bo4CTGafJzyvcij4ee3tyZyMnhLnn9uSgcNFd8dKZqn5"
    user_pubkey = Pubkey.from_string(user_address)
    
    print(f"Fetching certificates for user: {user_address}")
    print("="*60)
    
    certificates = await get_user_certificates(user_pubkey, provider, program)
    
    if certificates:
        print(f"\n✅ Found {len(certificates)} certificate(s):\n")
        for i, cert in enumerate(certificates, 1):
            print(f"Certificate #{i}")
            print(f"  Address: {cert['address']}")
            print(f"  Event ID: {cert['event_id']}")
            print(f"  Hours: {cert['hours']}")
            print(f"  Issued At: {cert['issued_at']}")
            print(f"  Issuer: {cert['issuer']}")
            print(f"  Revoked: {cert['revoked']}")
            print("-"*60)
    else:
        print("❌ No certificates found for this user")


if __name__ == "__main__":
    asyncio.run(main())
