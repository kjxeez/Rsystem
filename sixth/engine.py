import hashlib
from time import time
import json
import requests
from urllib.parse import urlparse


def mine(blockchain):
    end_block = blockchain.end_block
    prove = blockchain.prove_of_work(end_block)

    last_hash = blockchain.hash(end_block)
    block = blockchain.new_block(prove, last_hash)

    Feedback = {
        'ser_mes': "New fake block",
        'index': block['index'],
        'procedure': block['procedure'],
        'prove': block['prove'],
        'last_hash': block['last_hash'],
    }
    return Feedback  # print(Feedback)


class Blockchain:
    def __init__(self):
        self.current_procedure = []
        self.chain = []
        self.hosts = set()

        self.new_block(last_hash='1', prove=100)  # Create the genesis block

    def register_host(self, address):
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.hosts.add(parsed_url.netloc)
        elif parsed_url.path:

            self.hosts.add(parsed_url.path)  # Accepts an URL without scheme like '192.168.0.5:5000'
        else:
            raise ValueError('Неверный URL-адрес')

    def valid_chain(self, chain):
        end_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{end_block}')
            print(f'{block}')
            print("\n----------------\n")
            end_block_hash = self.hash(end_block)  # Check that the hash of the block is correct
            if block['last_hash'] != end_block_hash:
                return False

            if not self.valid_prove(end_block['prove'], block['prove'],
                                    end_block_hash):  # Check that the prove of Work is correct
                return False

            end_block = block
            current_index += 1
        return True

    def resolve_conflicts(self):
        relative = self.hosts
        new_chain = None
        max_length = len(self.chain)  # We're only looking for chains longer than ours

        for host in relative:  # Grab and verify the chains from all the hosts in our network
            Feedback = requests.get(f'http://{host}/chain')

            if Feedback.status_code == 200:
                length = Feedback.json()['длина']
                chain = Feedback.json()['сеть']

                if length > max_length and self.valid_chain(
                        chain):  # Check if the length is longer and the chain is valid
                    max_length = length
                    new_chain = chain
        if new_chain:  # Replace our chain if we discovered a new, valid chain longer than ours
            self.chain = new_chain
            return True
        return False

    def new_block(self, prove, last_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'procedure': self.current_procedure,
            'prove': prove,
            'last_hash': last_hash or self.hash(self.chain[-1]),
        }

        self.current_procedure = []  # Reset the current list of procedure

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_procedure.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.end_block['index'] + 1

    @property
    def end_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def prove_of_work(self, end_block):
        last_prove = end_block['prove']
        last_hash = self.hash(end_block)

        prove = 0
        while self.valid_prove(last_prove, prove, last_hash) is False:
            prove += 1

        return prove

    @staticmethod
    def valid_prove(last_prove, prove, last_hash):
        predict = f'{last_prove}{prove}{last_hash}'.encode()
        predict_hash = hashlib.sha256(predict).hexdigest()
        return predict_hash[:4] == "0000"


def get_end_block(blockchain):
    Feedback = blockchain.end_block
    return Feedback