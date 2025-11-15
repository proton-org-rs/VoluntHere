import certification
from solders.pubkey import Pubkey
from anchorpy import Program, Provider, Wallet, Idl, Context
from solana.rpc.async_api import AsyncClient
import asyncio
import json
import os
import time
from random import randint

import certification.user_blockchain_service

async def main():
    service = certification.user_blockchain_service.UserBlockchainService()

    user = await service.create_and_register_user("test_user_123", "test@gmail.com", "Test User")
    print(f"Loaded user: {user}")

    # try:
    #     cert = await service.issue_certificate_to_user(user["user_id"], "event_456", randint(1, 10))
    #     print(f"Issued certificate: {cert}")

    # except Exception as e:
    #     print(f"Error issuing certificate: {e}")
    
    certs = await service.get_user_certificates(user["user_id"], include_revoked=False)
    print(f"User has {len(certs)} certificates:")
    for c in certs:
        print(f"- {c}")

    stats = await service.get_user_statistics(user["user_id"])
    print(f"User statistics: {stats}")

asyncio.run(main())
