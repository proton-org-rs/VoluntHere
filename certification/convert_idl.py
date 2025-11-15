import json

# Load the new format IDL
with open("volunteer_cert_decoded.json") as f:
    new_idl = json.load(f)

# Convert to old format (pre-0.30)
old_format = {
    "version": new_idl["metadata"]["version"],
    "name": new_idl["metadata"]["name"],
    "instructions": [],
    "accounts": [],
    "types": new_idl.get("types", []),
    "errors": new_idl.get("errors", [])
}

# Convert instructions
for instr in new_idl["instructions"]:
    old_instr = {
        "name": instr["name"],
        "accounts": [],
        "args": instr["args"]
    }
    
    # Convert accounts
    for acc in instr["accounts"]:
        old_acc = {
            "name": acc["name"],
            "isMut": acc.get("writable", False),
            "isSigner": acc.get("signer", False)
        }
        old_instr["accounts"].append(old_acc)
    
    old_format["instructions"].append(old_instr)

# Convert account types
for acc_type in new_idl.get("accounts", []):
    # Find the corresponding type definition
    for type_def in new_idl.get("types", []):
        if type_def["name"] == acc_type["name"]:
            old_format["accounts"].append({
                "name": acc_type["name"],
                "type": type_def["type"]
            })

# Save converted IDL
with open("volunteer_cert_old_format.json", "w") as f:
    json.dump(old_format, f, indent=2)

print("✅ Converted IDL to old format")
print("   Saved to: volunteer_cert_old_format.json")