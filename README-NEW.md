# RepoToTextForLLMs

Automates the analysis of GitHub repositories or local directories, specifically tailored for usage with large context LLMs. This Python script efficiently fetches README files, repository structure, and non-binary file contents. Additionally, it provides structured outputs complete with pre-formatted prompts to guide further analysis of the repository's content.

## Features

-   **README Retrieval:** Automatically extracts the content of README.md to provide an initial insight into the repository.
-   **Structured Repository Traversal:** Maps out the repository's structure through an iterative traversal method, ensuring thorough coverage without the limitations of recursion.
-   **Selective Content Extraction:** Retrieves text contents from files, intelligently skipping over binary files and the `.git` folder (for local repositories) to streamline the analysis process.
-   **Local Repository Support:** Analyzes local directories in addition to GitHub repositories.
-   **Comprehensive Binary File Detection:** Utilizes an extensive list of binary file extensions to accurately identify and exclude binary files from the analysis.

## Prerequisites

To use **RepoToTextForLLMs**, you'll need:

-   Python installed on your system.
-   The following Python packages: `PyGithub`, `tqdm`, and `python-dotenv`.
-   A GitHub Personal Access Token configured as an environment variable (`GITHUB_TOKEN`) if analyzing GitHub repositories.

## Getting Started

1. Ensure Python and the required packages are installed:

```bash
pip install PyGithub tqdm python-dotenv
```

2. Set your GitHub Personal Access Token as an environment variable (if analyzing GitHub repositories):

```bash
export GITHUB_TOKEN=YOUR_GITHUB_TOKEN
```

or create a `.env` file in the same directory with the following content:

```
GITHUB_TOKEN=YOUR_GITHUB_TOKEN
```

## How to Use

1. Place the script in your desired directory.
2. Execute the script in your terminal:

```bash
python repototxt.py
```

3. For GitHub repositories, enter the repository URL when prompted. For local directories, provide the directory path as a command-line argument:

```bash
python repototxt.py /path/to/local/directory
```

The script will process the repository or local directory and output its findings, including the README, structure, and file contents (excluding binary files and the `.git` folder for local repositories), accompanied by analysis prompts.

## Contributing

Contributions to **RepoToTextForLLMs** are welcomed. Whether it's through submitting pull requests, reporting issues, or suggesting improvements, your input helps make this tool better for everyone.

## License

This project is licensed under the MIT License.
