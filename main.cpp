#include <iostream>
#include <string>
#include <vector>
#include "game.h"


int main(){
    std::cout << "Neerv is a nervous poker game. Take care of your nerves! " << std::endl << std::endl;
    
    Game poker;
    std::string new_player_name;
    unsigned long int new_player_stack;
    short players_count = 0;
    while (players_count != 5){
        std::cout << "What name do you want to take? "; std::cin >> new_player_name;
        std::cout << new_player_name << ", how much money can you spend in this game? "; std::cin >> new_player_stack;
        poker.add_player(new_player_name, new_player_stack);
        std::cout << "Added! " << std::endl << std::endl;
        players_count++;
    };
    std::cout << "OK. Let's start our game... " << std::endl << std::endl;    
    return 0;
}