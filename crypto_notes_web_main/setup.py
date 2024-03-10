from setuptools import setup, find_packages

setup(
    name='crypto_notes_app',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyramid',
        'waitress',
    ],
    entry_points={
        'paste.app_factory': [
            'main = crypto_notes_app:main',
        ],
    },
)
