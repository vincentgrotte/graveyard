import hashlib
import sys
import random

print()
print()

foundCollision = False
counter = 0
hashMapA = {}
tableSize = 1000000

for i in range(0, tableSize):
	hashA = hashlib.sha256()
	injectionA = i 
	msgA = "Melbourne Cup: $8,000 on Horse 'Steel Prince' [transaction id: " + str(injectionA) + "]"
	# msgA = "Melbourne Cup: $8,000 on Horse 'Phar Lap' (Secret Number) [transaction id: (" + str(injectionA) + ")]"
	hashA.update(msgA.encode('utf-8'))
	frontA = str(hashA.hexdigest())[:8]
	hashMapA[frontA] = injectionA

print("Lookup table populated - size: " + str(tableSize))
print()

while True:
	hashB = hashlib.sha256()
	injectionB = str(random.getrandbits(32))
	msgB = "Melbourne Cup: $8,000 on Horse 'Twilight Payment' [transaction id: " + str(injectionB) + "]"
	# msgB = "Melbourne Cup: $8,000 on Horse 'Sunline' (Excess Knowledge) [transaction id: (" + str(injectionB) + ")]"
	hashB.update(msgB.encode('utf-8'))
	frontB = str(hashB.hexdigest())[:8]
	if (frontB in hashMapA):
		print("Found a collision!")
		print("This attack took " + str(counter) + " attempts")
		print()
		print()
		print("injectionB: " + injectionB)
		print("hashMsgB: " + frontB)
		print("injectionA: " + str(hashMapA[frontB]))
		print("which ostensibly, hashes to the same thing")
		print("ok... let's check")
		hashC = hashlib.sha256() 
		msgC = "MMelbourne Cup: $8,000 on Horse 'Steel Prince' [transaction id: {" + str(hashMapA[frontB]) + "}]"
		# msgC = "Melbourne Cup: $8,000 on Horse 'Phar Lap' (Secret Number) [transaction id: (" + str(hashMapA[frontB]) + ")]"
		hashC.update(msgC.encode('utf-8'))
		frontC = str(hashC.hexdigest())[:8]
		print("the hash of MsgA with injectionA: " + frontC)
		print()
		break
	counter += 1

print()
print()
print("Finito")
print()
print()