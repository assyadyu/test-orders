#!/bin/bash

python -m pytest tests/ -s -vv -W ignore::DeprecationWarning
