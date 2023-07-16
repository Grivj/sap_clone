from ..events import BuyEvent, Event
from .ability import Ability


class OnBuyAbility(Ability):
    def trigger(self, event: Event) -> None:
        # The ability is triggered when the pet is bought
        if isinstance(event, BuyEvent):
            self.do_effect()

    def do_effect(self) -> None:
        ...
