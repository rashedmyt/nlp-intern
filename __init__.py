# -*- coding: utf-8 -*-
"""This module contains a template MindMeld application"""
from nlp_intern.root import app

import nlp_intern.handlers.greeting
import nlp_intern.handlers.unsupported
import nlp_intern.handlers.placement_info
import nlp_intern.handlers.company_info

__all__ = ['app']
