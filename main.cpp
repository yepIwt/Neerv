#include <iostream>
#include <string>
#include <vector>
#include "game.h"


int main(){
    Player p1(193802139012);
    p1.nickname = "yepIwt";
    Deck deck;
    deck.shuffle();
    deck.cmd_print();
    Card a = deck.take_card();
    Card b = deck.take_card();
    Card c = deck.take_card();
    std::cout << cardvalues[a.value] << cardsuits[a.suit] << std::endl; 
    std::cout << cardvalues[b.value] << cardsuits[b.suit] << std::endl;
    std::cout << cardvalues[c.value] << cardsuits[c.suit] << std::endl;
    // for (Card c : deck){
    //     std::cout << "Card Info: " << c.cmd_view() << std::endl; 
    // }
    
    std::cout << "Player info: " << p1.nickname << std::endl;
    std::cout << "Player stack: " << p1.get_in_game_stack() << std::endl;  
    return 0;
}