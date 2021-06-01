#include <vector>
#include <string>

const std::string cardsuits[4] = {"Черви","Вини","Буби","Крести"};
const std::string cardvalues[13] = {"2","3","4","5","6","7","8","9","10","Валет","Дама","Король","Туз"};

class Card{
    private:
        short cardsuit;
        short cardvalue;
        
    public:

        short suit(){
            return this->cardsuit;
        };

        short value(){
            return this->cardvalue;
        };

        std::string cmd_view(){
            return cardvalues[this->cardvalue] + " " + cardsuits[this->cardsuit];
        }
        
    Card() = default;
    Card(short new_suit, short new_value){
            this->cardsuit = new_suit;
            this->cardvalue = new_value;    
        };
};

std::vector<Card> generate_deck(){
    std::vector<Card> new_deck = {};
    for (short gen_value = 0; gen_value < 13; gen_value++){
        for (short gen_suit = 0; gen_suit < 4; gen_suit++){
            new_deck.push_back(Card(gen_suit, gen_value));
        } 
    }
    return new_deck;
}