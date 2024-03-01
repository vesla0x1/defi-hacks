The problem seems to be related to the rounding up in _repay

Lets simulate the transaction rounding up:
- initial:   totalBorrow: (0 97)
- borrow(1, true):    totalBorrow: (1 98)
- borrow(1, true):    totalBorrow: (2 196)
- repay(1, true):     totalBorrow: (1 195)
- borrow(1, true):    totalBorrow: (2 390)
- repay(1, true):     totalBorrow: (1 389)
- borrow(1, true):    totalBorrow: (2 778)
- repay(1, true):     totalBorrow: (1 777)
- borrow(1, true):    totalBorrow: (2 1554)
- repay(1, true):     totalBorrow: (1 1553)


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