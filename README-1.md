## RepoToTextForLLMs - Analyzing Repositories for Large Language Models

**Automates the analysis of GitHub repositories or local directories, specifically tailored for large language models (LLMs).**

This Python script efficiently fetches content useful for LLMs, including:

-   **README retrieval:** Extracts the content of the `README.md` file for initial insights.
-   **Structured repository traversal:** Maps out the repository's structure for understanding its organization.
-   **Selective content extraction:** Retrieves text contents from non-binary files, streamlining analysis for LLMs.
-   **Local repository support:** Analyzes local directories in addition to GitHub repositories.

**Key Features:**

-   **Configuration options:** Customize the analysis process through configuration files:
    -   **Analysis prompts:** Modify or create prompts in `instructions-prompt.txt` to guide LLM analysis.
    -   **Binary file extensions:** Specify additional binary file types to exclude in `repototxt.py`.

**How to Use:**

**1. Converting a GitHub Repository to Text**

-   Execute the script in your terminal:

```bash
python repototxt.py
```

-   Enter the GitHub repository URL when prompted.

**2. Converting a Local Directory to Text**

-   Provide the directory path as a command-line argument:

```bash
python repototxt.py /path/to/local/directory
```

**Output:**

The script processes the repository or local directory and outputs a text file named `${repo_name}-text.txt` (configurable) containing:

-   Analysis instructions (from `instructions-prompt.txt`)
-   README content
-   Repository structure
-   Content of non-binary files

**Control Output:**

-   **Clipboard:** Set the `ENABLE_CLIPBOARD` environment variable to `1` to copy the analyzed content to the clipboard.
-   **File:** Set the `ENABLE_SAVE_TO_FILE` environment variable to `1` (default) to save the analyzed content to a file.

**Getting Started:**

1. Ensure Python and required packages (`PyGithub`, `tqdm`, `python-dotenv`, `pyperclip`) are installed:

```bash
pip install -r requirements.txt
```

2. (Optional) Set your GitHub Personal Access Token as an environment variable (`GITHUB_TOKEN`) for analyzing GitHub repositories.

**Contributing:**

Contributions are welcome! Submit pull requests, report issues, or suggest improvements.

**License:**

This project is licensed under the MIT License.
