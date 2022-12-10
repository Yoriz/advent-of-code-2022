import dataclasses
import typing

FILENAME = "day8_data.txt"


def yield_lines(filename: str) -> typing.Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.rstrip()


@dataclasses.dataclass
class VisibleFrom:
    top: bool = False
    right: bool = False
    bottom: bool = False
    left: bool = False


def create_visible_from() -> VisibleFrom:
    return VisibleFrom()


@dataclasses.dataclass
class Tree:
    height: int
    visible_from: VisibleFrom = dataclasses.field(default_factory=create_visible_from)
    scenic_score: int = dataclasses.field(default=0, init=False)

    @property
    def is_visibile(self) -> bool:
        return any(
            (
                self.visible_from.top,
                self.visible_from.right,
                self.visible_from.bottom,
                self.visible_from.left,
            )
        )


@dataclasses.dataclass
class Grid:
    trees: list[list[Tree]] = dataclasses.field(default_factory=list)

    def __str__(self) -> str:
        string = ""
        for row in self.trees:
            row_str = "".join((str(tree.height) for tree in row))
            string = f"{string}{row_str}\n"
        return string

    def find_trees_visble_from_left(self) -> None:
        for row in self.trees:
            max_height = -1
            for tree in row:
                if tree.height > max_height:
                    tree.visible_from.left = True
                    max_height = tree.height

    def find_trees_visble_from_right(self) -> None:
        for row in self.trees:
            max_height = -1
            for tree in row[::-1]:
                if tree.height > max_height:
                    tree.visible_from.right = True
                    max_height = tree.height

    def find_trees_visible_from_top(self) -> None:
        for col in list(zip(*self.trees)):
            max_height = -1
            for tree in col:
                if tree.height > max_height:
                    tree.visible_from.top = True
                    max_height = tree.height

    def find_trees_visible_from_bottom(self) -> None:
        for col in list(zip(*self.trees[::-1])):
            max_height = -1
            for tree in col:
                if tree.height > max_height:
                    tree.visible_from.bottom = True
                    max_height = tree.height

    def find_trees_visible_all_directions(self) -> None:
        self.find_trees_visble_from_left()
        self.find_trees_visble_from_right()
        self.find_trees_visible_from_top()
        self.find_trees_visible_from_bottom()

    @property
    def tress_visible(self) -> int:
        visible_count = 0
        for row in self.trees:
            for tree in row:
                if tree.is_visibile:
                    visible_count += 1
        return visible_count

    def find_scenic_scores(self) -> None:
        for row_index, row in enumerate(self.trees):
            for col_index, tree in enumerate(row):
                scenic_score = self.scenic_score_right(row_index, col_index)
                scenic_score *= self.scenic_score_left(row_index, col_index)
                scenic_score *= self.scenic_score_down(row_index, col_index)
                scenic_score *= self.scenic_score_up(row_index, col_index)
                tree.scenic_score = scenic_score

    def scenic_score_right(self, tree_row_index: int, tree_col_index: int):
        tree = self.trees[tree_row_index][tree_col_index]
        score = 0
        for index, col in enumerate(range(tree_col_index + 1, len(self.trees[0])), 1):
            score = index
            if self.trees[tree_row_index][col].height >= tree.height:
                break
        return score

    def scenic_score_left(self, tree_row_index: int, tree_col_index: int):
        tree = self.trees[tree_row_index][tree_col_index]
        score = 0
        for index, col in enumerate(range(tree_col_index - 1, -1, -1), 1):
            score = index
            if self.trees[tree_row_index][col].height >= tree.height:
                break
        return score

    def scenic_score_down(self, tree_row_index: int, tree_col_index: int):
        tree = self.trees[tree_row_index][tree_col_index]
        score = 0
        for index, row in enumerate(range(tree_row_index + 1, len(self.trees)), 1):
            score = index
            if self.trees[row][tree_col_index].height >= tree.height:
                break
        return score

    def scenic_score_up(self, tree_row_index: int, tree_col_index: int):
        tree = self.trees[tree_row_index][tree_col_index]
        score = 0
        for index, row in enumerate(range(tree_row_index - 1, -1, -1), 1):
            score = index
            if self.trees[row][tree_col_index].height >= tree.height:
                break
        return score

    @property
    def max_scenic_score(self) -> int:
        score = 0
        for row in self.trees:
            for tree in row:
                score = max(score, tree.scenic_score)
        return score


def create_grid(lines: typing.Iterator[str]) -> Grid:
    grid = Grid()
    for line in lines:
        row = [Tree(int(height)) for height in line]
        grid.trees.append(row)

    return grid


def part1(filename: str) -> None:
    lines = yield_lines(filename)
    grid = create_grid(lines)
    grid.find_trees_visible_all_directions()
    print(grid.tress_visible)


def part2(filename: str) -> None:
    lines = yield_lines(filename)
    grid = create_grid(lines)
    grid.find_scenic_scores()
    print(grid.max_scenic_score)


def main():
    part1(FILENAME)
    part2(FILENAME)


if __name__ == "__main__":
    main()
