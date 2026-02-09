# collective.behavior.dateoverride

[![PyPI](https://img.shields.io/pypi/v/collective.behavior.dateoverride)](https://pypi.org/project/collective.behavior.dateoverride/)
[![Plone](https://img.shields.io/badge/Plone-5.2%20%7C%206.0-blue)](https://plone.org)

A Plone behavior that allows events to override their date display with custom text.

## Use Case

Sometimes you need to display events with uncertain or flexible dates:

- "Coming Soon" - for events without confirmed dates
- "TBA" - to be announced
- "Spring 2025" - seasonal rather than specific dates
- "Multiple Dates - See Details" - for recurring events

This behavior adds two fields to events that let you override the date display while keeping the actual dates for calendar/sorting purposes.

## Features

- ✅ Simple checkbox to enable date override
- ✅ Custom text field for display
- ✅ Catalog indexes for efficient querying
- ✅ Works with Collections and event listings
- ✅ No performance overhead (uses catalog metadata)
- ✅ Safe for mixed content (non-events get safe defaults)
- ✅ Compatible with Plone 5.2 and 6.0

## Installation

Add to your buildout:

```ini
[buildout]
eggs =
    collective.behavior.dateoverride
```

Run buildout:

```bash
bin/buildout
```

Install the add-on:

1. Go to Site Setup → Add-ons
2. Install "Event Date Override Behavior"

## Usage

### Enable the Behavior

1. Go to Site Setup → Dexterity Content Types
2. Click on "Event"
3. Go to the "Behaviors" tab
4. Check "Event Date Override"
5. Save

### In the Event Edit Form

When editing an event, you'll see two new fields in the "Dates" fieldset:

1. **Override Event Date Display** - Checkbox to enable the override
2. **Event Date Override Text** - Custom text to display

### In Templates

The fields are available as direct attributes:

```python
# In Python
if event.event_date_override:
    display_text = event.event_date_override_text
else:
    display_text = event.start.strftime('%B %d, %Y')
```

```xml
<!-- In TAL -->
<tal:override condition="context/event_date_override">
    <span tal:content="context/event_date_override_text">Coming Soon</span>
</tal:override>
<tal:normal condition="not:context/event_date_override">
    <span tal:content="python:context.start.strftime('%B %d, %Y')">Jan 15, 2025</span>
</tal:normal>
```

### In Collections and Listings

The fields are available as catalog metadata on brains:

```python
# No getObject() needed - uses catalog metadata
for brain in results:
    if brain.event_date_override:
        date_text = brain.event_date_override_text
    else:
        date_text = brain.start.strftime('%B %d, %Y')
```

```xml
<!-- In isotope or other listing templates -->
<tal:items repeat="brain view/results">
    <tal:override condition="brain/event_date_override">
        <span tal:content="brain/event_date_override_text">TBA</span>
    </tal:override>
    <tal:normal condition="not:brain/event_date_override">
        <span tal:content="python:brain.start.strftime('%B %d, %Y')">Date</span>
    </tal:normal>
</tal:items>
```

### In Collection Criteria

You can also use the fields as Collection criteria:

- **Event Date Override** - Boolean field to filter events with overrides
- **Event Date Override Text** - Text field to search for specific override messages

## How It Works

### Storage

The behavior uses `DexteritySchemaPolicy`, storing fields as direct attributes on event objects for simple access.

### Catalog Integration

The add-on includes catalog indexes and metadata columns:

- `event_date_override` - BooleanIndex
- `event_date_override_text` - FieldIndex

This allows efficient querying and display in event listings without loading full objects.

### Safe Indexers

Custom indexers ensure non-event content gets safe default values:

- Events without override: `False`, `None`
- Non-event content: `False`, `None`
- Events with override: `True`, `"Custom text"`

No errors, ever.

## Upgrade Notes

When upgrading from an existing site:

1. Install the add-on
2. Enable the behavior on Event type
3. Run the catalog upgrade step (Site Setup → Add-ons → collective.behavior.dateoverride → Upgrade)

The upgrade step adds the catalog indexes and reindexes all content.

## Development

Clone the repository:

```bash
git clone https://github.com/collective/collective.behavior.dateoverride.git
cd collective.behavior.dateoverride
```

Create a virtualenv and install:

```bash
python3 -m venv venv
./venv/bin/pip install -e ".[test]"
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for your changes
4. Submit a pull request

## License

GPL version 2

## Author

Your Name (your.email@example.com)

## Credits

This package was developed to solve a common need in Plone event management.
