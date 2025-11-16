import certification.user_blockchain_service
import asyncio
import json
from random import randint


async def main():
    service = certification.user_blockchain_service.UserBlockchainService("http://despot-flex7:8899")

    user = await service.create_and_register_user("test_user_123", "test@gmail.com", "Test User")
    print(f"Loaded user: {user}")

    print('\n')

    try:
        cert = await service.issue_certificate_to_user(user["user_id"], "skiing", randint(1, 10))
        print(f"Issued certificate: {json.dumps(cert,indent=2)}")
    except Exception as e:
        print(f"Error issuing certificate: {e}")
    
    print('\n')
    for i in range(30):
        print(f"Sleeping for {30-i}s...")
        await asyncio.sleep(1)

    certs = await service.get_user_certificates(user["user_id"], include_revoked=False)
    print(f"User has {len(certs)} certificates:")
    for c in certs:
        print(f"- {json.dumps(c, indent=2)}")

    print('\n')

    stats = await service.get_user_statistics(user["user_id"])
    print(f"User statistics: {json.dumps(stats, indent=2)}")

asyncio.run(main())
