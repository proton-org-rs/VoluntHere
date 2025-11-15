from solders.pubkey import Pubkey
from anchorpy import Program, Provider, Wallet, Idl, Context
from solana.rpc.async_api import AsyncClient
from wallet_manager import WalletManager
import asyncio
import json
import os

async def register_user_on_blockchain(user_id: str, rpc_url: str = "http://127.0.0.1:8899"):
    """
    Register a new user on the blockchain by issuing them a registration certificate.
    
    Args:
        user_id: User identifier
        rpc_url: RPC endpoint
    """
    # Initialize wallet manager
    wallet_manager = WalletManager()
    
    # Check if user already has a wallet
    user_pubkey_str = wallet_manager.get_user_public_key(user_id)
    
    if not user_pubkey_str:
        # Create new wallet for user
        print(f"Creating new wallet for {user_id}...")
        wallet_info = wallet_manager.create_user_wallet(user_id)
        user_pubkey_str = wallet_info["public_key"]
        
        # Fund the wallet
        print(f"Funding wallet...")
        await wallet_manager.fund_user_wallet(user_id, amount_sol=2.0, rpc_url=rpc_url)
    else:
        print(f"Wallet already exists for {user_id}")
    
    # Setup provider (platform's admin wallet issues the certificate)
    provider = Provider(AsyncClient(rpc_url), Wallet.local())
    
    # Load program IDL
    with open("volunteer_cert_old_format.json") as f:
        idl_dict = json.load(f)
    idl = Idl.from_json(json.dumps(idl_dict))
    
    program_id = Pubkey.from_string("4LxPhsLVgDxYKuyfy7dAcmYjF79osBMbUN7SsHt7F2zp")
    program = Program(idl, program_id, provider)
    
    # Issue a "registration" certificate
    user_pubkey = Pubkey.from_string(user_pubkey_str)
    event_id = f"registration_{user_id}"
    
    # Compute PDA for registration certificate
    seeds = [b"certificate", bytes(user_pubkey), event_id.encode('utf-8')]
    certificate_pubkey, bump = Pubkey.find_program_address(seeds, program.program_id)
    
    print(f"\nRegistering user on blockchain...")
    print(f"  User: {user_id}")
    print(f"  Public Key: {user_pubkey}")
    print(f"  Registration Certificate PDA: {certificate_pubkey}")
    
    try:
        ctx = Context(
            accounts={
                "issuer": provider.wallet.public_key,
                "recipient": user_pubkey,
                "certificate": certificate_pubkey,
                "system_program": Pubkey.from_string("11111111111111111111111111111111")
            }
        )
        
        tx_sig = await program.rpc["issue_certificate"](
            event_id,
            0,  # 0 hours for registration certificate
            ctx=ctx
        )
        
        print(f"\n✅ User registered on blockchain!")
        print(f"   Transaction: {tx_sig}")
        print(f"   Certificate: {certificate_pubkey}")
        
        return {
            "user_id": user_id,
            "public_key": user_pubkey_str,
            "registration_certificate": str(certificate_pubkey),
            "transaction": str(tx_sig)
        }
        
    except Exception as e:
        print(f"❌ Registration failed: {e}")
        import traceback
        traceback.print_exc()
        return None


async def main():
    """Register multiple users"""
    
    users = [
        "alice@volunthere.com",
        "bob@volunthere.com",
        "charlie@volunthere.com"
    ]
    
    print("="*60)
    print("REGISTERING USERS ON BLOCKCHAIN")
    print("="*60)
    
    for user_id in users:
        result = await register_user_on_blockchain(user_id)
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
