
from src.section import Section
from src.performance import Performance

class Score:

  def __init__(self, cfg, name, sections):
    self.cfg = cfg
    self.name = name
    self.raw_sections = sections
    self.sections = {k:Section(cfg,k,v) for (k,v) in sections.items()}
    self.section_index = 0


  @staticmethod
  def create_performance_version(cfg, score, new_name):
    new_sections = Performance.create(cfg, score.raw_sections)
    new_score = Score(score.cfg, new_name, new_sections)
    return new_score


  @property
  def section(self):
    name = list(self.sections.keys())[self.section_index]
    return self.sections[name]


  @property
  def pos(self):
    return self.section.pos


  @property
  def tracks(self):
    return self.section.tracks


  def get_section(self, index):
    name = list(self.sections.keys())[index]
    return self.sections[name]


  def select_section(self, index):
    if -1 < index < len(self.sections):
      self.section_index = index
      self.section.reset_pos()


  def prev_section(self):
    self.section_index -= 1
    if self.section_index < 0:
      self.section_index = len(self.sections)-1
    self.section.reset_pos()


  def next_section(self):
    self.section_index = (self.section_index + 1) % len(self.sections)
    self.section.reset_pos()


  def reset(self):
    self.section.reset()


  def reset_section(self):
    self.section_index = 0


  def reset_pos(self):
    self.section.reset_pos()


  def go_to_start(self):
    self.section.go_to_start()


  def go_to_end(self):
    self.section.go_to_end()


  def reset_all_sections(self):
    for section in self.sections.values():
      section.reset()


  def shift_n16(self, n16=1):
    self.section.shift_n16(n16)


  def shift_n4(self, n4=1):
    self.section.shift_n4(n4)


  def toggle_track_mute(self, index):
    self.section.toggle_track_mute(index)


  def toggle_track_solo(self, index):
    self.section.toggle_track_solo(index)

