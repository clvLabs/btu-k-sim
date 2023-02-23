import pygame

class TextPrint:

  def __init__(self, screen, cfg, font_cfg):
    self.screen = screen
    self.cfg = cfg
    self.x = 0
    self.y = 0
    self.font = pygame.font.SysFont(font_cfg.Font.name, font_cfg.Font.size)
    self.line_height = font_cfg.line_height
    self.color = font_cfg.Color.normal


  def print(self, textString=None, color=None, newLine=True):
    if color is None:
      _color = self.color
    else:
      _color = color

    if textString:
      textBitmap = self.font.render(textString, True, _color)
      self.screen.blit(textBitmap, [self.x, self.y])

    if newLine:
      self.y += self.line_height


  def reset(self):
    self.x = 0
    self.y = 0


  def jump(self, amount=10):
    self.y += amount


  def indent(self, amount=10):
    self.x += amount


  def unindent(self, amount=10):
    self.x -= amount


