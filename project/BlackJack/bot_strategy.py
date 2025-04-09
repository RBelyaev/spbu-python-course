from abc import ABC, abstractmethod
import project.BlackJack.deck


class Strategy(ABC):
    """
    Abstract base class defining the interface for different Blackjack playing strategies.
    All concrete strategy implementations must implement the decide_hit method.
    """

    @abstractmethod
    def decide_hit(self, score: int) -> bool:
        """
        Determines whether the player should hit (take another card) based on current hand score.

        Args:
            score (int): The current total value of the player's hand.

        Returns:
            bool: True if the player should hit, False otherwise.
        """
        pass


class AccurateStrategy(Strategy):
    """
    Strategy where the player hits if the hand value is less than 14.
    """

    def decide_hit(self, score: int) -> bool:
        """
        Implements the conservative hitting strategy.

        Args:
            score (int): Current hand value.

        Returns:
            bool: True if score < 14, False otherwise.
        """
        return score < 14


class AggressiveStrategy(Strategy):
    """
    Strategy where the player hits if the hand value is less than 17.
    """

    def decide_hit(self, score: int) -> bool:
        """
        Implements the aggressive hitting strategy.

        Args:
            score (int): Current hand value.

        Returns:
            bool: True if score < 17, False otherwise.
        """
        return score < 17


class CountingStrategy(Strategy):
    """
    Advanced strategy that uses card counting to adjust hitting decisions.
    Maintains a running count of high/low cards to determine optimal play.

    Attributes:
        count (int): Running count of card advantage (positive favors player).
    """

    def __init__(self) -> None:
        """Initializes the counting strategy with a zero count."""

        self.count: int = 0

    def update_count(self, card: project.BlackJack.deck.Card) -> None:
        """
        Updates the running count based on the card that was dealt.
        Uses Hi-Lo counting system:
        - Low cards (2-6) increase count (+1)
        - High cards (10-A) decrease count (-1)
        - Neutral cards (7-9) don't affect count

        Args:
            card (Card): The card that was dealt and needs to be counted.
        """
        if card.name in ["2", "3", "4", "5", "6"]:
            self.count += 1
        elif card.name in ["10", "J", "Q", "K", "A"]:
            self.count -= 1

    def decide_hit(self, score: int) -> bool:
        """
        Makes hitting decision based on current hand score and count value.
        - When count is favorable (> +2), hits until 18
        - When count is unfavorable (< -2), stands earlier
        - Otherwise uses standard basic strategy (hit until 16)

        Args:
            score (int): Current hand value.

        Returns:
            bool: Whether the player should hit based on count-adjusted strategy.
        """

        if self.count > 2:
            return score < 19
        elif self.count < -2:
            return score < 16
        else:
            return score < 17
