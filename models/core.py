from django.shortcuts import get_object_or_404
from django.core.cache import cache
from abc import ABC , ABCMeta , abstractmethod


def make_a_cache_to_models(self):
    models_cache = get_object_or_404("accounts.value" , pk = 1 )    
    return None


@abstractmethod
def some(self):
    return None



def new_class_var(self , val):
    self.val = val
    return val
    

