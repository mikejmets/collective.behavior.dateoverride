# Client Site Integration Guide

## Overview

This guide shows how to integrate `collective.behavior.dateoverride` into your client's Plone site, specifically for use with `collective.isotope` event listings.

## Step 1: Add to Client Buildout

Edit your client's `buildout.cfg`:

```ini
[buildout]
extends = 
    https://dist.plone.org/release/6.0-latest/versions.cfg

eggs =
    Plone
    client.theme
    collective.isotope
    collective.behavior.dateoverride  # Add this line

[instance]
recipe = plone.recipe.zope2instance
eggs = ${buildout:eggs}
```

Run buildout:

```bash
bin/buildout
bin/instance restart
```

## Step 2: Install the Add-on

1. Access Plone: http://yoursite/@@overview-controlpanel
2. Go to "Add-ons"
3. Install "Event Date Override Behavior"

That's it! The behavior is automatically enabled on Events.

## Step 3: Customize Your Isotope Template

### Option A: Override via z3c.jbot (Recommended)

In your `client.theme` package:

```
client.theme/
├── src/
│   └── client/
│       └── theme/
│           └── browser/
│               └── overrides/
│                   └── collective.isotope.browser.templates.isotope.pt
```

**File: `collective.isotope.browser.templates.isotope.pt`**

```xml
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:tal="http://xml.zope.org/namespaces/tal"
      xmlns:metal="http://xml.zope.org/namespaces/metal"
      metal:use-macro="context/main_template/macros/master">

<body>
<metal:content-core fill-slot="content-core">
    <div id="isotopeContainer" class="isotope-container">
        
        <tal:items repeat="brain view/results">
            <div class="isotope-item"
                 tal:define="is_event python:brain.portal_type == 'Event'">
                
                <h3>
                    <a tal:attributes="href brain/getURL"
                       tal:content="brain/Title">Title</a>
                </h3>
                
                <!-- Event with date override support -->
                <tal:event condition="is_event">
                    <div class="event-date">
                        <!-- Use catalog metadata - fast! -->
                        <tal:override condition="brain/event_date_override">
                            <span class="date-override"
                                  tal:content="brain/event_date_override_text">
                                Coming Soon
                            </span>
                        </tal:override>
                        
                        <tal:normal condition="not:brain/event_date_override">
                            <span tal:content="python:brain.start.strftime('%B %d, %Y')">
                                Date
                            </span>
                        </tal:normal>
                    </div>
                </tal:event>
                
                <div class="description" tal:content="brain/Description">
                    Description
                </div>
                
            </div>
        </tal:items>
        
    </div>
</metal:content-core>
</body>
</html>
```

### Option B: Custom View Class

For more control, create a custom view:

**File: `client.theme/browser/views.py`**

```python
from collective.isotope.browser.view import IsotopeView


class CustomIsotopeView(IsotopeView):
    """Custom isotope view with date override support"""
    
    def format_event_date(self, brain):
        """Format event date, respecting override"""
        if brain.event_date_override:
            return brain.event_date_override_text
        return brain.start.strftime('%B %d, %Y')
```

**File: `client.theme/browser/configure.zcml`**

```xml
<browser:page
    name="custom-isotope-view"
    for="plone.app.contenttypes.interfaces.ICollection"
    class=".views.CustomIsotopeView"
    template="templates/custom_isotope.pt"
    permission="zope2.View"
    />
```

## Step 4: Add Custom Styling

**File: `client.theme/static/custom.css`**

```css
/* Override date styling */
.event-date {
    margin: 10px 0;
    padding: 8px 12px;
    background: #f5f5f5;
    border-left: 3px solid #007eb1;
}

.date-override {
    font-weight: bold;
    color: #d04437;
    font-style: italic;
}

.date-override::before {
    content: "📅 ";
}
```

## Step 5: Client Training

Create documentation for content editors:

### How to Override Event Dates

1. Edit your event
2. Scroll to the "Dates" fieldset
3. Check "Override Event Date Display"
4. Enter custom text, e.g.:
   - "Coming Soon"
   - "TBA"
   - "Spring 2025"
   - "Multiple dates - see details"
5. Save

The event will now display your custom text instead of the date.

**Note:** The actual start/end dates are still used for:
- Sorting in collections
- Calendar exports
- Event indexes

## Benefits for Your Client

### No Custom Development Needed
- No Python code in client package (just templates)
- Behavior is maintained as a separate add-on
- Easy updates via buildout

### Performance
- Uses catalog metadata (no getObject() calls)
- Fast event listings even with hundreds of events

### Flexibility
- Content editors control override per event
- Works with existing Collections
- Compatible with isotope filtering/sorting

### Maintainable
- Clear separation of concerns
- Add-on can be updated independently
- Can be used on multiple client sites

## Example Client Package Structure

```
client.theme/
├── setup.py
├── buildout.cfg  (includes collective.behavior.dateoverride)
└── src/
    └── client/
        └── theme/
            ├── browser/
            │   ├── configure.zcml
            │   ├── overrides/
            │   │   └── collective.isotope.browser.templates.isotope.pt
            │   └── static/
            │       └── custom.css
            └── profiles/
                └── default/
                    └── registry.xml
```

## Testing the Integration

1. Create test events:
   - Event A: Normal date display
   - Event B: Override with "Coming Soon"
   - Event C: Override with "TBA"

2. Create a Collection:
   - Type = Event
   - Sort by Start Date

3. View with isotope:
   - Should show mixed date displays
   - Override text should be styled differently
   - Sorting should use actual dates

## Troubleshooting

### "Fields not appearing in edit form"

Check that the behavior is enabled:
```
Site Setup → Dexterity Content Types → Event → Behaviors
✓ Event Date Override
```

### "Override not showing in isotope view"

Verify catalog has metadata:
```python
from plone import api
catalog = api.portal.get_tool('portal_catalog')
print(catalog.schema())  # Should include 'event_date_override'
```

### "Performance issues"

Make sure you're using brain metadata, not getObject():
```xml
<!-- Good -->
<span tal:content="brain/event_date_override_text">

<!-- Bad - don't do this -->
<tal:define define="obj brain/getObject">
```

## Deployment Checklist

- [ ] Add to buildout.cfg
- [ ] Run bin/buildout
- [ ] Restart instance
- [ ] Install add-on via UI
- [ ] Test event creation
- [ ] Override isotope template
- [ ] Add custom CSS
- [ ] Test with real content
- [ ] Document for editors
- [ ] Deploy to production
