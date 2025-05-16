from setuptools import find_packages, setup

inst_reqs = [
    "boto3",
    "pydantic-settings",
    "aws-cdk-lib==2.196.0"
]

extra_reqs = {
    "test": ["pytest", "pytest-cov", "black", "flake8"],
    "dev": [
        "pytest",
        "black",
        "flake8",
        "nodeenv",
        "isort",
        "pre-commit",
        "pre-commit-hooks",
    ],
}

setup(
    name="edl-credential-rotation",
    version="0.0.1",
    python_requires=">=3.8",
    author="development seed",
    packages=find_packages(),
    package_data={
        ".": [
            "cdk.json",
        ],
    },
    install_requires=inst_reqs,
    extras_require=extra_reqs,
    include_package_data=True,
)
