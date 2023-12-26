import city_block
import math
from functools import partial


def distance_dikstra(block: city_block.CityBlock) -> int:
    """Calculates distance for search algorithm"""
    return city_block.CityBlock.heat_loss


def distance_a_star(block: city_block.CityBlock, end_position: tuple[int, int]) -> int:
    return (
        math.sqrt(
            (end_position[0] - block.loc[0]) ^ 2 + (end_position[1] - block.loc[1]) ^ 2
        )
        + block.heat_loss
    )


def get_distance_a_star(
    end_position: tuple[int, int]
) -> callable[city_block.CityBlock, int]:
    return partial(distance_a_star, end_position=end_position)
