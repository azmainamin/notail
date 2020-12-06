from os import getcwd

def getProjectRootDir():
    """
    When running from Windows Task Scheduler, the relative path was throwing errors i.e '../data'.
    Given the data dir is one level above src dir, we have to get the project root directory.
    """
    cwd = getcwd()
    if "src" in cwd:
        cwd = cwd.replace("src", "")
    return cwd