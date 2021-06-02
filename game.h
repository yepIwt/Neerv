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
        }
};

class Player{
    public:
        std::string nickname;
        unsigned long int money; // $
        Card hand_cards[2];
        bool in_game=false;
        int move; //round
        int thinks;
};

class Game{
    private:
        Player players[6];
        Deck deck;
        int cursor;
        Card tableCards[5];
        int pot; // общий банк игры
        int player_action; // выбор игрока
        int player_bet; // новая ставка игрока
        int winner,roundWinner;
    public:
        bool add_player(std::string new_nickname, unsigned long int new_stack){
            bool player_sat_down  = false;
            for (int i=0; i < 6; i++){
                if (players[i].in_game != true){ // Есть свободное место?
                    players[i].nickname = new_nickname; players[i].money = new_stack;
                    players[i].in_game = true;
                    player_sat_down = true;
                }
            }
            return player_sat_down;
        }

};