from setuptools import find_packages, setup

# 5.0.4 is the latest version of flake8 that works with python 3.6
flake8 = "flake8==5.0.4"

setup(
    name="hls_mask_jp2_to_envi",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer==0.7.0",
        "rasterio==1.2.10",
    ],
    extras_require={
        "dev": [flake8, "black==22.8.0", "isort==5.10.1"],
        "test": [flake8, "pytest==7.0.1"],
    },
    entry_points={
        "console_scripts": [
            "mask_jp2_to_envi=hls_mask_jp2_to_envi.main:app",
        ]
    },
)
