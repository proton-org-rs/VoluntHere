from solders.pubkey import Pubkey
from anchorpy import Program, Provider, Wallet, Idl, Context
from solana.rpc.async_api import AsyncClient
import asyncio
import json

async def issue_certificate(recipient_pubkey: Pubkey, event_id: str, hours: int, program: Program, provider: Provider):
    # Compute PDA for certificate account
    seeds = [b"certificate", bytes(recipient_pubkey), event_id.encode('utf-8')]
    certificate_pubkey, bump = Pubkey.find_program_address(seeds, program.program_id)

    # print(f"Certificate PDA: {certificate_pubkey}")
    # print(f"Issuing certificate for {event_id} to {recipient_pubkey}...")

    try:
        # Create the context properly using Context class
        ctx = Context(
            accounts={
                "issuer": provider.wallet.public_key,
                "recipient": recipient_pubkey,
                "certificate": certificate_pubkey,
                "system_program": Pubkey.from_string("11111111111111111111111111111111")
            }
        )
        
        tx_sig = await program.rpc["issue_certificate"](
            event_id,
            28,  # hours (u16)
            ctx=ctx
        )
        print(f"✅ Certificate issued successfully!")
        print(f"   Transaction signature: {tx_sig}")
        print(f"   Certificate account: {certificate_pubkey}")
        return certificate_pubkey
    except Exception as e:
        print(f"❌ Error issuing certificate: {e}")
        import traceback
        traceback.print_exc()


async def main():
    provider = Provider(AsyncClient("http://127.0.0.1:8899"), Wallet.local())

    # Load the old format IDL file
    with open("volunteer_cert_old_format.json") as f:
        idl_dict = json.load(f)
    
    # Convert to Idl object
    idl = Idl.from_json(json.dumps(idl_dict))
    
    program_id = Pubkey.from_string("4LxPhsLVgDxYKuyfy7dAcmYjF79osBMbUN7SsHt7F2zp")
    program = Program(idl, program_id, provider)

    recipient_pubkey = Pubkey.from_string("Bo4CTGafJzyvcij4ee3tyZyMnhLnn9uSgcNFd8dKZqn5")
    event_id = "bowling"

    cert_pubkey = await issue_certificate(recipient_pubkey, event_id, 28, program, provider)

    print(f"Issued certificate account: {cert_pubkey}")


if __name__ == "__main__":
    asyncio.run(main())
