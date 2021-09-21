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
    modifier can_buy_hadcoins(uint usd_invested) {
        require (usd_invested * usd_to_hadcoins + total_hadcoins_bought <= max_hadcoins);
        _;
    }

}