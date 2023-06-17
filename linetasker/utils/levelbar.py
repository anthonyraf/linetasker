class LevelBar(str):
    def __new__(cls, level: int):
        if int(level) < 1:
            raise ValueError("Level must be positive non-null integer")

        return super().__new__(
            cls, cls.colorize(level) + f"[gray74] {level}[/gray74]"
        )

    @staticmethod
    def colorize(level: int) -> str:
        level = level
        bar = "⢀⣀⣠⣤⣴⣶⣾⣿"
        colors = [
            "light_green",
            "green",
            "yellow",
            "gold1",
            "dark_orange",
            "orange_red",
            "red",
            "red3",
        ]
        tmp = ["gray35"] * 8
        tmp[: level * 2] = colors[: level * 2]

        colored_bar = ""

        for i, char in enumerate(bar):
            colored_bar += f"[{tmp[i]}]{char}"

        return colored_bar
