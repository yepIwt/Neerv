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
        int folded_bets = 0; // Ticket 2: а почему бы не вектор от пары(ник,последняя ставка)?
        Deck deck1;
        int cursor;
        Card tableCards[5];
        int button_player; // номер игрока из players
        int small_blind_player, big_blind_player; // тоже номера
        int game_limit_small_blind = 30; // просто константа для блайнда, потом поменяется
        int player_action; // выбор игрока
        int player_bet; // новая ставка игрока
        int winner,roundWinner;
        int all_in_initiated = 0; // если кто-то пойдет ва-банк
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
            std::set<int> setted_bets(bets.begin(), bets.end());
            if (setted_bets.size() == 1)
                return true;
            return false;
        }
        bool all_in_completed(){ // Я не знаю как назвать эту функцию, для меня важен смысл функции
            // debug
            std::cout << "ALL_IN_COMPLETED RULE: ";
            for (int i=0; i < players.size(); i++){
                std::cout << bets[i] << " ";
            }
            std::cout << std::endl;
            
            // RULE
            for (int i=0; i < players.size(); i++){
                if (bets[i] == all_in_initiated){
                    continue;
                } else {
                    if (players[i].money == 0){
                        continue;
                    } else {
                        return false;
                    }
                }
            }
            return true;
        }
        void make_zero_bets(){
            for (int i=0; i < players.size(); i++)
                bets.push_back(0);
        }
        void add_player(std::string new_nickname, int new_stack){
            Player new_player; 
            new_player.in_game = true; new_player.money = new_stack; new_player.nickname = new_nickname;
            players.push_back(new_player);
        }
        std::string bet_small_blind(){
            players[small_blind_player].money -= game_limit_small_blind;
            bets[small_blind_player] += game_limit_small_blind;            
            return players[small_blind_player].nickname;
        }
        std::string bet_big_blind(){
            players[big_blind_player].money -= game_limit_small_blind * 2;
            player_bet = game_limit_small_blind * 2;
            bets[big_blind_player] += game_limit_small_blind * 2;
            cursor = player_next_to_player(big_blind_player);
            return players[big_blind_player].nickname;
        }
        void deal_cards(){
            for (int i=0; i < players.size(); i++){
                players[i].hand_cards[0] = deck1.take_card();
                players[i].hand_cards[1] = deck1.take_card();
            }
            make_zero_bets();
        }
        std::string get_dealer_nick(){
            return players[button_player].nickname;
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
        int calc_pot(){
            int pot=0;
            for (int bet : bets)
                pot += bet;
            pot += folded_bets;
            return pot
        }
        void print_players_stack(){
            std::cout << "In " << players[cursor].nickname <<"'s stack: ";
            std::cout << players[cursor].money << ". ";
        }
        int get_player_action(){
            std::cin >> player_action; // Ticket 1: Если ввести char, а не int, то случится ka-boom
            while (player_action != 1 && player_action != 2 && player_action != 3 && player_action != 4){
                std::cout << "Idk that action. pls correct your answer: ";
                std::cin >> player_action;
            }
            return player_action;
        }
        int ask_new_bet(){
            int new_player_bet=0;
            std::cin >> new_player_bet;
            while (new_player_bet > players[cursor].money || new_player_bet < player_bet){
                std::cout << "Eneter valid bet: "; std::cin >> new_player_bet;
            } 
            return new_player_bet;
        }
        bool ask_if_fold_whenever_all_in(){ // true = fold. false = all-ined
            std::cin >> player_action;
            while (player_action != 1 && player_action != 2){
                std::cout << "Are you nervous right now? Enter VALID action: ";
                std::cin >> player_action;
            }
            if (player_action == 1) {return true;} else {return false;}
        }
        // Просто действия пользователя в инфинитиве
        void bet(int howmch){
            bets[cursor] += howmch;
            players[cursor].money -= howmch;
        }
        void call(){
            bet(player_bet);
        }
        void fold(){
            folded_bets += bets[cursor];
            players.erase(players.begin() + cursor);
            bets.erase(bets.begin() + cursor);
            if (cursor >= players.size()){ cursor = 0; }
        }
        void all_in(){
            bets[cursor] += players[cursor].money;
            players[cursor].money = 0;
            all_in_initiated = bets[cursor];
        }
        //===========================================
        void player_bets(){
            int previous_bet = player_bet;
            std::cout << "Yor bank is " <<  players[cursor].money << "$. Enter new bet: ";
            player_bet = ask_new_bet();
            if (player_bet == players[cursor].money){
                player_signing_an_allin();
            } else {
                if (previous_bet == player_bet){
                    std::cout << players[cursor].nickname << " calls..."<< std::endl;
                } else {
                    std::cout << players[cursor].nickname << " bets " << player_bet << "..." << std::endl;
                }
            }
            bets[cursor] += player_bet;
            players[cursor].money -= player_bet;
            cursor = player_next_to_player(cursor);
        }
        void player_calls(){
            while (player_bet > players[cursor].money){
                std::cout << "You can't call. You don't have enough money!" << std::endl;
                print_players_stack();
                std::cout << "Do an action (1) Fold; (4) All-In";
                player_action = ask_if_fold_whenever_all_in();
            }

            bets[cursor] += player_bet;
            players[cursor].money -= player_bet;
            cursor = player_next_to_player(cursor);
        }
        void player_signing_an_allin(){
            std::cout << players[cursor].nickname << " all-ined..." << std::endl;
            bets[cursor] += players[cursor].money;
            all_in_initiated = bets[cursor];
            players[cursor].money = 0;
            //cursor = player_next_to_player(cursor);
        }
        void handle_player_action(){
            if (player_action == 1)
                fold();
            if (player_action == 2)
                player_bets();
            if (player_action == 3)
                call();
            if (player_action == 4)
                player_signing_an_allin();
        }
        void makeBets(){

            while (bets_are_equal() != true && all_in_initiated == 0){
                std::cout << "Last Bet: " << player_bet << "$" << std::endl;
                std::cout << "POT: " << calc_pot() << std::endl;
                print_players_stack();
                std::cout << "Do an action: (1) Fold ";
                if (player_bet >= players[cursor].money){
                    std::cout << "(4) All-In: ";
                } else { 
                    std::cout << "(2) Bet (3) Call: ";
                }
                player_action = get_player_action();
                handle_player_action();
            }

            while (all_in_completed() != true){
                std::cout << "===== ALL-IN GAME. ALL-IN BET: " << all_in_initiated << std::endl;
                print_pot();
                print_players_stack();
                std::cout <<  "Do an action: (1) Fold; (2) All-In: ";
                bool he_folds = ask_if_fold_whenever_all_in();
                if (he_folds){
                    fold();
                } else {
                    if ( (bets[cursor] + players[cursor].money) < all_in_initiated){ // если у него не хватает на олл-ин
                        bets[cursor] += players[cursor].money;
                        players[cursor].money = 0;
                    } else { // если у него хватает на олл-ин
                        players[cursor].money -= all_in_initiated - bets[cursor];
                        bets[cursor] += all_in_initiated - bets[cursor];
                    }
                    cursor = player_next_to_player(cursor);

                }
            }
        }
        void preflop(){
            makeBets();
            std::cout << std::endl << "All allined. so money: ";
            for (int i=0; i < players.size(); i++){
                std::cout << players[i].money << " ";
            } std::cout << std::endl;
        }
};
