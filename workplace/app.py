from uuid import uuid4
from flask import Flask, jsonify, request

from .cryptocurrency.cryptocurrency import Blockchain

app = Flask(__name__)

node_address = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    return response, 200


@app.route('/mine_block', methods=['GET'])
def mine_block():
    """
    The blockchain is public. In this case everyone has access
    to the chain. If you want to mine it you can.
    """

    # Access the last item in the chain
    previous_block = blockchain.get_previous_block()

    # This is what you need for mining
    previous_proof = previous_block['proof']

    # This is the actual mining. Tryig to solve a problem.
    proof = blockchain.proof_of_worf(previous_proof)

    # with a proof at hands now you are good to go on creating a new block
    previous_hash = blockchain.hash(previous_block)

    # Add a transaction to your wallet since you are going to mine the block!
    blockchain.add_transaction(
        sender=node_address,
        receiver='Fernando',
        amount=1
    )

    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Congratulations on mining a new block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'transactions': block['transactions']
    }

    return jsonify(response), 200


@app.route('/is_chain_valid')
def is_chain_valid():
    return jsonify(blockchain.is_chain_valid(blockchain.chain)), 200


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Misising information elements', 400
    index = blockchain.add_transaction(
        json['sender'],
        json['receiver'],
        json['amount']
    )
    response = {'message': f'This transaction will be added to block {index}'}
    return jsonify(response), 201


@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'Empty', 400
    for node in nodes:
        blockchain.add_node(node)
    response = {
        "message": "All following nodes connected:",
        "total_node": list(blockchain.nodes)
    }
    return jsonify(response), 201


@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {
            "message": "The chain was replaced",
            "new_chain": blockchain.chain
        }
    else:
        response = {
            "message": "The chain was not replaced",
            "chain": blockchain.chain
        }
    return jsonify(response), 200


@app.route('/')
def hello_world():
    return 'Hello, as!'
