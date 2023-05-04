"""
Blockchain
"""

import datetime as dt
import json as jsn
import hashlib as hl
from flask import Flask, jsonify

class Blockchain:

    #Constructor
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash=0)

    # Add blocks at chain
    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "time_stamp": str(dt.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash
        }
        self.chain.append(block)
        return block

    #Return the last block
    def get_previous_block(self):
        return self.chain[-1]

    #Proof of work (PoW)
    def proof_of_work(self, previous_hash):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hl.sha256(str(new_proof**2 - previous_hash**2).encode()).hexdigest()
            if hash_operation[4:] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    #Return the hash
    def hash(self, block):
        encode_block = jsn.dumps(block, sort_keys=True).encode()
        return hl.sha256(encode_block).hexdigest()

    #Validate chain
    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_block = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hl.sha256(str(proof**2 - previous_block**2).encode()).hexdigest()
            if hash_operation[4:] != "0000":
                return False

            previous_block = block
            block_index += 1

        return True

#Creation of the APP

app = Flask(__name__)

blockchain = Blockchain()

