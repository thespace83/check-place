import time
import requests
import json


# 1343734
def get_place(url: str, idApplication: int) -> int:
    response = requests.get(url)
    response.raise_for_status()
    data: dict = response.json()

    place: int = 1
    for applicant in data["applicants"]:
        if applicant["idApplication"] == idApplication:
            return place
        if applicant["consent"] == "ONLINE" or applicant["consent"] == "OFFLINE":
            place += 1
        elif applicant["consent"] != "NONE":
            raise Exception(f"Тип поданного согласия {applicant['consent']}")
    raise Exception(f"Меня нет в конкурсном списке f{url}")


def main():
    config: dict = json.loads(open("config.json", "r", encoding="utf-8").read())

    idApplication: int = int(input("Здесь введи свой ID: "))
    requests_delay: float = float(
        input("А здесь введи задержку между запросами (сек.): ")
    )
    if requests_delay < 0.5:
        raise Exception(
            "Не стоит ставить столь маленькую задержку, госуслуги могут посчитать это DDoS-атакой ;)"
        )

    running = True
    while running:
        for university in config.keys():
            print(f" * {university}")
            for specialty in config[university].keys():
                print(
                    f"    -> {specialty}: {get_place(config[university][specialty]['url'], idApplication)} из {config[university][specialty]['numberOfPlaces']}"
                )
                time.sleep(requests_delay)


if __name__ == "__main__":
    main()
