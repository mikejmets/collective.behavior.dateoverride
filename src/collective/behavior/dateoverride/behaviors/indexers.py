"""Indexers for event date override behavior"""
from plone.indexer import indexer
from zope.interface import Interface
from .dateoverride import IEventDateOverride


@indexer(Interface)
def event_date_override_indexer(obj):
    """Index event_date_override field.
    
    Returns False for objects that don't have the behavior.
    This ensures the catalog always has a value.
    """
    behavior = IEventDateOverride(obj, None)
    if behavior is not None:
        return getattr(behavior, 'event_date_override', False)
    return False


@indexer(Interface)
def event_date_override_text_indexer(obj):
    """Index event_date_override_text field.
    
    Returns None for objects that don't have the behavior.
    """
    behavior = IEventDateOverride(obj, None)
    if behavior is not None:
        return getattr(behavior, 'event_date_override_text', None)
    return None
