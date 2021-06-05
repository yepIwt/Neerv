#include <vector>
#include <string>
#include <random>
#include <iostream>
#include <algorithm>
#include <ctime>
#include <set>
const std::string cardsuits[4] = {"Черви","Вини","Буби","Крести"};
const std::string cardvalues[13] = {"2","3","4","5","6","7","8","9","10","Валет","Дама","Король","Туз"};

class Card{
    public:
    int suit;
    int value;
};

class Deck{
    private:
        Card cards[52];
        int top;
    public:
        void shuffle(){
            this->top = 51; // Защита от неперемешаннной колоды
            srand(time(0)); // Фикс бага при компиляции задается единый сид рандома
            std::random_shuffle(std::begin(this->cards), std::end(this->cards));
        }
        void cmd_print(){
            for (int i=0;i<52;i++)
                std::cout << cardvalues[cards[i].value] << cardsuits[cards[i].suit] << std::endl;
            std::cout << std::endl;
        }
        Card take_card(){
            this->top--;
            return this->cards[this->top+1];
        }
        Deck(){
            for (int i=0;i<4;i++){
                for (int j=0;j<13;j++){
                    cards[i*13+j].suit = i;
                    cards[i*13+j].value = j;
                }
            }
            shuffle();
        }
};

class Player{
    public:
        std::string nickname;
        unsigned long int money; // $
        Card hand_cards[2] = {};
        bool in_game=false;
        int move; //round
        int thinks;
};

class Game{
    private:
        std::vector<Player> players;
        std::vector<int> bets{};
        Deck deck1;
        int cursor;
        Card tableCards[5];
        int button_player; // номер игрока из players
        int small_blind_player, big_blind_player; // тоже номера
        int game_limit_small_blind = 30; // просто константа для блайнда, потом поменяется
        int pot=0; // общий банк игры
        int player_action; // выбор игрока
        int player_bet; // новая ставка игрока
        int winner,roundWinner;
    public:
        //Instruments
        void choose_dealer(){
            srand(time(0));
            button_player = rand() % players.size();
        }
        void choose_blinds_players(){
            small_blind_player = player_next_to_player(button_player);
            big_blind_player = player_next_to_player(small_blind_player);
        }
        int player_next_to_player(int next_to){
            return (next_to + 1) % players.size();
        }
        bool bets_are_equal(){
            std::set<int> setted_bets(this->bets.begin(), this->bets.end());
            if (setted_bets.size() == 1){
                return true;
            } else {
                return false;
            }
        }
        void make_zero_bets(){
            for (int i=0; i < players.size(); i++){
                bets.push_back(0);
            }
        }
        //Gameplay
        bool add_player(std::string new_nickname, unsigned long int new_stack){
            bool player_sat_down  = false;
            if (players.size() != 6){
                Player new_player; 
                new_player.in_game = true; new_player.money = new_stack; new_player.nickname = new_nickname;
                players.push_back(new_player);
                player_sat_down = true;
            }
            return player_sat_down;
        }
        std::string bet_small_blind(){
            pot += game_limit_small_blind;
            players[small_blind_player].money -= game_limit_small_blind;

            bets[small_blind_player] += game_limit_small_blind;
            
            return players[small_blind_player].nickname;
        }
        std::string bet_big_blind(){
            pot += game_limit_small_blind * 2;
            players[big_blind_player].money -= game_limit_small_blind * 2;
            cursor = player_next_to_player(big_blind_player);
            player_bet = game_limit_small_blind * 2;
            
            bets[big_blind_player] += game_limit_small_blind * 2;

            return players[big_blind_player].nickname;
        }
        void deal_cards(){
            for (int i=0; i < players.size(); i++){
                players[i].hand_cards[0] = deck1.take_card();
                players[i].hand_cards[1] = deck1.take_card();
            }
            make_zero_bets();
        }
        void print_dealer(){
            std::cout << "Button: " << players[button_player].nickname << std::endl << std::endl;
            //std::cout << "SB/BB: " << players[small_blind_player].nickname << " ";
            //std::cout << players[big_blind_player].nickname << std::endl << std::endl;
        }
        void print_hand_cards(){
            for (int i=0; i < players.size(); i++){
                std::cout << players[i].nickname << " cards: ";
                std::string hand_card_names = cardsuits[players[i].hand_cards[0].suit];
                std::string hand_card_value = cardvalues[players[i].hand_cards[0].value];

                std::string hand_card_names1 = cardsuits[players[i].hand_cards[1].suit];
                std::string hand_card_value1 = cardvalues[players[i].hand_cards[1].value];

                std::cout << hand_card_value << hand_card_names << " " << hand_card_value1 << hand_card_names1 << std::endl;
            }
        }
        void print_last_bet(){
            std::cout << "LastBet is " << player_bet << std::endl;
        }
        int get_player_action(){
            std::cin >> player_action; // Ticket 1: Если ввести char, а не int, то случится ka-boom
            while (player_action != 1 && player_action != 2 && player_action != 3){
                std::cout << "Idk that action. pls correct your answer: ";
                get_player_action();
            }
            return player_action;
        }
        void makeBets(){
            while (bets_are_equal() != true){
                print_last_bet();
                std::cout << players[cursor].nickname << ", do an action: (1) Fold; (2) Bet; (3) Call: ";
                player_action = get_player_action();
                std::cout << "Player action is " << player_action;
                //scursor = player_next_to_player(cursor);
            }
        }
        void preflop(){
            makeBets();
            //while (bets_are_equal() != true)
        }
};