pragma solidity ^0.6.0;

contract Lottery {
    address payable[] public players;

    function enter() public payable {
        // 50USD minimum
        players.push(msg.sender);
    }

    function getEntranceFee() public {}

    function startLottery() public {}

    function endLottery() public {}
}
