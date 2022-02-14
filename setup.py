from setuptools import setup, find_packages

DESCRIPTION = "piro is software designed to assist in planning of synthesis pathways for inorganics"

LONG_DESCRIPTION = """
The piro software package enables prediction and planning of synthesis pathways
and determination of pareto-optimal frontiers for synthesis of
specific inorganic materials.
"""

setup(
    name="piro",
    version="2021.10.6-post0",
    packages=find_packages(),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    install_requires=["matminer==0.7.4",
                      "scikit-learn==1.0.2",
                      "plotly==5.5.0",
                      "pymongo==4.0.1",
                      "pydantic==1.9.0"
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
    package_data={
        "piro": ["*.pickle", "*.json"]
    },
    include_package_data=True,
    author="AMDD - Toyota Research Institute",
    author_email="murat.aykol@tri.global",
    maintainer="Joseph Montoya",
    maintainer_email="joseph.montoya@tri.global",
    # license="Apache",
    keywords=[
        "materials", "battery", "chemistry", "science",
        "density functional theory", "energy", "AI", "artificial intelligence",
        "sequential learning", "active learning"
    ],
    )
