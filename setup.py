from setuptools import setup

packages = ['mainflux']

requires = [
    'httpx==0.11.1',
    'hbmqtt==0.9.5'
]

setup(
    name="mainfluxpy",
    version='0.0.1',
    packages=packages,
    install_requires=requires,
    python_requires='>=3.6.1'
)
