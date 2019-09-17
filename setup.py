from setuptools import setup, find_packages


setup(
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    use_scm_version=True,
    install_requires=[
        'ffmpeg-python',
    ],
    setup_requires=[
        'setuptools_scm',
    ],
    extras_require={
        # 'full':  [
        #    'wmc-resize',
        #    'lying',
        #    'blurring',
        # ],
    },
    entry_points={
        'wmc.register_cls': [
            'setup=wmc.commands:Setup',
            'info=wmc.commands:Info',
            'record=wmc.commands:Record',
            'link=wmc.commands:Link',
        ],
        'console_scripts': [
            'wmc=wmc.cli:main',
        ],
    },
)
