# -*- coding: utf-8 -*-
"""This module contains an empty application container.
It is defined here to avoid circular imports
"""
from mindmeld import Application
from mindmeld.components import QuestionAnswerer

app = Application(__name__)

__all__ = ['app']

qa = QuestionAnswerer(app_path='nlp_intern')
qa.load_kb(app_namespace='placement', index_name='companies',
           data_file='nlp_intern/data/companies.json')
