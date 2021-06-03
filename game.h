#include <vector>
#include <string>
#include <random>
#include <iostream>
#include <algorithm>
#include <ctime>

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
        Deck deck1;
        int cursor;
        Card tableCards[5];
        int button_player; // номер игрока из players
        int small_blind_player, big_blind_player; // тоже номера
        int game_limit_small_blind = 30; // просто константа для блайнда, потом поменяется
        int pot; // общий банк игры
        int player_action; // выбор игрока
        int player_bet; // новая ставка игрока
        int winner,roundWinner;
    public:
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
        void choose_dealer(){
            srand(time(0));
            button_player = rand() % players.size();
        }
        void choose_blinds_players(){
            small_blind_player = (button_player + 1) % players.size();
            big_blind_player = (button_player + 2) % players.size();
        } // DEBUG
        void print_blids_and_dealer(){
            std::cout << "Dealer: " << players[button_player].nickname << std::endl;
            std::cout << "Blinds are (sb/bb):" << std::endl;
            std::cout << players[small_blind_player].nickname << std::endl;
            std::cout << players[big_blind_player].nickname << std::endl;
        }
        void deal_cards(){
            for (int i=0; i < players.size(); i++){
                players[i].hand_cards[0] = deck1.take_card();
                players[i].hand_cards[1] = deck1.take_card();
            }
        } // DEBUG
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
};