## RepoToTextForLLMs

**Automates the analysis of GitHub repositories or local directories, specifically tailored for usage with large context LLMs.** This Python script efficiently fetches README files, repository structure, and non-binary file contents. Additionally, it provides structured outputs complete with pre-formatted prompts to guide further analysis of the repository's content.

**Features**

-   **README Retrieval:** Automatically extracts the content of README.md to provide an initial insight into the repository.
-   **Structured Repository Traversal:** Maps out the repository's structure through an iterative traversal method, ensuring thorough coverage without the limitations of recursion.
-   **Selective Content Extraction:** Retrieves text contents from files, intelligently skipping over binary files to streamline the analysis process.
-   **Local Repository Support:** Analyzes local directories in addition to GitHub repositories.

**Configuration**

The script provides several configuration options to customize its behavior and tailor it to your specific needs.

-   **Analysis Prompt:** The analysis prompt used to guide the further examination of the repository's content is stored in the instructions-prompt.txt file. You can modify or remove this prompt by editing the contents of this file according to your preferences.

-   **Binary File Extensions:** The script uses an extensive list of binary file extensions to identify and exclude binary files from the analysis process. If you need to include additional binary file types specific to your use case, you can add their extensions to the binary_extensions list in the repototxt.py file.

**Contributing**

Contributions to RepoToTextForLLMs are welcomed. Whether it's through submitting pull requests, reporting issues, or suggesting improvements, your input helps make this tool better for everyone.

**License**

This project is licensed under the MIT License.
