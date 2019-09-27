import os
import subprocess
from flask import Flask, abort, request, jsonify, g, url_for, make_response
from flask_restplus import Api, Resource, fields, Namespace
from flask_cors import CORS
import datetime
from jsonschema import validate
import json

import hashlib
from nanolib import Block, generate_account_id, generate_account_private_key, get_account_id
import requests
from tinydb import TinyDB, Query
db = TinyDB('db.json')

# Environmental variables
# Init app 
app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Bionet Index',
            description='Bionet Index 1 try'
            )

ns_blast = Namespace('blast',description='Blast on the Bionet')
blast_model = ns_blast.schema_model('blast_seq',{"type":"object","properties": {"search_sequence": {"type": "string"}}, "required": ["search_sequence"],"additionalProperties": False})

@ns_blast.route('/')
class BlastRoute(Resource):
    @ns_blast.doc('blast')
    @ns_blast.expect(blast_model)
    def post(self):
        f = open("files/test_query.fa", "w")
        f.write("> Query Sequence")
        f.write("\n")
        f.write(request.get_json()['search_sequence'])
        f.write("\n")
        f.close()
        output = json.loads(subprocess.check_output("blastn -db blastdb/blast.db -query files/test_query.fa -outfmt 15",shell=True).decode("utf-8"))
        return output

ns_google_docs = Namespace('google_docs',description='Add a google doc to the Bionet!')
google_model = ns_blast.schema_model('add_google_doc',
        {"type":"object","properties": 
            {"email": {"type": "string"}, 
            "url": {"type": "string"}}, 
            "required": ["email","url"],
            "additionalProperties": False})

@ns_google_docs.route('/add/')
class AddGoogleDoc(Resource):
    @ns_google_docs.doc('add')
    @ns_google_docs.expect(google_model)
    def post(self):
        db.insert(request.get_json())
        return request.get_json()


api.add_namespace(ns_blast)
api.add_namespace(ns_google_docs)
