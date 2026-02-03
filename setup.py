from setuptools import setup, find_packages

setup(
    name="joystick-teleoperation",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pygame",
    ],
    author="Ko-Br",
    description="Joystick teleoperation module",
    python_requires=">=3.12",
)
