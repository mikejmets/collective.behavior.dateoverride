"""Upgrade step to add event date override indexes to catalog"""
from plone import api


def add_event_date_override_indexes(context):
    """Add event_date_override and event_date_override_text to catalog.
    
    This upgrade step:
    1. Adds the indexes if they don't exist
    2. Adds the metadata columns if they don't exist
    3. Reindexes all objects with the behavior
    """
    catalog = api.portal.get_tool('portal_catalog')
    
    # Add indexes
    indexes_to_add = {
        'event_date_override': 'BooleanIndex',
        'event_date_override_text': 'FieldIndex',
    }
    
    existing_indexes = catalog.indexes()
    
    for index_name, index_type in indexes_to_add.items():
        if index_name not in existing_indexes:
            catalog.addIndex(index_name, index_type)
            print(f"Added {index_type} '{index_name}' to catalog")
        else:
            print(f"Index '{index_name}' already exists")
    
    # Add metadata columns
    existing_metadata = catalog.schema()
    
    for column_name in indexes_to_add.keys():
        if column_name not in existing_metadata:
            catalog.addColumn(column_name)
            print(f"Added metadata column '{column_name}'")
        else:
            print(f"Metadata column '{column_name}' already exists")
    
    # Reindex all objects
    # This is safe - indexers return default values for objects without the behavior
    print("Reindexing event_date_override and event_date_override_text...")
    catalog.manage_reindexIndex(ids=list(indexes_to_add.keys()))
    print("Reindexing complete")
