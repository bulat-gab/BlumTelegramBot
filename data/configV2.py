from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsV2(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str

    DELAYS: dict[str, list[int]] = {
        'ACCOUNT': [5, 15],  # delay between connections to accounts (the more accounts, the longer the delay)
        'PLAY': [5, 15],   # delay between play in seconds
        'ERROR_PLAY': [60, 180],    # delay between errors in the game in seconds
    }

    # Use proxies or not
    PROXY: bool = True

    # Play drop game
    PLAY_GAMES: bool = True

    # points with each play game; max 280
    POINTS: list[int] = [220, 270]

    # title blacklist tasks (do not change)
    BLACKLIST_TASKS: list[str] = ['Farm points']

    # session folder (do not change)
    WORKDIR: str = "sessions/"

    ACCOUNT_PER_ONCE: int = 3

    SOLVE_TASKS: bool


settingsV2 = SettingsV2()