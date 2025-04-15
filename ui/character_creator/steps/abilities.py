import pygame

from ui.utils.text_renderer import draw_text
from .creation_step import CreationStep
from ..data.abilities import ABILITY_NAMES, create_default_scores
from .skills import SkillStep
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..character_creator import CharacterCreator

class AbilityStep(CreationStep):
    def __init__(self, creator: "CharacterCreator") -> None:
        super().__init__(creator)
        self.ability_names = ABILITY_NAMES
        self.selected_index = 0
        if not hasattr(creator, "ability_scores"):
            creator.ability_scores = create_default_scores()
        if not hasattr(creator, "ability_score_points"):
            creator.ability_score_points = 27

    def draw(self) -> None:
        draw_text(f"Assign ability points (Remaining: {self.creator.ability_score_points})", self.center_x, self.center_y-100)
        draw_text("Up/Down: Select | Left/Right: Adjust | Enter: Confirm", self.center_x, self.center_y - 75, font_size=20)

        for i, ability in enumerate(self.ability_names):
            y_pos = self.center_y - 50 + i * 40
            score = self.creator.ability_scores[ability]
            cost = self.calculate_ability_cost(score) if i == self.selected_index else 0

            if i == self.selected_index:
                text = f"> {ability}: {score} (Next: {cost}) <"
                color = (255, 255, 0)
            else:
                text = f"{ability}: {score}"
                color = (255, 255, 255)
            draw_text(text, self.center_x, y_pos, color=color)

    def handle_event(self, event: pygame.event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.ability_names)
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.ability_names)
            elif event.key == pygame.K_RIGHT:
                self._increase_ability()
            elif event.key == pygame.K_LEFT:
                self._decrease_ability()
            elif event.key == pygame.K_RETURN:
                if self.creator.ability_score_points == 0:
                    self.creator.set_step(SkillStep)     
    
    def calculate_ability_cost(self, ability_score: int) -> int:
        if ability_score < 8 or ability_score >= 15:
            return 0
        return 2 if ability_score >= 13 else 1
    
    def _increase_ability(self) -> None:
        ability = self.ability_names[self.selected_index]
        current_value = self.creator.ability_scores[ability]

        if current_value >= 15:
            return
        
        cost = self.calculate_ability_cost(current_value)
        if cost > self.creator.ability_score_points:
            return
        
        self.creator.ability_scores[ability] += 1
        self.creator.ability_score_points -= cost

    def _decrease_ability(self) -> None:
        ability = self.ability_names[self.selected_index]
        current_value = self.creator.ability_scores[ability]

        if current_value <= 8:
            return
        
        refund = self.calculate_ability_cost(current_value - 1)
        self.creator.ability_scores[ability] -= 1
        self.creator.ability_score_points += refund