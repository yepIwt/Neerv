#include <iostream>
#include <string>
#include <vector>
#include "game.h"

using std::cin;  using std::cout;  using std::endl;

int main(){
    cout << "Neerv is a nervous poker game. Take care of your nerves! " << endl << endl;
    Game poker;
    
    // Registration of players
    std::string new_player_name;
    unsigned long int new_player_stack;
    short players_count = 0;
    while (players_count != 5){
        cout << "What name do you want to take? "; cin >> new_player_name;
        cout << new_player_name << ", how much money can you spend in this game? "; cin >> new_player_stack;
        poker.add_player(new_player_name, new_player_stack);
        cout << "Added! " << endl << endl;
        players_count++;
    };
    cout << "OK. Let's start our game... " << endl << endl;

    // Take a button
    poker.choose_dealer();
    // Choose small blind and big blind
    poker.choose_blinds_players();
    poker.print_dealer();
    
    // Deal 2 hand cards
    cout << "Now you got hand cards!" << endl;
    poker.deal_cards();

    cout << poker.bet_small_blind() << " posts the small blind..." << endl;
    cout << poker.bet_big_blind() << " posts the big blind..." << endl;

    //cout << "Setting"
    // Start preflop
    poker.preflop();
    
    

    return 0;
}