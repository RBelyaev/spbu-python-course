from abc import ABC, abstractmethod
import project.BlackJack.deck
import project.BlackJack.bot_strategy
from typing import Optional, List


class Player(ABC):
    """
    Abstract base class representing a Blackjack player.

    Attributes:
        name (str): Player's name
        chips (int): Player's chip balance (default: 1000)
        hand (List[Card]): Cards currently held by player
        score (int): Current calculated value of player's hand
    """

    def __init__(self, name: str, chips: int = 1000) -> None:
        """
        Initializes a new player with given name and starting chips.

        Args:
            name (str): Player identifier
            chips (int): Starting chip balance (default: 1000)
        """
        self.name = name
        self.chips = chips
        self.hand: List[project.BlackJack.deck.Card] = []
        self.score = 0

    def get_card(self, card: project.BlackJack.deck.Card) -> None:
        """
        Adds a card to the player's hand.

        Args:
            card (Card): Card to be added to hand
        """
        self.hand.append(card)

    def calculate_score(self) -> None:
        """
        Calculates the current score of the player's hand according to Blackjack rules.
        Handles special case for Aces (counts as 11 unless it would bust the hand).
        """
        self.score = 0
        ace_flag = False
        if self.hand:
            for card in self.hand:
                match card.name:
                    case "A":
                        self.score += 1
                        ace_flag = True
                    case "K" | "Q" | "J" | "10":
                        self.score += 10
                    case _:
                        self.score += int(card.name)
            if ace_flag and self.score <= 11:
                self.score += 10

    def place_bet(self, amount: int) -> int:
        """
        Places a bet from player's chips.

        Args:
            amount (int): Desired bet amount

        Returns:
            int: Actual bet amount (may be less if player lacks chips)
        """
        amount = min(amount, self.chips)
        return amount

    def settle_bet(self, amount: int) -> None:
        """
        Adjusts player's chip balance based on bet outcome.

        Args:
            amount (int): Amount to add/subtract from balance
        """
        self.chips += amount

    @abstractmethod
    def decide_hit(self) -> bool:
        """
        Abstract method to determine whether player wants another card.

        Returns:
            bool: True if player wants to hit, False to stand
        """
        pass


class Bot(Player):
    """
    AI-controlled player that follows a predefined strategy.

    Attributes:
        strategy (Strategy): The decision-making strategy the bot follows
    """

    def __init__(
        self,
        strategy: project.BlackJack.bot_strategy.Strategy,
        name: str,
        chips: int = 1000,
    ) -> None:
        """
        Initializes a new bot player with specified strategy.

        Args:
            strategy (Strategy): The strategy implementation to use
            name (str): Bot identifier
            chips (int): Starting chip balance (default: 1000)
        """
        super().__init__(name, chips)
        self.strategy = strategy

    def decide_hit(self) -> bool:
        """
        Delegates hit decision to the bot's strategy.

        Returns:
            bool: Decision from strategy based on current score
        """
        return self.strategy.decide_hit(self.score)


class Dealer(Player):
    """
    Special player representing the house/dealer in Blackjack.
    Has unlimited chips and follows specific game rules.
    """

    def __init__(self):
        """
        Initializes dealer with maximum possible chips.
        """
        super().__init__("Dealer", 2**63 - 1)
        self.hide_card: Optional[project.BlackJack.deck.Card] = None

    def decide_hit(self) -> bool:
        """
        Dealer hit logic is handled by Game class.

        Raises:
            AttributeError: Always raises to indicate dealer logic is external
        """
        raise AttributeError(
            f"The logic of the dealer's game is defined in the Game class"
        )
