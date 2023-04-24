from setuptools import setup, find_packages

DESCRIPTION = "piro is software designed to assist in planning of synthesis pathways for inorganics"

LONG_DESCRIPTION = """
The piro software package enables prediction and planning of synthesis pathways
and determination of pareto-optimal frontiers for synthesis of
specific inorganic materials.
"""

setup(
    name="piro",
    version="2023.4.24",
    packages=find_packages(),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    install_requires=["matminer==0.8.0",
                      "plotly==5.11.0",
                      "pymongo==3.12.0",
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
                  ],
        "m3gnet": ["m3gnet==0.2.4"]
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
