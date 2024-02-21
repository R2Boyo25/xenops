from dataclasses import dataclass

Point = tuple[int, int]

@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int

    def contains_point(self, point: Point) -> bool:
        return (
            point[0] >= self.x
            and point[0] <= self.x + self.w
            and point[1] >= self.y
            and point[1] <= self.y + self.h
        )