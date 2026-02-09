"""Behavior to add event date override fields to events"""
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IEventDateOverride(model.Schema):
    """Behavior to add date override fields to events"""
    
    model.fieldset(
        'dates',
        label='Dates',
        fields=['event_date_override', 'event_date_override_text']
    )
    
    event_date_override = schema.Bool(
        title='Override Event Date Display',
        description='Check this to display custom text instead of the actual event date',
        required=False,
        default=False,
    )
    
    event_date_override_text = schema.Text(
        title='Event Date Override Text',
        description='Text to display instead of the event date (e.g., "Coming Soon", "TBA")',
        required=False,
    )
