from datetime import date


def get_md_message_unified(name: str, digest: dict) -> str:
    today = date.today().strftime("%d.%m.%y")
    message = f"{name} картина дня от {today}\n\n\n"
    for key in digest:
        tmp = f"--  [{digest[key]}]({key})\n\n"
        message += tmp
    return message


def not_habr(message: str) -> bool:
    return (
        True
        if str(message).strip().lower() in ["habr", "start", "help", "rbc", "gazeta"]
        else False
    )

def get_name():
    pass


if __name__ == "__main__":
    print(__file__)
