from setuptools import setup, find_packages
import warnings

DESCRIPTION = "piro is software designed to assist in planning of synthesis pathways for inorganics"

LONG_DESCRIPTION = """
The piro software package enables prediction and planning of synthesis pathways
and determination of pareto-optimal frontiers for synthesis of
specific inorganic materials.
"""

setup(
    name="piro",
    version="2020.12.2",
    packages=find_packages(),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    install_requires=["matminer==0.6.4",
                      "scikit-learn==0.23.2",
                      "plotly==4.13.0",
                      "pymatgen"
                      ],
    classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: Apache Software License",
          "Operating System :: OS Independent",
    ],
    extras_require={
        "web": ["dash-core-components>=0.22.1",
                "dash-html-components>=0.10.1",
                "dash-renderer>=0.12.1",
                "dash-table==4.11.0",
                "dash==1.17.0"
                ]
    },
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
