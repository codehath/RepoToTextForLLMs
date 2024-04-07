# RepoToTextForLLMs

Automates the analysis of GitHub repositories or local directories, specifically tailored for usage with large context LLMs. This Python script efficiently fetches README files, repository structure, and non-binary file contents. Additionally, it provides structured outputs complete with pre-formatted prompts to guide further analysis of the repository's content.

## Features

-   **README Retrieval:** Automatically extracts the content of README.md to provide an initial insight into the repository.
-   **Structured Repository Traversal:** Maps out the repository's structure through an iterative traversal method, ensuring thorough coverage without the limitations of recursion.
-   **Selective Content Extraction:** Retrieves text contents from files, intelligently skipping over binary files to streamline the analysis process.
-   **Local Repository Support:** Analyzes local directories in addition to GitHub repositories.

## Prerequisites

To use **RepoToTextForLLMs**, you'll need:

-   Python installed on your system.
-   A GitHub Personal Access Token configured as an environment variable (`GITHUB_TOKEN`) if converting GitHub repositories.

## Getting Started

1. Ensure Python and the required packages are installed:

```bash
pip install PyGithub tqdm python-dotenv
```

2. Set your GitHub Personal Access Token as an environment variable (if converting GitHub repositories). Rename sample.env to .env and replace 'your_github_token' with your GitHub Personal Access Token. [How to Generate a Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic)

```
GITHUB_TOKEN=YOUR_GITHUB_TOKEN
```

## How to Use

### To convert GitHub repo to text:

1. Execute the script in your terminal:

```bash
python repototxt.py
```

2. Enter the GitHub repository URL when prompted. The script will process the repository and output its findings, including the README, structure, and file contents (excluding binary files), accompanied by analysis prompts.

### To convert local repo to text:

1. For local directories, provide the directory path as a command-line argument when calling the script:

```bash
python repototxt.py /path/to/local/directory
```

The script will process the repository or local directory and output it as a text file into the same folder as repototext.py, including the README, structure, and file contents (excluding binary files and the `.git` folder for local repositories), accompanied by analysis prompts.

## Configuration

The script provides several configuration options to customize its behavior and tailor it to your specific needs.

### Analysis Prompt

The analysis prompt used to guide the further examination of the repository's content is stored in the instructions-prompt.txt file. You can modify or remove this prompt by editing the contents of this file according to your preferences.

### Binary File Extensions

The script uses an extensive list of binary file extensions to identify and exclude binary files from the analysis process. If you need to include additional binary file types specific to your use case, you can add their extensions to the binary_extensions list in the repototxt.py file.

For example, to include .bin and .exe files as binary files, you can modify the binary_extensions list as follows:

```python
binary_extensions = [
    # ...
    # Additional binary extensions
    ".bin",
    ".exe",
    # ...
]
```

By providing these configuration options, the script allows you to fine-tune the analysis process and tailor it to your specific requirements, ensuring that the output aligns with your desired format and content.

## Contributing

Contributions to **RepoToTextForLLMs** are welcomed. Whether it's through submitting pull requests, reporting issues, or suggesting improvements, your input helps make this tool better for everyone.

## License

This project is licensed under the MIT License.
