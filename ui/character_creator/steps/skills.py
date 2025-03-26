import pygame

from ui.utils.text_renderer import draw_text
from .creation_step import CreationStep
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..character_creator import CharacterCreator

class SkillStep(CreationStep):
    def __init__(self, creator: "CharacterCreator") -> None:
        super().__init__(creator)
        self.skills = self.creator.character_class.skill_proficiencies
        self.selected_index = 0
        self.max_skills = self.creator.character_class.skill_proficiency_points
        self.selected_skills = []

    def draw(self) -> None:
        draw_text(f"Choose {self.max_skills} skill proficiencies", self.center_x, self.center_y - 100)
        draw_text("Up/Down: Navigate | Enter: Select | Space: Confirm", 
                self.center_x, self.center_y - 75, font_size=20)

        for i, skill in enumerate(self.skills):
            y_pos = self.center_y - 50 + i * 40
            prefix = "> " if i == self.selected_index else "  "
            suffix = " X" if skill in self.selected_skills else ""

            draw_text(f"{prefix}{skill}{suffix}", self.center_x, y_pos)

    def handle_event(self, event: pygame.event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.skills)
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.skills)
            elif event.key == pygame.K_RETURN:
                    self._toggle_skill()
            elif event.key == pygame.K_SPACE:
                if len(self.selected_skills) == self.max_skills:
                    self.creator.complete_creation()
                else:
                    pass

    def _toggle_skill(self) -> None:
        skill = self.skills[self.selected_index]

        if skill in self.selected_skills:
            self.selected_skills.remove(skill)
        elif len(self.selected_skills) < self.max_skills:
            self.selected_skills.append(skill)

        self.creator.skills = self.selected_skills