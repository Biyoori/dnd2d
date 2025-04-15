from .creation_step import CreationStep
from typing import TYPE_CHECKING
from ui.utils.text_renderer import draw_text
from settings import get_color
from .abilities import AbilityStep
import pygame

if TYPE_CHECKING:
    from character_creator import CharacterCreator

class ItemStep(CreationStep):
    def __init__(self, creator: "CharacterCreator") -> None:
        super().__init__(creator)
        self.selected_index = 0
        self.gear_options = self.creator.character_class.starting_gear

        self.chosen_gear = []

        self.flattened_options = []
        item_counts = {}
        for category, items in self.gear_options.items():
            for item in items:
                if isinstance(item, list):
                    for subitem in item:
                        name, count = subitem if isinstance(subitem, tuple) else (subitem, 1)
                        key = (category, name)
                        item_counts[key] = item_counts.get(key, 0) + count
                else:
                    name, count = item if isinstance(item, tuple) else (item, 1)
                    key = (category, name)
                    item_counts[key] = item_counts.get(key, 0) + count

        self.flattened_options = [(category, name, count) for (category, name), count in item_counts.items()]
        print(self.flattened_options)

    def draw(self) -> None:
        y_offset = self.center_y - 150
        line_height = 30
        category_spacing = 50

        option_counter = 0
        last_category = None

        for flattened_option in self.flattened_options:
            category, item, count = flattened_option

            if category != last_category:
                if last_category is not None:
                    y_offset += category_spacing
                draw_text(f"Select {category}", self.center_x, y_offset, color=get_color("light-gray"))
                y_offset += line_height
                last_category = category

            color = get_color("white")
            if option_counter == self.selected_index:
                color = get_color("yellow")

            draw_text(f"> {item} x{count}" if color == get_color("yellow") else f" {item} x{count}", self.center_x, y_offset, color=color)
            y_offset += line_height
            option_counter += 1

        y_offset += category_spacing
        draw_text("Press SPACE to confirm selection", self.center_x, y_offset + 20, color=get_color("light-gray"))

    def handle_event(self, event: pygame.event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.flattened_options)
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.flattened_options)

            elif event.key == pygame.K_RETURN:
                category, selected_item, count = self.flattened_options[self.selected_index]

                already_picked = [(cat, item, cnt) for cat, item, cnt in self.chosen_gear if cat == category]
                print(f"Already picked: {already_picked}")
                if not already_picked:
                    self.chosen_gear.append((category, selected_item, count))
                    print(f"Selected gear: {selected_item} x {count}")
                else:
                    self.chosen_gear = [
                        (cat, item, cnt) if cat != category else (category, selected_item, count)
                        for cat, item, cnt in self.chosen_gear
                    ]
                    print(f"Replaced {already_picked[0]} with {selected_item}")
                    
            elif event.key == pygame.K_SPACE:
                chosen_categories = {cat for cat, _, _ in self.chosen_gear}
                if chosen_categories == set(self.gear_options.keys()):

                    self.creator.starting_gear = [
                        [item] * count for _, item, count in self.chosen_gear
                    ]
                    self.creator.set_step(AbilityStep)
                else:
                    print("You must select one item from each category before proceeding.")

        