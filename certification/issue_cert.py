from solders.pubkey import Pubkey
from anchorpy import Program, Provider, Wallet
from solana.rpc.async_api import AsyncClient
import asyncio

async def main():
    provider = Provider(AsyncClient("http://172.17.113.189:8899"), Wallet.local())  # adjust for localnet/devnet
    program = await Program.at("4LxPhsLVgDxYKuyfy7dAcmYjF79osBMbUN7SsHt7F2zp", provider)

    recipient_pubkey = Pubkey("Bo4CTGafJzyvcij4ee3tyZyMnhLnn9uSgcNFd8dKZqn5")
    event_id = "hackathon1"

    # Compute PDA for certificate account
    seeds = [b"certificate", bytes(recipient_pubkey), bytes(event_id, "utf-8")]
    certificate_pubkey, _ = Pubkey.find_program_address(seeds, program.program_id)

    await program.rpc["issue_certificate"](
        event_id,
        5,  # hours
        ctx={
            "accounts": {
                "issuer": provider.wallet.public_key,
                "recipient": recipient_pubkey,
                "certificate": certificate_pubkey,
                "system_program": Pubkey("11111111111111111111111111111111")
            }
        }
    )
    print("Certificate issued at PDA:", certificate_pubkey)

asyncio.run(main())
