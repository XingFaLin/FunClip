#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Copyright FunASR (https://github.com/alibaba-damo-academy/FunClip). All Rights Reserved.
#  MIT License  (https://opensource.org/licenses/MIT)

from http import server
import os
import logging
import argparse
import gradio as gr
import toml
from funasr import AutoModel
from pathlib import Path

from videoclipper import VideoClipper
from llm.openai_api import openai_call
from llm.qwen_api import call_qwen_model
from llm.g4f_openai_api.py