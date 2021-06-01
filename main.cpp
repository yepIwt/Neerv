#include <iostream>
#include <string>
#include <vector>
#include "game.h"

int main(){
    Player p1(193802139012);
    p1.nickname = "yepIwt";
    std::vector<Card> deck = generate_deck();
    // for (Card c : deck){
    //     std::cout << "Card Info: " << c.cmd_view() << std::endl; 
    // }
    std::cout << "Player info: " << p1.nickname << std::endl;
    std::cout << "Player stack: " << p1.get_in_game_stack() << std::endl;  
    return 0;
}