#!/bin/bash -e

virtualenv -p python3 .genanki-env
source .genanki-env/bin/activate
pip install genanki

