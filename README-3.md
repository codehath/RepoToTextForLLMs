## RepoToTextForLLMs - Analyze GitHub Repositories and Local Directories for Large Language Models

This Python script automates the analysis of GitHub repositories or local directories, specifically tailored for use with large context Large Language Models (LLMs). It efficiently extracts and formats content to streamline further analysis by LLMs.

**Key Features:**

-   **README Retrieval:** Fetches the content of the `README.md` file to provide an initial understanding of the repository.
-   **Structured Repository Traversal:** Maps out the repository's structure using an iterative traversal method to ensure comprehensive coverage.
-   **Selective Content Extraction:** Retrieves text contents from non-binary files, intelligently skipping over binary files for efficient analysis.
-   **Local Repository Support:** Analyzes local directories in addition to GitHub repositories.

**How to Use:**

**1. Prerequisites:**

-   Python installed on your system.
-   A GitHub Personal Access Token configured as an environment variable (`GITHUB_TOKEN`) if converting GitHub repositories. ([https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens))

**2. Installation:**

```bash
pip install -r requirements.txt
```

**3. Configuration (Optional):**

The script provides several configuration options to customize its behavior and tailor it to your specific needs. These configurations are located in the following files:

-   `instructions-prompt.txt`: This file contains the analysis prompt used to guide the further examination of the repository's content. You can modify or remove this prompt by editing the contents of this file according to your preferences.
-   `binary_extensions`: The script uses an extensive list of binary file extensions to identify and exclude binary files from the analysis process. If you need to include additional binary file types specific to your use case, you can add their extensions to the `binary_extensions` list in the `repototxt.py` file.

**4. Usage:**

**a) To convert a GitHub repository to text:**

1. Execute the script in your terminal:

```bash
python repototxt.py
```

2. Enter the GitHub repository URL when prompted.

**b) To convert a local directory to text:**

1. Provide the directory path as a command-line argument when calling the script:

```bash
python repototxt.py /path/to/local/directory
```

**Output:**

The script processes the repository or local directory and outputs its findings, including:

-   The README content (if available)
-   The repository structure (directory and file hierarchy)
-   The text contents of non-binary files, accompanied by analysis prompts in the format specified by `instructions-prompt.txt`

By default, the script copies the extracted content to your clipboard or saves it to a file named `"{repository_name}-text.txt"` in the directory specified by the `OUTPUT_DIR` environment variable (defaults to the current working directory). You can control this behavior by setting the `ENABLE_CLIPBOARD` and `ENABLE_SAVE_TO_FILE` environment variables.

**Contributing:**

Contributions to **RepoToTextForLLMs** are welcome! Whether it's through submitting pull requests, reporting issues, or suggesting improvements, your input helps make this tool better for everyone.

**License:**

This project is licensed under the MIT License.
