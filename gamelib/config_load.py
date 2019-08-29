from gamelib import file_io


def load_config():
    loaded_config = file_io.config_load()
    config_map = {
        'screen_x_axis': loaded_config["display_size"]["display_x"],
        'screen_y_axis': loaded_config["display_size"]["display_y"],
        'starting_lives': loaded_config["lives"]["starting_lives"],
        'max_lives': loaded_config["lives"]["max_lives"],
        'spawn_water': loaded_config["lives"]["water"],
        'lives_spawn_rate': loaded_config["lives"]["lives_spawn_rate"],
        'spawn_gems': loaded_config["gems"]["spawn_gems"],
        'gem1_score': loaded_config["gems"]["gem1"],
        'gem2_score': loaded_config["gems"]["gem2"],
        'gem3_score': loaded_config["gems"]["gem3"],
        'gem4_score': loaded_config["gems"]["gem4"],
        'gem5_score': loaded_config["gems"]["gem5"],
        'enemy_spawn_rate': loaded_config["enemies"]["spawn_rate"],
        'game_level_up': loaded_config["enemies"]["level_up"],
        'level_up_spawn_increase': loaded_config["enemies"]["spawn_increase"],
        'first_level_up': loaded_config["enemies"]["levelup_1"],
        'second_level_up': loaded_config["enemies"]["levelup_2"],
        'enemy_min_speed': loaded_config["enemies"]["min_speed"],
        'enemy_max_speed': loaded_config["enemies"]["max_speed"]
    }
    return config_map



