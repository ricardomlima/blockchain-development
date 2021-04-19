from flask import Flask, jsonify

from .creating_blockchain.blockchain import Blockchain

app = Flask(__name__)

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
    block = blockchain.create_block(proof, previous_hash)

    response = {
        'message': 'Congratulations on mining a new block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200


@app.route('/')
def hello_world():
    return 'Hello, as!'
