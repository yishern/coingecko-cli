# trunk-ignore(bandit/B404)
import subprocess


def get_n_terminal_cols(*, default: int | None = 80) -> int:
    try:
        # trunk-ignore(bandit/B602)
        # trunk-ignore(bandit/B607)
        output = subprocess.check_output('tput cols', shell=True)
        return int(output)
    except Exception as e:
        if default is not None:
            return default
        else:
            raise e


def get_n_terminal_rows(*, default: int | None = 80) -> int:
    try:
        # trunk-ignore(bandit/B602)
        # trunk-ignore(bandit/B607)
        output = subprocess.check_output('tput lines', shell=True)
        return int(output)
    except Exception as e:
        if default is not None:
            return default
        else:
            raise e
