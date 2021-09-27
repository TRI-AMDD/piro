from setuptools import setup, find_packages

DESCRIPTION = "piro is software designed to assist in planning of synthesis pathways for inorganics"

LONG_DESCRIPTION = """
The piro software package enables prediction and planning of synthesis pathways
and determination of pareto-optimal frontiers for synthesis of
specific inorganic materials.
"""

setup(
    name="piro",
    version="2021.6.24",
    packages=find_packages(),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    install_requires=["matminer==0.7.4",
                      "scikit-learn==1.0",
                      "plotly==5.2.1",
                      "pymongo==3.12.0",
                      "pydantic==1.8.2"
                      ],
    classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: Apache Software License",
          "Operating System :: OS Independent",
    ],
    extras_require={
        "tests": ["pytest",
                  "pytest-cov",
                  "coveralls"
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
