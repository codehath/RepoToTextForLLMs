import os
from github import Github
from tqdm import tqdm
from dotenv import load_dotenv
import pyperclip

load_dotenv()  # Load variables from .env file

try:
    OUTPUT_DIR = os.environ["OUTPUT_DIR"]
    if OUTPUT_DIR == "DEFAULT":
        OUTPUT_DIR = ""
except:
    OUTPUT_DIR = ""

try:
    GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
except KeyError:
    GITHUB_TOKEN = None
    print("Warning: GitHub Personal Access Token not found in environment variables.")
    print("You will only be able to convert local repositories")

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
    ".lock",
    ".lockb",
    "package-lock.json",
    "pnpm-lock.yaml",
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


def get_structure_iteratively(repo):
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


def get_local_structure(directory_path):
    """
    Generate the structure of a local directory, excluding the .git folder.
    """
    structure = ""
    for root, dirs, files in os.walk(directory_path):
        dirs[:] = [d for d in dirs if d != ".git"]  # Exclude the .git folder
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            relative_path = os.path.relpath(dir_path, directory_path)
            structure += f"{relative_path}/\n"

        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, directory_path)
            structure += f"{relative_path}\n"
    return structure


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
                # Skip the README file
                if content.name.lower() == "readme.md":
                    continue

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


def get_local_file_contents_iteratively(directory_path):
    """
    Generate the contents of files in a local directory, excluding the .git folder and README file.
    """
    file_contents = ""
    global binary_extensions

    for root, dirs, files in os.walk(directory_path):
        dirs[:] = [d for d in dirs if d != ".git"]  # Exclude the .git folder
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, directory_path)

            # Skip the README file and files in the .git folder
            if relative_path.startswith(".git/") or file_name.lower() == "readme.md":
                continue

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


def get_instructions(prompt_path, repo_name):
    with open(prompt_path, "r", encoding="utf-8") as f:
        instructions = f.read()
        instructions = instructions.replace("##REPO_NAME##", repo_name)
        return instructions


def set_functions(is_local):
    if is_local:
        get_readme = get_local_readme_content
        get_structure = get_local_structure
        get_files = get_local_file_contents_iteratively
    else:
        get_readme = get_readme_content
        get_structure = get_structure_iteratively
        get_files = get_file_contents_iteratively

    return get_readme, get_structure, get_files


def get_repo_contents(repo_path_or_url, is_local=False):
    """
    Main function to get repository contents.
    """
    repo_name = repo_path_or_url.split("/")[-1]
    if is_local:
        repo_or_path = repo_path_or_url
    else:
        if not GITHUB_TOKEN:
            raise ValueError(
                "Please set the 'GITHUB_TOKEN' environment variable or the 'GITHUB_TOKEN' in the script."
            )
        g = Github(GITHUB_TOKEN)
        repo_or_path = g.get_repo(repo_path_or_url.replace("https://github.com/", ""))

    get_readme, get_structure, get_files = set_functions(is_local)

    print(f"Fetching README for: {repo_name}")
    readme_content = get_readme(repo_or_path)

    print(f"\nFetching repository structure for: {repo_name}")
    repo_structure = f"Repository Structure: {repo_name}\n"
    repo_structure += get_structure(repo_or_path)

    print(f"\nFetching file contents for: {repo_name}")
    file_contents = get_files(repo_or_path)

    instructions = get_instructions("instructions-prompt.txt", repo_name)

    return repo_name, instructions, readme_content, repo_structure, file_contents


def analyze_repo(repo_path_or_url, is_local=False):
    try:
        repo_name, instructions, readme_content, repo_structure, file_contents = (
            get_repo_contents(repo_path_or_url, is_local)
        )
        output_filename = f"{repo_name}_contents.txt"
        with open(OUTPUT_DIR + output_filename, "w", encoding="utf-8") as f:
            f.write(instructions)
            f.write("\n\n")
            f.write(f"README:\n{readme_content}\n\n")
            f.write(repo_structure)
            f.write("\n\n")
            f.write(file_contents)

        # Combine all extracted content into a single string
        all_content = f"{instructions}\n\nREADME:\n{readme_content}\n\n{repo_structure}\n\n{file_contents}"

        # Copy the content to clipboard
        pyperclip.copy(all_content)
        print(
            f"Repository contents copied to clipboard and saved to '{output_filename}'."
        )
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")
        if is_local:
            print("Please provide a valid directory path.")
        else:
            print("Please check the repository URL and try again.")


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
        analyze_repo(os.path.realpath(args.directory), is_local=True)
    else:
        # No command-line argument provided, prompt user for input
        repo_url = input("Please enter the GitHub repository URL: ")
        analyze_repo(repo_url)
