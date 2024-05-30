from setuptools import setup, find_packages

setup(
    name="Foxy",
    version="0.1.0",
    author="Josselin LE TALLEC",
    author_email="josselin.letallec@proton.me",
    description="A set of rules designed to optimize performance and improve privacy in Firefox. Always up to date!",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/J0ssel1n/Foxy",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'foxy=Foxy.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)