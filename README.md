# DeFi Hacks Playground
This repository aims to recreate (in)famous Ethereum transactions, similar to [DeFi Hack Labs](https://github.com/SunWeb3Sec/DeFiHackLabs/). However, it differs by not only recreating the transaction but also by providing a way to interact with vulnerable contracts. This allows to gain a better understanding of each step in the transaction's execution by creating logs and visualizing events in a flexible manner. In addition to this, another goal of this project is to provide a mechanism to modify vulnerable contracts, with the goal to mitigate the root cause of the issue and prevent hack to happen. Comprehensive write-ups of these hacks will also be included.

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
| [MiM Spell](./mim-spell/) | 2024/01/30    | Rounding error  | ~$6,5M    | [📝](./mim-attack/README.md)  | [🛠️](https://github.com/vesla0x1/defi-hacks/commit/bba00fd2666ffc00f9def56cd3e71e769249dcdc) |



## Usage
You need to have git and [foundry](https://book.getfoundry.sh/getting-started/installation) installed.

Clone this repository to your local machine:
`git clone https://github.com/vesla0x1/defi-hacks.git`

Enter in a sub-directory containing an attack:
`cd mim-spell`

Change to a branch and play around:
`git checkout <playground|fix>`

Run test:
`forge test -vv`

## Support me
If this supported you, I would appreciate if you could support me as well by sending some crypto to `0xb49d817A0Ee1bfDBb9cb0b2599eFf01f6cE18E13`.