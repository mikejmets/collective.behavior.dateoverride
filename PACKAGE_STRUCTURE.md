# collective.behavior.dateoverride Package Structure

## Complete Package Overview

```
collective.behavior.dateoverride/
├── setup.py                          # Package metadata and dependencies
├── MANIFEST.in                       # Include non-Python files in package
├── README.md                         # Main documentation
├── CHANGES.md                        # Version history
├── INSTALL.md                        # Installation instructions
├── CLIENT_INTEGRATION.md             # Guide for client site integration
├── .gitignore                        # Git ignore rules
│
└── src/
    └── collective/
        ├── __init__.py               # Namespace package
        └── behavior/
            ├── __init__.py           # Namespace package
            └── dateoverride/
                ├── __init__.py       # Package initialization
                ├── configure.zcml    # Main ZCML configuration
                ├── upgrades.py       # Upgrade step handlers
                ├── upgrades.zcml     # Upgrade step registration
                │
                ├── behaviors/
                │   ├── __init__.py
                │   ├── configure.zcml         # Behavior registration
                │   ├── dateoverride.py        # Behavior interface/fields
                │   └── indexers.py            # Catalog indexers
                │
                ├── browser/
                │   ├── __init__.py
                │   └── configure.zcml         # Browser views (optional)
                │
                └── profiles/
                    └── default/
                        ├── metadata.xml       # Profile version
                        ├── catalog.xml        # Catalog indexes/columns
                        └── types/
                            └── Event.xml      # Enable behavior on Event
```

## File Purposes

### Root Level

**setup.py**
- Defines package metadata (name, version, author)
- Lists dependencies (Plone, plone.behavior, etc.)
- Entry point for pip/buildout installation

**MANIFEST.in**
- Ensures non-Python files are included in distribution
- Templates, XML, images, etc.

**README.md**
- Main documentation
- Features, usage examples
- For PyPI and GitHub

**CHANGES.md**
- Version history
- What changed in each release

**INSTALL.md**
- Step-by-step installation guide
- Troubleshooting

**CLIENT_INTEGRATION.md**
- How to use in client sites
- Template customization examples
- Integration with collective.isotope

### Core Package (src/collective/behavior/dateoverride/)

**__init__.py**
- Package initialization
- `initialize()` function for Zope 2 products

**configure.zcml**
- Main ZCML configuration
- Includes sub-packages
- Registers GenericSetup profile

**upgrades.py**
- Python code for upgrade steps
- Adds catalog indexes

**upgrades.zcml**
- Registers upgrade steps with GenericSetup

### Behaviors (behaviors/)

**dateoverride.py**
- `IEventDateOverride` interface
- Field definitions (event_date_override, event_date_override_text)
- Plone form schema

**indexers.py**
- Catalog indexers for both fields
- Safe for objects without behavior (returns defaults)

**configure.zcml**
- Registers the behavior with plone.behavior
- Registers indexer adapters

### Browser (browser/)

**configure.zcml**
- Placeholder for browser views
- Can add custom views later if needed

### GenericSetup Profile (profiles/default/)

**metadata.xml**
- Profile version number
- Dependencies (plone.app.dexterity)

**catalog.xml**
- Adds indexes to portal_catalog
- Adds metadata columns
- Installed when profile is applied

**types/Event.xml**
- Modifies Event content type
- Enables the behavior automatically
- `purge="false"` to preserve other behaviors

## Key Design Decisions

### Why DexteritySchemaPolicy?
- Simple direct attribute access in templates
- Behavior is permanent on Event type
- Better for client site customization

### Why Catalog Metadata?
- Fast queries (no getObject() needed)
- Works with Collections and listings
- Essential for isotope performance

### Why Safe Indexers?
- Non-event content gets False/None
- No errors in mixed collections
- Works before reindexing

### Why Separate Add-on?
- Reusable across projects
- Clean separation from client code
- Independent updates/versioning
- Can be shared with community

## Installation Flow

1. **Buildout adds to eggs** → Package downloaded
2. **Instance starts** → ZCML loaded, behavior registered
3. **Profile installed** → Catalog indexes added, behavior enabled on Event
4. **Upgrade step runs** → Existing content reindexed

## Usage Flow

1. **Content editor** → Checks override box, enters text
2. **Event saved** → Fields stored as attributes
3. **Event indexed** → Indexers add to catalog
4. **Collection query** → Returns brains with metadata
5. **Template renders** → Uses brain.event_date_override_text

## Development Workflow

```bash
# Initial setup
git clone <repo>
cd collective.behavior.dateoverride
python3 -m venv venv
./venv/bin/pip install -e ".[test]"

# Make changes
# Edit files in src/collective/behavior/dateoverride/

# Test locally
# Add to a Plone buildout
# Install and test

# Release
# Update version in setup.py
# Update CHANGES.md
# git tag v1.0.0
# python setup.py sdist bdist_wheel
# twine upload dist/*
```

## Integration with Client Site

```
client.site/
├── buildout.cfg
│   eggs = collective.behavior.dateoverride  # Add this
│
└── src/client/theme/
    └── browser/
        └── overrides/
            └── collective.isotope.browser.templates.isotope.pt
                # Use brain.event_date_override here
```

Client site only needs:
1. Add egg to buildout
2. Override isotope template
3. Use the fields

No custom Python code needed in client site!

## Maintenance

### Updating the Add-on
1. Make changes in separate package
2. Increment version in setup.py
3. Update CHANGES.md
4. Release to PyPI or private repo

### Updating Client Sites
1. Update version pin in buildout
2. Run buildout
3. Restart
4. Run upgrade steps if needed

## Future Enhancements

Possible additions:
- [ ] Translation files (i18n)
- [ ] Additional validators
- [ ] Custom vocabularies for common override texts
- [ ] RestAPI serializer
- [ ] Plone 6.1 support
- [ ] More tests

## Questions?

See:
- README.md - General usage
- INSTALL.md - Installation
- CLIENT_INTEGRATION.md - Using in client sites
