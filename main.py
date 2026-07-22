import time
import requests
import json


def get_place(url: str) -> int:
    response = requests.get(url)
    response.raise_for_status()
    data: dict = response.json()

    place: int = 1
    for applicant in data["applicants"]:
        if applicant["idApplication"] == 1343734:
            return place
        if applicant["consent"] == "ONLINE" or applicant["consent"] == "OFFLINE":
            place += 1
        elif applicant["consent"] != "NONE":
            raise Exception(f"Тип поданного согласия {applicant['consent']}")
    raise Exception(f"Меня нет в конкурсном списке f{url}")


def main():
    config: dict = json.loads(open("config.json", "r", encoding="utf-8").read())
    for university in config.keys():
        print(f" * {university}")
        for specialty in config[university].keys():
            print(
                f"    -> {specialty}: {get_place(config[university][specialty]['url'])} из {config[university][specialty]['numberOfPlaces']}"
            )
            time.sleep(1)


if __name__ == "__main__":
    main()
