"""Three nested terminal bars, using only the standard library."""

import shutil
import sys


class Progress:
    def __init__(self, rows, questions, answers, stream=None):
        self.stream = stream if stream is not None else sys.stderr
        self.bars = [["Rows", 0, rows, ""], ["Questions", 0, questions, ""],
                     ["Debate", 0, answers, ""]]
        self.drawn = False

    def update(self, level, done=None, detail=None, reset_children=False):
        if done is not None:
            self.bars[level][1] = done
        if detail is not None:
            self.bars[level][3] = detail
        if reset_children:
            for bar in self.bars[level + 1:]:
                bar[1], bar[3] = 0, ""
        lines = []
        for depth, (name, count, total, text) in enumerate(self.bars):
            filled = int(20 * count / total)
            bar = "#" * filled + "-" * (20 - filled)
            lines.append(f"{'  ' * depth}{name}: [{bar}] {count}/{total} | {text}")
        if self.stream.isatty():
            width = max(1, shutil.get_terminal_size().columns - 1)
            if self.drawn:
                self.stream.write("\033[3A")
            for line in lines:
                self.stream.write("\r\033[2K" + line[:width] + "\n")
        else:
            # Redirected logs remain readable, with no terminal escape codes.
            self.stream.write(lines[level] + "\n")
        self.stream.flush()
        self.drawn = True
