from setuptools import setup, find_packages

setup(
    name='jigsaw-puzzle-game',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'customtkinter',
        'Pillow',
        'sqlite3',
    ],
    entry_points={
        'console_scripts': [
            'jigsaw-puzzle-game=main:main',
        ],
    },
    include_package_data=True,
    description='An interactive jigsaw puzzle game with scoring, hints, and high score tracking.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/jigsaw-puzzle-game',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)