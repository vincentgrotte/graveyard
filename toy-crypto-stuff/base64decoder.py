import base64

txt = "KNXSYIDFNZRW6ZDJNZTSA2LTEBXG65BAMVXGG6LSOB2GS33OFYXC4==="
hex = base64.b32decode(txt).hex()
message = bytearray.fromhex(hex).decode()
print(message)