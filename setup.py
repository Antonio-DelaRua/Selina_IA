from setuptools import setup, find_packages

setup(
    name="selina_ia",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "langchain_ollama",
        "pygame",
        "pillow",
        "pyttsx3",
        "pywhatkit",
        "wikipedia",
        "keyboard",
        "opencv-python",
        "numpy",
        "speechrecognition"
    ],
    entry_points={
        'console_scripts': [
            'selina=src.main:main',
        ],
    },
    python_requires=">=3.10",
)