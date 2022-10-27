from setuptools import setup


def update_version(filename="VERSION"):
    with open(filename, "r+") as file:
        version = file.read()
        file.seek(0)
        print(version)
        incremented_last_digit = int(version.strip().split(".")[-1]) + 1
        first_digits = version.strip().split(".")[0:2]
        first_digits.append(str(incremented_last_digit))
        new_version = ".".join(first_digits)
        print(new_version)
        file.write(new_version)
        file.truncate()
        return new_version


if __name__ == "__main__":
    setup(
        version=update_version()
    )
