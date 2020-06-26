# -*- coding: utf-8 -*-
"""Installer for the uwosh.oie.studyabroadstudent package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='uwosh.oie.studyabroadstudent',
    version='1.0a1',
    description='Dexterity content type for study abroad programs and student '
                'applications for the University of Wisconsin Oshkosh Office '
                'of International Education',
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    ],
    keywords='Python Plone workflow study abroad',
    author='T. Kim Nguyen',
    author_email='kim.nguyen@wildcardcorp.com',
    url='https://github.com/uwosh/uwosh.oie.studyabroadstudent',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['uwosh', 'uwosh.oie'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'Products.GenericSetup>=1.8.2',
        'setuptools',
        'z3c.jbot',
        'plone.app.dexterity',
        'currencies',
        'collective.dexteritytextindexer',
        'collective.z3cform.datagridfield',
        'plone.app.workflowmanager',
        'collective.impersonate',
        'collective.easyform',
        'Products.ContentWellPortlets',
        'webcouturier.dropdownmenu',
        'plone.app.iterate',
        'uwosh.oie.studyabroadtheme',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
