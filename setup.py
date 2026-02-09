"""Installer for the collective.behavior.dateoverride package."""

from setuptools import find_packages, setup

long_description = '\n\n'.join([
    open('README.md').read(),
    open('CHANGES.md').read(),
])

setup(
    name='collective.behavior.dateoverride',
    version='1.0.0',
    description="Plone behavior to override event date display with custom text",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone CMS Event Date Override',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/collective/collective.behavior.dateoverride',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/collective.behavior.dateoverride',
        'Source': 'https://github.com/collective/collective.behavior.dateoverride',
        'Tracker': 'https://github.com/collective/collective.behavior.dateoverride/issues',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.behavior'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        'setuptools',
        'Plone',
        'plone.api',
        'plone.behavior',
        'plone.autoform',
        'plone.supermodel',
        'plone.indexer',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.testing',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
