import random
from typing import List, Dict, Optional
from abc import ABCMeta, abstractmethod
from project.BlackJack.players import Player, Bot, Dealer
import project.BlackJack.deck
import project.BlackJack.bot_strategy


class GameMeta(ABCMeta):
    """
    Metaclass for dynamically configuring game rules and bot strategies.

    Defines default game configuration:
    - MAX_PLAYERS: Maximum number of players (6)
    - BLACKJACK_PAYOUT: Payout multiplier for blackjack (1.5)
    - DEALER_STAND_SCORE: Dealer stands at this score (17)
    - MAX_ROUND: Maximum rounds before game ends (5)
    - STOP_CARD: Reshuffle when this many cards dealt (32)
    - strategies: Available bot strategies dictionary
    """

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)

        cls.MAX_PLAYERS = 6
        cls.BLACKJACK_PAYOUT = 1.5
        cls.DEALER_STAND_SCORE = 17
        cls.MAX_ROUND = 5
        cls.STOP_CARD = 32

        # Register available bot strategies
        cls.strategies = {
            "accurate": project.BlackJack.bot_strategy.AccurateStrategy(),
            "aggressive": project.BlackJack.bot_strategy.AggressiveStrategy(),
            "counting": project.BlackJack.bot_strategy.CountingStrategy(),
        }


class Game(metaclass=GameMeta):
    """
    Main Blackjack game controller class.

    Manages game state, player turns, betting, and rule enforcement.

    Attributes:
        deck (Deck): Game card deck
        players (List[Player]): List of active players
        counting_players (List[Bot]): List of card-counting bots
        dealer (Dealer): Game dealer
        bets (Dict[str, int]): Current round bets
        game_over (bool): Game completion flag
        round_count (int): Current round number
    """

    def __init__(self):
        """Initialize game with fresh deck and empty player list."""
        self.deck = project.BlackJack.deck.Deck()
        self.players: List[Player] = []
        self.counting_players: List[Bot] = []
        self.dealer = Dealer()
        self.bets: Dict[str, int] = {}
        self.game_over = False
        self.round_count = 0

    def add_player(self, player: Player) -> None:
        """
        Add a player to the game.

        Args:
            player (Player): Player instance to add

        Raises:
            ValueError: If maximum player limit reached
        """
        if len(self.players) >= self.MAX_PLAYERS:
            raise ValueError(f"Maximum number of players: {self.MAX_PLAYERS}")
        self.players.append(player)
        if isinstance(player, Bot) and isinstance(
            player.strategy, project.BlackJack.bot_strategy.CountingStrategy
        ):
            self.counting_players.append(player)

    def create_bot(self, strategy_name: str, bot_name: str, chips: int = 1000) -> Bot:
        """
        Create a new bot player with specified strategy.

        Args:
            strategy_name (str): Name of strategy ('accurate', 'aggressive', 'counting')
            bot_name (str): Name for the bot
            chips (int): Starting chip amount (default: 1000)

        Returns:
            Bot: New bot instance

        Raises:
            ValueError: If unknown strategy specified
        """
        strategy = self.strategies.get(strategy_name.lower())
        if strategy:
            return Bot(strategy, bot_name, chips)
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

    def shuffle(self) -> None:
        """Shuffle deck and reset card counters."""
        self.deck.shuffle()
        for c_player in self.counting_players:
            c_player.strategy.count = 0

    def start_round(self) -> None:
        """
        Start a new round by dealing initial cards.

        Reshuffles if needed, clears hands, deals 2 cards to each player,
        and 2 cards to dealer (one hidden).
        """
        if self.deck.count >= self.STOP_CARD:
            self.shuffle()

        # Clear all hands
        for player in self.players:
            player.hand = []
            player.score = 0
        self.dealer.hand = []
        self.dealer.score = 0

        # Deal initial cards
        for _ in range(2):
            for player in self.players:
                card = self.deck.get_card()
                player.get_card(card)
                player.calculate_score()
                self.counting(card)

            card = self.deck.get_card()
            if _ == 1:
                self.dealer.hide_card = card
            else:
                self.dealer.get_card(card)
                self.counting(card)

            self.dealer.calculate_score()

        self.game_over = False

    def place_bets(self) -> None:
        """Collect random bets from all players (10-100 chips)."""
        self.bets = {}
        for player in self.players:
            bet = random.randint(10, min(100, player.chips))
            bet_amount = player.place_bet(bet)
            self.bets[player.name] = bet_amount

    def play_turn(self, player: Player) -> None:
        """
        Process a player's turn.

        Args:
            player (Player): Player whose turn it is
        """
        if self.game_over:
            return

        if isinstance(player, Bot):
            while player.decide_hit():
                self.hit(player)
                self.print_table()

    def hit(self, player: Player) -> None:
        """
        Deal one card to player and update scores.

        Args:
            player (Player): Player receiving card
        """
        card = self.deck.get_card()
        player.get_card(card)
        player.calculate_score()

        self.counting(card)

    def play_dealer_turn(self) -> None:
        """Execute dealer's turn according to game rules."""
        # Reveal hidden card
        if self.dealer.hide_card:
            self.dealer.hand.append(self.dealer.hide_card)
            self.counting(self.dealer.hide_card)
            self.dealer.hide_card = None
            self.dealer.calculate_score()
            self.print_table()

        # Dealer hits until stand score reached
        while self.dealer.score < self.DEALER_STAND_SCORE and self.dealer.score <= 21:
            card = self.deck.get_card()
            self.dealer.get_card(card)
            self.counting(card)
            self.dealer.calculate_score()
            self.print_table()

        # End game if max rounds reached
        if self.MAX_ROUND == self.round_count:
            self.game_over = True

    def settle_bets(self, print_res: bool = True) -> None:
        """
        Settle all bets based on game outcome.

        Args:
            print_res (bool): Whether to print results (default: True)
        """
        dealer_score = self.dealer.score

        if print_res:
            print(f"Dealer: {dealer_score}")

        for player in self.players:
            bet = self.bets.get(player.name, 0)

            if player.score > 21:
                player.settle_bet(-bet)
                if print_res:
                    print(
                        f"{player.name}: {player.score} lost {bet} (overage). Chips number: {player.chips}"
                    )
                continue

            if dealer_score > 21:
                winnings = bet
                player.settle_bet(winnings)
                if print_res:
                    print(
                        f"{player.name}: {player.score} win {winnings} (dealer is overage). Chips number: {player.chips}"
                    )
                continue

            if (
                len(player.hand) == 2
                and player.score == 21
                and not (len(self.dealer.hand) == 2 and dealer_score == 21)
            ):
                winnings = int(bet * self.BLACKJACK_PAYOUT)
                player.settle_bet(winnings)
                if print_res:
                    print(
                        f"{player.name}: {player.score} win {winnings} (Black Jack). Chips number: {player.chips}"
                    )
                continue

            if player.score > dealer_score:
                winnings = bet
                player.settle_bet(winnings)
                if print_res:
                    print(
                        f"{player.name}: {player.score} win {winnings}. Chips number: {player.chips}"
                    )
            elif player.score == dealer_score:
                player.settle_bet(0)
                if print_res:
                    print(
                        f"{player.name}: {player.score} (draw). Chips number: {player.chips}"
                    )
            else:
                player.settle_bet(-bet)
                if print_res:
                    print(
                        f"{player.name}: {player.score} lost {bet}. Chips number: {player.chips}"
                    )

    def print_table(self) -> None:
        """Print current game state showing all hands."""
        for player in self.players:
            hand_str = " ".join(str(card) for card in player.hand)
            print(player.name + ": " + hand_str + "\n")

        hand_str = " ".join(str(card) for card in self.dealer.hand)
        print("Dealer: " + hand_str)
        print("____________")

    def counting(self, card: project.BlackJack.deck.Card) -> None:
        """Update card counts for counting strategy bots."""
        for c_player in self.counting_players:
            c_player.strategy.update_count(card)

    def change_bot_strategy(
        self, bot_name: str, strategy_name: str, print_res: bool = True
    ) -> None:
        """
        Change a bot's strategy during gameplay.

        Args:
            bot_name (str): Name of bot to modify
            strategy_name (str): New strategy name
            print_res (bool): Whether to print confirmation

        Raises:
            ValueError: If bot not found or unknown strategy
        """
        for player in self.players:
            if player.name == bot_name and isinstance(player, Bot):
                strategy = self.strategies.get(strategy_name.lower())
                if strategy:
                    player.strategy = strategy
                    if print_res:
                        print(f"Strategy {bot_name} changed to {strategy_name}")
                else:
                    raise ValueError(f"Unknown strategy: {strategy_name}")
                return
        raise ValueError(f"The bot was not found: {bot_name}")

    def modify_game_rule(self, rule_name: str, value, print_res: bool = True) -> None:
        """
        Dynamically modify a game rule.

        Args:
            rule_name (str): Rule to modify
            value: New value for rule
            print_res (bool): Whether to print confirmation

        Raises:
            ValueError: If unknown rule specified
        """
        if hasattr(self, rule_name):
            setattr(self, rule_name, value)
            if print_res:
                print(f"Rule {rule_name} changed to {value}")
        else:
            raise ValueError(f"Unknown game rule {rule_name}")

    def play_round(self, print_res: bool = True):
        """
        Play one complete round of Blackjack.

        Args:
            print_res (bool): Whether to print round progress
        """
        self.round_count += 1
        if print_res:
            print(f"\nRound {self.round_count}")
            print("________________________")
        self.place_bets()
        self.start_round()
        if print_res:
            self.print_table()

        for player in self.players:
            self.play_turn(player)

        self.play_dealer_turn()
        self.settle_bets()

    def play(self, print_res: bool = True) -> None:
        """
        Play complete game until completion.

        Args:
            print_res (bool): Whether to print game progress
        """
        self.shuffle()
        while not self.game_over:
            self.play_round(print_res)
