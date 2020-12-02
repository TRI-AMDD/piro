from setuptools import setup, find_packages
import warnings

DESCRIPTION = "rxn is software designed to assist in prediction of synthesis pathway"

LONG_DESCRIPTION = """
The rxn software package enables prediction of synthesis pathways
and determination of pareto-optimal frontiers for synthesis of
specific materials
"""

setup(
    name="rxn",
    version="2020.12.2",
    packages=find_packages(),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    install_requires=["matminer==0.6.3",
                      "scikit-learn==0.23.1",
                      "plotly==4.8.2"
                      ],
    classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: Apache Software License",
          "Operating System :: OS Independent",
    ],
    include_package_data=True,
    author="AMDD - Toyota Research Institute",
    author_email="murat.aykol@tri.global",
    maintainer="Murat Aykol",
    maintainer_email="murat.aykol@tri.global",
    # license="Apache",
    keywords=[
        "materials", "battery", "chemistry", "science",
        "density functional theory", "energy", "AI", "artificial intelligence",
        "sequential learning", "active learning"
    ],
    )
