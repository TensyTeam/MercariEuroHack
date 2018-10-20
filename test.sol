pragma solidity ^0.4.24;

contract mortal {
    address owner;

    event one (
        address indexed user,
        uint price
    );

    event Actions (
        address indexed user
    );

    constructor() public {
        owner = msg.sender;
    }

    function kill() public {
        if (msg.sender == owner) {
            selfdestruct(owner);
        }
    }
}

contract greeter is mortal {
    string greeting;

    constructor(string _greeting) public {
        greeting = _greeting;
    }

    function greet(address user, uint price) public constant returns (string) {
        emit one(user, price);
        return greeting;

        emit Actions(msg.sender);
    }
}