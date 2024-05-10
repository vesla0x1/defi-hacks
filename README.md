# DeFi Hacks Playground
This is a playground for me to learn and practice smart contract security by replaying (in)famous Ethereum transactions, similar to [DeFi Hack Labs](https://github.com/SunWeb3Sec/DeFiHackLabs/). However, in this project my goal is not just to replay the transaction, but also to test fixes for the hack and explore the vulnerable contracts involved in the attack by cloning the original contracts and modifying their code. This allows me better understand each step of the transaction by creating logs and visualizing events in flexible manner.

## Structure
Each directory of this repository is a foundry project containing:
- **/test:** foundry test emulating the transaction (fork of [DeFi Hack Labs](https://github.com/SunWeb3Sec/DeFiHackLabs/) with some changes);

- **/src:** vulnerable contracts (and its dependencies) extracted from etherscan. These contracts must have their stated restored at the block that the hack happened (for now, I am using https://evm.storage but I plan to automate this in the future);

- **README.md:** write-up of the hack with mitigation steps;

- **branches:**
  - *playground:* explore, experiment and understand better the transaction using this branch. This can contain logs and useful notes. Feel free to change whatever you want here;
  - *fix:* mitigation steps for the hack. It's like if you could go back in time and change something in the vulnerable contract to avoid the hack to happen. 


## Summary
| Hack                      | Date          | Category        | Loss      | Write up                      | Fix patch                                                                                    |
|:-------------------------:|:-------------:|:---------------:|:---------:|:-----------------------------:|:--------------------------------------------------------------------------------------------:|
| [MiM Spell](./mim-spell/) | 2024/01/30    | Precision loss  | ~$6,5M    | [📝](./mim-spell/README.md)  | [🛠️](https://github.com/vesla0x1/defi-hacks/commit/ab6bc9b7f43cd3f45496a47b3e4038bb79e9bf58) |



## Usage
You need to have git and [foundry](https://book.getfoundry.sh/getting-started/installation) installed.

Clone this repository to your local machine:
```
git clone https://github.com/vesla0x1/defi-hacks.git
```

Enter in a sub-directory containing an attack:
```
cd mim-spell
```

Change to a branch and play around:
`git checkout <playground|fix>`

Run test:
```
forge test -vv
```

## Support me
If this supported you, I would appreciate if you could support me as well by sending some crypto to `0xb49d817A0Ee1bfDBb9cb0b2599eFf01f6cE18E13`.
