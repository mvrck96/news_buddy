from datetime import date


def get_md_message_unified(name: str, digest: dict) -> str:
    today = date.today().strftime("%d.%m.%y")
    message = f"{name} картина дня от {today}\n\n\n"
    for key in digest:
        tmp = f"--  [{digest[key]}]({key})\n\n"
        message += tmp
    return message


if __name__ == "__main__":
    print(__file__)
