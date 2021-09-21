// ICO Hadcoins

/*
 Run on http://remix.ethereum.org/#appVersion=0.7.7&optimize=false&version=soljson-v0.4.11+commit.68ef5810.js
 MyEtherWaller == 3.11.2.4
*/


// version
pragma solidity ^0.4.11

contract hadcoin_ico {
    // max number of hadcoins available in ICO
    uint public max_hadcoins = 1000000;

    // dolar cost
    uint public usd_to_hadcoins = 1000;

    // total hadcoins bought by investors
    uint public total_hadcoins_bought = 0;

    // equivalence functions
    mapping(address => uint) equity_hadcoins;
    mapping(address => uint) equity_usd;

    // checking if investor can buy hadcoins
    // modifiers can only be accessed by functions
    modifier can_buy_hadcoins(uint usd_invested) {
        require (usd_invested * usd_to_hadcoins + total_hadcoins_bought <= max_hadcoins);
        _;
    }

    // returns investment value in hadcoins
    function equity_in_hadcoins(address investor) external constant returns(uint) {
        return equity_hadcoins[investor];
    }

    // returns investment value in dollars
    function equity_in_usd(address investor) external constant returns(uint) {
        return equity_usd[investor];
    }

    // buying hadcoins
    function buy_hadcoins(address investor, uint usd) external
    can_buy_hadcoins(usd_invested) {
        uint hadcoins_bought = usd_invested * usd_to_hadcoins;
        equity_hadcoins[investor] += hadcoins_bought;
        equity_usd[investor] = equity_hadcoins[investor] / 1000;
        total_hadcoins_bought += hadcoins_bought;
    }

}