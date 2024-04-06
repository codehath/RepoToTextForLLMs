import os
from github import Github
from tqdm import tqdm
from dotenv import load_dotenv
import json

load_dotenv()  # Load variables from .env file

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
binary_extensions = [
    # Compiled executables and libraries
    ".exe",
    ".dll",
    ".so",
    ".a",
    ".lib",
    ".dylib",
    ".o",
    ".obj",
    # Compressed archives
    ".zip",
    ".tar",
    ".tar.gz",
    ".tgz",
    ".rar",
    ".7z",
    ".bz2",
    ".gz",
    ".xz",
    ".z",
    ".lz",
    ".lzma",
    ".lzo",
    ".rz",
    ".sz",
    ".dz",
    # Application-specific files
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".odt",
    ".ods",
    ".odp",
    # Media files (less common)
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".mp3",
    ".mp4",
    ".wav",
    ".flac",
    ".ogg",
    ".avi",
    ".mkv",
    ".mov",
    ".webm",
    ".wmv",
    ".m4a",
    ".aac",
    # Virtual machine and container images
    ".iso",
    ".vmdk",
    ".qcow2",
    ".vdi",
    ".vhd",
    ".vhdx",
    ".ova",
    ".ovf",
    # Database files
    ".db",
    ".sqlite",
    ".mdb",
    ".accdb",
    ".frm",
    ".ibd",
    ".dbf",
    # Java-related files
    ".jar",
    ".class",
    ".war",
    ".ear",
    ".jpi",
    # Python bytecode and packages
    ".pyc",
    ".pyo",
    ".pyd",
    ".egg",
    ".whl",
    # Other potentially important extensions
    ".deb",
    ".rpm",
    ".apk",
    ".msi",
    ".dmg",
    ".pkg",
    ".bin",
    ".dat",
    ".data",
    ".dump",
    ".img",
    ".toast",
    ".vcd",
    ".crx",
    ".xpi",
    ".lockb",
    "package-lock.json",
    ".svg",
    ".eot",
    ".otf",
    ".ttf",
    ".woff",
    ".woff2",
    ".ico",
    ".icns",
    ".cur",
    ".cab",
    ".dmp",
    ".msp",
    ".msm",
    ".keystore",
    ".jks",
    ".truststore",
    ".cer",
    ".crt",
    ".der",
    ".p7b",
    ".p7c",
    ".p12",
    ".pfx",
    ".pem",
    ".csr",
    ".key",
    ".pub",
    ".sig",
    ".pgp",
    ".gpg",
    ".nupkg",
    ".snupkg",
    ".appx",
    ".msix",
    ".msp",
    ".msu",
    ".deb",
    ".rpm",
    ".snap",
    ".flatpak",
    ".appimage",
    ".ko",
    ".sys",
    ".elf",
    ".swf",
    ".fla",
    ".swc",
    ".rlib",
    ".pdb",
    ".idb",
    ".pdb",
    ".dbg",
    ".sdf",
    ".bak",
    ".tmp",
    ".temp",
    ".log",
    ".tlog",
    ".ilk",
    ".bpl",
    ".dcu",
    ".dcp",
    ".dcpil",
    ".drc",
    ".aps",
    ".res",
    ".rsrc",
    ".rc",
    ".resx",
    ".prefs",
    ".properties",
    ".ini",
    ".cfg",
    ".config",
    ".conf",
    ".DS_Store",
    ".localized",
    ".svn",
    ".git",
    ".gitignore",
    ".gitkeep",
]


def get_readme_content(repo):
    """
    Retrieve the content of the README file.
    """
    try:
        readme = repo.get_contents("README.md")
        return readme.decoded_content.decode("utf-8")
    except:
        return "README not found."


## Local
def get_local_readme_content(directory_path):
    """
    Retrieve the content of the README file in a local directory.
    """
    readme_path = os.path.join(directory_path, "README.md")
    if os.path.exists(readme_path):
        try:
            with open(readme_path, "r", encoding="utf-8") as readme_file:
                return readme_file.read()
        except Exception as e:
            return f"Error reading README file: {e}"
    else:
        return "README not found."


def traverse_repo_iteratively(repo):
    """
    Traverse the repository iteratively to avoid recursion limits for large repositories.
    """
    structure = ""
    dirs_to_visit = [("", repo.get_contents(""))]
    dirs_visited = set()

    while dirs_to_visit:
        path, contents = dirs_to_visit.pop()
        dirs_visited.add(path)
        for content in tqdm(contents, desc=f"Processing {path}", leave=False):
            if content.type == "dir":
                if content.path not in dirs_visited:
                    structure += f"{path}/{content.name}/\n"
                    dirs_to_visit.append(
                        (f"{path}/{content.name}", repo.get_contents(content.path))
                    )
            else:
                structure += f"{path}/{content.name}\n"
    return structure


def get_file_contents(path, binary_extensions):
    file_contents = ""
    for root, _, files in os.walk(path):
        for name in files:
            if not is_binary(name):
                file_path = os.path.join(root, name)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                    file_contents += f"File: /{os.path.relpath(file_path, path)}\nContent:\n{content}\n\n"
                except UnicodeDecodeError:
                    file_contents += f"File: /{os.path.relpath(file_path, path)}\nContent: Skipped due to encoding issue\n\n"
                except:
                    file_contents += f"File: /{os.path.relpath(file_path, path)}\nContent: Error reading file\n\n"
            else:
                file_contents += f"File: /{os.path.relpath(os.path.join(root, name), path)}\nContent: Skipped binary file\n\n"
    return file_contents


def get_file_contents_iteratively(repo):
    file_contents = ""
    dirs_to_visit = [("", repo.get_contents(""))]
    dirs_visited = set()
    global binary_extensions

    while dirs_to_visit:
        path, contents = dirs_to_visit.pop()
        dirs_visited.add(path)
        for content in tqdm(contents, desc=f"Downloading {path}", leave=False):
            if content.type == "dir":
                if content.path not in dirs_visited:
                    dirs_to_visit.append(
                        (f"{path}/{content.name}", repo.get_contents(content.path))
                    )
            else:
                # Check if the file extension suggests it's a binary file
                if any(content.name.endswith(ext) for ext in binary_extensions):
                    file_contents += (
                        f"File: {path}/{content.name}\nContent: Skipped binary file\n\n"
                    )
                else:
                    file_contents += f"File: {path}/{content.name}\n"
                    try:
                        if content.encoding is None or content.encoding == "none":
                            file_contents += (
                                "Content: Skipped due to missing encoding\n\n"
                            )
                        else:
                            try:
                                decoded_content = content.decoded_content.decode(
                                    "utf-8"
                                )
                                file_contents += f"Content:\n{decoded_content}\n\n"
                            except UnicodeDecodeError:
                                try:
                                    decoded_content = content.decoded_content.decode(
                                        "latin-1"
                                    )
                                    file_contents += f"Content (Latin-1 Decoded):\n{decoded_content}\n\n"
                                except UnicodeDecodeError:
                                    file_contents += "Content: Skipped due to unsupported encoding\n\n"
                    except (AttributeError, UnicodeDecodeError):
                        file_contents += "Content: Skipped due to decoding error or missing decoded_content\n\n"
    return file_contents


def is_binary(filename):
    return any(filename.endswith(ext) for ext in binary_extensions)


def get_repo_contents(repo_url):
    """
    Main function to get repository contents.
    """
    repo_name = repo_url.split("/")[-1]
    if not GITHUB_TOKEN:
        raise ValueError(
            "Please set the 'GITHUB_TOKEN' environment variable or the 'GITHUB_TOKEN' in the script."
        )
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_url.replace("https://github.com/", ""))
    print(f"Fetching README for: {repo_name}")
    readme_content = get_readme_content(repo)

    print(f"\nFetching repository structure for: {repo_name}")
    repo_structure = f"Repository Structure: {repo_name}\n"
    repo_structure += traverse_repo_iteratively(repo)

    print(f"\nFetching file contents for: {repo_name}")
    file_contents = get_file_contents_iteratively(repo)

    instructions = f"Prompt: Analyze the {repo_name} repository to understand its structure, purpose, and functionality. Follow these steps to study the codebase:\n\n"
    instructions += "1. Read the README file to gain an overview of the project, its goals, and any setup instructions.\n\n"
    instructions += "2. Examine the repository structure to understand how the files and directories are organized.\n\n"
    instructions += "3. Identify the main entry point of the application (e.g., main.py, app.py, index.js) and start analyzing the code flow from there.\n\n"
    instructions += "4. Study the dependencies and libraries used in the project to understand the external tools and frameworks being utilized.\n\n"
    instructions += "5. Analyze the core functionality of the project by examining the key modules, classes, and functions.\n\n"
    instructions += "6. Look for any configuration files (e.g., config.py, .env) to understand how the project is configured and what settings are available.\n\n"
    instructions += "7. Investigate any tests or test directories to see how the project ensures code quality and handles different scenarios.\n\n"
    instructions += "8. Review any documentation or inline comments to gather insights into the codebase and its intended behavior.\n\n"
    instructions += "9. Identify any potential areas for improvement, optimization, or further exploration based on your analysis.\n\n"
    instructions += "10. Provide a summary of your findings, including the project's purpose, key features, and any notable observations or recommendations.\n\n"
    instructions += (
        "Use the files and contents provided below to complete this analysis:\n\n"
    )

    return repo_name, instructions, readme_content, repo_structure, file_contents


def analyze_local_repo(path, binary_extensions):
    """
    Analyze a local repository to understand its structure and contents.
    :param path: absolute path to the local repository
    :param binary_extensions: list of binary file extensions to skip during analysis
    :return: string containing the analysis results
    """
    print(f"Analyzing local repository at: {path}")

    readme_content = get_readme_content(path)
    repo_structure = traverse_directory(path)
    file_contents = get_file_contents(path, binary_extensions)

    # Combine all the parts into one output
    output_content = (
        "README:\n" + readme_content + "\n\n" + repo_structure + "\n\n" + file_contents
    )
    return output_content


def traverse_directory(path):
    structure = "Repository Structure:\n"
    for root, dirs, files in os.walk(path):
        relative_path = os.path.relpath(root, path)
        if relative_path == ".":
            relative_path = ""
        else:
            relative_path += "/"
        for name in dirs:
            structure += f"/{relative_path}{name}/\n"
        for name in files:
            structure += f"/{relative_path}{name}\n"
    return structure


def get_prompt(prompt_path):
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def init(config_path):
    filename_opened = open(config_path, mode="r")

    j = {}
    j = json.load(filename_opened)

    filename_opened.close()
    return j


def get_local_repo_contents(directory_path):
    """
    Main function to get local repository contents.
    """
    repo_name = directory_path.split("/")[-1]

    print(f"Fetching README for: {repo_name}")
    readme_content = get_local_readme_content(directory_path)

    print(f"\nFetching repository structure for: {repo_name}")
    repo_structure = f"Repository Structure: {repo_name}\n"
    repo_structure += get_local_structure(directory_path)

    print(f"\nFetching file contents for: {repo_name}")
    file_contents = get_local_file_contents_iteratively(directory_path)

    instructions = get_instructions(repo_name)

    return repo_name, instructions, readme_content, repo_structure, file_contents


def get_local_structure(directory_path):
    """
    Generate the structure of a local directory.
    """
    structure = ""
    for root, dirs, files in os.walk(directory_path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            relative_path = os.path.relpath(dir_path, directory_path)
            structure += f"{relative_path}/\n"

        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, directory_path)
            structure += f"{relative_path}\n"
    return structure


def get_local_file_contents_iteratively(directory_path):
    """
    Generate the contents of files in a local directory.
    """
    file_contents = ""
    global binary_extensions

    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, directory_path)
            file_contents += f"File: {relative_path}\n"
            if any(file_name.endswith(ext) for ext in binary_extensions):
                file_contents += "Content: Skipped binary file\n\n"
            else:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    file_contents += f"Content:\n{content}\n\n"
                except UnicodeDecodeError:
                    try:
                        with open(file_path, "r", encoding="latin-1") as f:
                            content = f.read()
                        file_contents += f"Content (Latin-1 Decoded):\n{content}\n\n"
                    except UnicodeDecodeError:
                        file_contents += (
                            "Content: Skipped due to unsupported encoding\n\n"
                        )
                except Exception as e:
                    file_contents += f"Content: Skipped due to error: {str(e)}\n\n"
    return file_contents


def get_instructions(repo_name):
    """
    Generate instructions for analyzing a local directory.
    """
    instructions = f"Prompt: Analyze the {repo_name} repository to understand its structure, purpose, and functionality. Follow these steps to study the codebase:\n\n"
    instructions += "1. Read the README file to gain an overview of the project, its goals, and any setup instructions.\n\n"
    instructions += "2. Examine the repository structure to understand how the files and directories are organized.\n\n"
    instructions += "3. Identify the main entry point of the application (e.g., main.py, app.py, index.js) and start analyzing the code flow from there.\n\n"
    instructions += "4. Study the dependencies and libraries used in the project to understand the external tools and frameworks being utilized.\n\n"
    instructions += "5. Analyze the core functionality of the project by examining the key modules, classes, and functions.\n\n"
    instructions += "6. Look for any configuration files (e.g., config.py, .env) to understand how the project is configured and what settings are available.\n\n"
    instructions += "7. Investigate any tests or test directories to see how the project ensures code quality and handles different scenarios.\n\n"
    instructions += "8. Review any documentation or inline comments to gather insights into the codebase and its intended behavior.\n\n"
    instructions += "9. Identify any potential areas for improvement, optimization, or further exploration based on your analysis.\n\n"
    instructions += "10. Provide a summary of your findings, including the project's purpose, key features, and any notable observations or recommendations.\n\n"
    instructions += (
        "Use the files and contents provided below to complete this analysis:\n\n"
    )
    return instructions


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze a local directory or a GitHub repository."
    )
    parser.add_argument(
        "directory", nargs="?", default=None, help="Path to the directory to analyze."
    )
    args = parser.parse_args()

    if args.directory is not None:
        # Command-line argument provided
        directory_path = args.directory
        try:
            repo_name, instructions, readme_content, repo_structure, file_contents = (
                get_local_repo_contents(directory_path)
            )
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please check the repository URL and try again.")
    else:
        # No command-line argument provided, prompt user for input
        repo_url = input("Please enter the GitHub repository URL: ")
        try:
            repo_name, instructions, readme_content, repo_structure, file_contents = (
                get_repo_contents(repo_url)
            )
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please check the repository URL and try again.")

    try:
        output_filename = f"{repo_name}_contents.txt"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(instructions)
            f.write(f"README:\n{readme_content}\n\n")
            f.write(repo_structure)
            f.write("\n\n")
            f.write(file_contents)
        print(f"Repository contents saved to '{output_filename}'.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check the repository URL and try again.")
