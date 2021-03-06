
import datetime
import hashlib
import requests
import json

from flask import Flask
from urllib.parse import urlparse


class Blockchain:
    def __init__(self):
        self.chain = []
        # A blockchain starts with zero transactions
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'previous_hash': previous_hash,
            'proof': proof,
            'transactions': self.transactions,
        }
        # Clean transactions after creating a block
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_worf(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:

            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()
            ).hexdigest()

            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()
            ).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append(
            {'sender': sender, 'receiver': receiver, 'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block["index"] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        # netloc adds the address without the schema/protocol
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        """
        Consensus implementation

        Checking all nodes for longest and valid chain to replace
        current chain.
        """
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)

        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                response_json = response.json()
                node_chain_length = response_json['length']
                node_chain = response_json['chain']

                if node_chain_length > max_length and self.is_chain_valid(node_chain):
                    max_length = node_chain_length
                    longest_chain = node_chain

        if longest_chain:
            self.chain = longest_chain
            return True
        return False
