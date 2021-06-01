#include <iostream>
#include <string>
#include <vector>
#include "game.h"

int main(){
    std::vector<Card> deck = generate_deck();
    for (Card c : deck){
        std::cout << "Card Info: " << c.cmd_view() << std::endl; 
    }
    return 0;
}