The problem seems to be related to the rounding up in _repay

Lets simulate the transaction rounding up:
- initial:   totalBorrow: (0 97)
- borrow(1, true):    totalBorrow: (1 98) 
- borrow(1, true):    totalBorrow: (2 196) -> 1 * 98 / 1 (98) -> 98 (calculating shares; incremenet 1 from elastic)
- repay(1, true):     totalBorrow: (1 195) -> (need to calculate elastic shares from 1 base share) -> 196 -> 2 => 2 / 196 => 1 / 98 => 0.01020 (0) -> round up -> 1
- borrow(1, true):    totalBorrow: (2 390)
- repay(1, true):     totalBorrow: (1 389)
- borrow(1, true):    totalBorrow: (2 778)
- repay(1, true):     totalBorrow: (1 777)
- borrow(1, true):    totalBorrow: (2 1554)
- repay(1, true):     totalBorrow: (1 1553)

(elastic * total.base) / total.elastic; -> 1 * 98 / 90 (1.088) -> round up -> 2
(base * total.elastic) / total.base -> 0 * 91 / 100 (0) -> 1

- borrow(1, true):    totalBorrow: (90 98)
- borrow(1, true):    totalBorrow: (91 100)
- repay(0, true):     totalBorrow: (90 99) -> 91 -> 100 => 1 share = 91 / 100 => 0.91 (0) -> round up -> 1

- borrow(1, true):    totalBorrow: (10 98)
- borrow(1, true):    totalBorrow: (11 108)
- repay(0, true):     totalBorrow: (10 107) -> 11 -> 108 => 1 share = 11 / 108 => 0.1 (0) -> round up -> 1


- repay(0, false):     totalBorrow: (11 107) -> 11 -> 108 => 1 share = 11 / 108 => 0.1 (0) -> round up -> 0
- repay(0, false):     totalBorrow: (11 106) -> 11 -> 108 => 1 share = 11 / 108 => 0.1 (0) -> round up -> 0
...
- repay(0, false):     totalBorrow: (11 11) -> 11 -> 108 => 1 share = 11 / 108 => 0.1 (0) -> round up -> 0



and now without rounding up:
- initial:   totalBorrow: (0 97)
- borrow(1, true):    totalBorrow: (1 98)
- borrow(1, true):    totalBorrow: (2 196)
- repay(1, false):    totalBorrow: (2 195)
- borrow(1, true):    totalBorrow: (3 293)
- repay(1, false):    totalBorrow: (3 292)
- borrow(1, true):    totalBorrow: (4 390)
- repay(1, false):    totalBorrow: (4 389)
- borrow(1, true):    totalBorrow: (5 487)
- repay(1, false):    totalBorrow: (5 486)