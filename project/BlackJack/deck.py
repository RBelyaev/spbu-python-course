from itertools import product
import random


class Card:
    """
    Represents a playing card with a name (value) and suit.

    Attributes:
        name (str): The card's value (2-10, J, Q, K, A)
        suit (str): The card's suit (♥, ♦, ♣, ♠)
    """

    def __init__(self, name: str, suit: str) -> None:
        """
        Initializes a new card with the given name and suit.

        Args:
            name (str): The card's value/rank
            suit (str): The card's suit symbol
        """
        self.name = name
        self.suit = suit

    def __str__(self) -> str:
        """
        Returns the string representation of the card (name + suit).

        Returns:
            str: Concatenation of card name and suit (e.g. "A♥")
        """
        return f"{self.name}{self.suit}"


class Deck:
    """
    Represents a standard 52-card deck of playing cards.

    Attributes:
        count (int): Tracks how many cards have been dealt
        cards (List[Card]): The list of cards in the deck
    """

    def __init__(self) -> None:
        """
        Initializes a new deck with all 52 standard playing cards.
        Cards are ordered by value (2-A) and suit (hearts, diamonds, clubs, spades).
        """
        self.count = 0
        self.cards = [
            Card(card[0], card[1])
            for card in product(
                ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"],
                ["♥", "♦", "♣", "♠"],
            )
        ]

    def shuffle(self) -> None:
        """
        Shuffles the deck randomly and resets the dealt card counter.
        """
        random.shuffle(self.cards)
        self.count = 0

    def get_card(self) -> "Card":
        """
        Deals the next card from the deck.

        Returns:
            Card: The next card in the deck

        Note:
            Increments the internal counter tracking dealt cards.
            Does not check if deck is empty before dealing.
        """
        self.count += 1
        return self.cards[self.count - 1]
