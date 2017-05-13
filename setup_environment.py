import os
from click import echo, style


def setup_environment_variables():
    """
    import environment variables    
    :return: 
    """
    if os.path.exists(".env"):
        echo(style(text=">>>> Importing environment variables from .env", fg="green", bold=True))
        for line in open(".env"):
            var = line.strip().split("=")
            if len(var) == 2:
                os.environ[var[0]] = var[1]

if __name__ == "__main__":
    setup_environment_variables()
