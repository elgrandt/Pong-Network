import pygame

p = (               #sized 24x24
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "  XXXXXXXXXXXXXXX       ",
  " X...............X      ",
  "  XXXXXXXXX.......X     ",
  "      XXXXX.........X   ",
  "     X..............X   ",
  "      XXXXX.........X   ",
  "      XXXXX........X.X  ",
  "     X............X...X ",
  "      XXXXX......X.....X",
  "      XXXXX.....X.....X ",
  "     X.........X.....X  ",
  "      XXXXX...X.....X   ",
  "           X.X.....X    ",
  "            X..X..X     ",
  "             X...X      ",
  "              X.X       ",
  "               X        ",
  "                        ",
  "                        ",
  "                        ")

datatuple, masktuple  = pygame.cursors.compile(p, ".", "X")