from setuptools import setup, find_packages


setup(
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    use_scm_version=True,
    install_requires=[
        'ffmpeg-python',
        'pywin32 ; platform_system=="Windows"',
        'Xlib ; platform_system=="Linux"'
    ],
    setup_requires=[
        'setuptools_scm',
    ],
    entry_points={
        'wmc.register_setup': [
            'basic=wmc.basic:setup',
        ],
        'wmc.register_command': [
            'info=wmc.basic:info',
            'record=wmc.basic:record',
            'link=wmc.basic:link',
        ],
        'console_scripts': [
            'wmc=wmc.cli:main',
        ],

    },
)
