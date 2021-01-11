from game.config import WorldConfig


default_slalom_config = WorldConfig.builder() \
    .set_width(800) \
    .set_difficulty(1) \
    .set_gravity(100) \
    .set_inclination(60) \
    .set_friction(0.4) \
    .set_flags_start(300) \
    .set_distance_between_flags(200) \
    .set_flags_margin_horizontal(100) \
    .set_flags_margin_vertical(250) \
    .set_trees_margin_to_flags(100) \
    .set_flags_ammount(20) \
    .set_trees_ammount(40) \
    .build()

default_downhill_config = WorldConfig.builder() \
    .set_width(800) \
    .set_height(9000) \
    .set_difficulty(1) \
    .set_gravity(100) \
    .set_inclination(60) \
    .set_friction(0.4) \
    .set_trees_ammount(200) \
    .build()
