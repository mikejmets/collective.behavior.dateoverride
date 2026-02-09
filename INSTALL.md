# Installation Guide for collective.behavior.dateoverride

## Quick Start

### 1. Add to buildout.cfg

```ini
[buildout]
eggs =
    collective.behavior.dateoverride

[instance]
eggs =
    ${buildout:eggs}
```

### 2. Run buildout

```bash
bin/buildout
bin/instance restart
```

### 3. Install via Plone UI

1. Go to Site Setup (http://yoursite/@@overview-controlpanel)
2. Click "Add-ons"
3. Find "Event Date Override Behavior"
4. Click "Install"

Done! The behavior is automatically enabled on the Event content type.

## What Gets Installed

### Catalog Indexes
- `event_date_override` (BooleanIndex)
- `event_date_override_text` (FieldIndex)

### Metadata Columns
- `event_date_override`
- `event_date_override_text`

### Behavior
- Automatically enabled on Event content type
- Fields appear in the "Dates" fieldset

## Post-Installation

### For Existing Sites

If you have existing events, they'll automatically get indexed with default values:
- `event_date_override = False`
- `event_date_override_text = None`

No manual reindexing needed!

### Verify Installation

Create a test event:
1. Go to any folder
2. Add → Event
3. Fill in basic details
4. Look for "Dates" fieldset
5. You should see:
   - "Override Event Date Display" checkbox
   - "Event Date Override Text" field

## Using in Templates

### Client Site Customization

In your client site's package (e.g., `client.theme`), you can now customize event display:

```xml
<!-- In your event view template -->
<tal:override condition="context/event_date_override">
    <span class="date-override" 
          tal:content="context/event_date_override_text">
        Coming Soon
    </span>
</tal:override>

<tal:normal condition="not:context/event_date_override">
    <span tal:content="python:context.start.strftime('%B %d, %Y')">
        January 15, 2025
    </span>
</tal:normal>
```

### In Collection/Isotope Views

```xml
<!-- Using catalog metadata - no getObject() needed -->
<tal:items repeat="brain view/results">
    <tal:override condition="brain/event_date_override">
        <span tal:content="brain/event_date_override_text">TBA</span>
    </tal:override>
    <tal:normal condition="not:brain/event_date_override">
        <span tal:content="python:brain.start.strftime('%B %d, %Y')">Date</span>
    </tal:normal>
</tal:items>
```

## Development Installation

For development/testing:

```bash
git clone https://github.com/collective/collective.behavior.dateoverride.git
cd collective.behavior.dateoverride
python3 -m venv venv
./venv/bin/pip install -e ".[test]"
```

## Uninstallation

1. Go to Site Setup → Add-ons
2. Find "Event Date Override Behavior"
3. Click "Uninstall"

Note: This removes the catalog indexes but doesn't delete existing override data from events (it's preserved in case you reinstall).

## Troubleshooting

### Fields Not Showing

1. Verify the behavior is enabled:
   - Site Setup → Dexterity Content Types → Event → Behaviors tab
   - "Event Date Override" should be checked

2. Clear your browser cache

### Catalog Not Working

Run the upgrade step:
1. Site Setup → Add-ons
2. Find "Event Date Override Behavior"
3. Click "Upgrade" if available

Or manually in Python:

```python
from plone import api
catalog = api.portal.get_tool('portal_catalog')
catalog.manage_reindexIndex(ids=['event_date_override', 'event_date_override_text'])
```

### Template Errors

Make sure you're accessing the fields correctly:

```python
# Direct access (behavior enabled on type)
context.event_date_override

# Catalog brain access
brain.event_date_override
brain.event_date_override_text

# Safe check if behavior might not be enabled
getattr(context, 'event_date_override', False)
```
