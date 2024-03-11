# MiM Spell Attack

## 1. Root cause
### TL;DR
The root cause of the attack was a precision loss introduced by a rounding error in [`CauldronV4.sol::_repay`](https://github.com/vesla0x1/defi-hacks/blob/master/mim-spell/src/CauldronV4.sol#L396-L407), when [`toElastic`](https://github.com/boringcrypto/BoringSolidity/blob/78f4817d9c0d95fe9c45cd42e307ccd22cf5f4fc/contracts/libraries/BoringRebase.sol#L28-L41) is calculated. [`toElastic`](https://github.com/boringcrypto/BoringSolidity/blob/78f4817d9c0d95fe9c45cd42e307ccd22cf5f4fc/contracts/libraries/BoringRebase.sol#L28-L41) is evaluated as `x = (part * totalBorrow.elastic) / totalBorrow.base` and in order to handle the precision loss caused by the division, it rounds up favoring the protocol. However, when (part * totalBorrow.elastic) < totalBorrow.base, rounding up will cause `toElastic` to be always evaluated to 1, violating the invariant of the exchange rate (`totalBorrow.elastic` / `totalBorrow.base`) before repayments $e$, being approximately the exchange rate after, $e'$.

Let $e$ = 2:196 (0.0102); [`CauldronV4.sol::repay`](https://github.com/vesla0x1/defi-hacks/blob/master/mim-spell/src/CauldronV4.sol#L415-L422) is called with `part` = 1; `toElastic(1)` is evaluated as 1 ((1 * 2) / 196 => 0 truncation => 1 round up); exchange rate $e'$ is calculated as `totalBorrow.elastic` = 2 - 1, `totalBorrow.base` = 196 - 1. Therefore, $e'$ = 1:195 (0.0051), $e' \approx \frac{e}{2}$, violating $e' \approx e$.

The impact of this rounding error is that it made possible to bypass the health check in [`CauldronV4.sol#L272`](https://github.com/vesla0x1/defi-hacks/blob/master/mim-spell/src/CauldronV4.sol#L272) to borrow (and withdraw) all MiM tokens in Degenbox for a very small collateral amount. This became possible by increasing `totalBorrow.base` to (almost) infinity, while keeping `totalBorrow.elastic` at 1. This  was achieved by repeatedly calling [`borrow`](https://github.com/vesla0x1/defi-hacks/blob/master/mim-spell/src/CauldronV4.sol#L390-L393) and [`repay`](https://github.com/vesla0x1/defi-hacks/blob/master/mim-spell/src/CauldronV4.sol#L415-L422) with small `part` amounts.

### Full explanation
[`CauldronV4.sol::_repay`](https://github.com/vesla0x1/defi-hacks/blob/master/mim-spell/src/CauldronV4.sol#L396-L407) is meant to subtract an amount of elastic and base shares from `totalBorrow` (see [`CauldronV4.sol#L401`](https://github.com/vesla0x1/defi-hacks/blob/master/mim-spell/src/CauldronV4.sol#L401) and [`BoringRebase.sol::sub`](https://github.com/boringcrypto/BoringSolidity/blob/78f4817d9c0d95fe9c45cd42e307ccd22cf5f4fc/contracts/libraries/BoringRebase.sol#L60-L69)). It receives `part` as [argument](https://github.com/vesla0x1/defi-hacks/blob/master/mim-spell/src/CauldronV4.sol#L399), which is an amount in base shares. In order to subtract an amount of `elastic` shares from `totalBorrow.elastic`, the given argument (`part`) has first to be converted to elastic shares. This is done in [`BoringRebase::toElastic`](https://github.com/boringcrypto/BoringSolidity/blob/78f4817d9c0d95fe9c45cd42e307ccd22cf5f4fc/contracts/libraries/BoringRebase.sol#L28-L41) and this is the moment when the issue occurs, as we are going to see in a while. 

Converting base to elastic is calculating $x$ in the equation below:

$$\begin{align*}
totalBorrow.elastic & \to totalBorrow.base \\
x & \to part
\end{align*}
$$

Therefore,

$$
x = \frac{(part \times totalBorrow.elastic)}{totalBorrow.base}
$$

As we can see, the division to `totalBorrow.base` in the equation above, introduces some precision loss. The protocol addresses this by rounding up the result, benefiting itself. Let's suppose `totalBorrow.elastic` = 135 and `totalBorrow.base` = 50. If someone wants to repay 1 borrowed `base` share, 2.7 `elastic` would be charged (2 due to truncation), but since the protocol rounds in its favor, it rounds up to 3:
```python
repay(1) {'elastic': 135, 'base': 50}
 - toElastic(1, True) => (1 * 135) / 50 => 2.7 => 2
   - roundUp: (2 * 50) / 135 < 1               => True
 - return => 3
totalBorrow: {'elastic': 132, 'base': 49} # @> after the conversion, 1 base and 3 elastic shares are discounted.
```
This works well when `totalBorrow.elastic` >= `totalBorrow.base` because, as we can see in the equation above, the division `totalBorrow.elastic` / `totalBorrow.base` will always result in `x` >= 1 (remember, `totalBorrow.base` < `totalBorrow.elastic`).

However, when `totalBorrow.elastic` < `totalBorrow.base`, the rounding up does not work as expected. To understand better let's see an example using the `elastic` and `base` values observed in the MiM attack:
```python
repay(1) {'elastic': 2, 'base': 196} # @> original ratio 1:98
 - toElastic(1, True) => (1 * 2) / 196 => 0.0102 => 0
   - roundUp: (0 * 196) / 2 < 1                  => True
 - return => 1
totalBorrow: {'elastic': 1, 'base': 195} # @> final ratio 1:195
```

In the example, `elastic` = 2 and `base` = 196 (1 `elastic` => 98 `base`). If someone wants to repay 1 borrowed `base`, 2 / 196 = 0.0102 `elastic` should be charged. Since 0.0102 < 1 it rounds up to 1, resulting in 1 `base` = 1 `elastic` and that is the root cause of the attack. To decrease 1 `elastic` from `totalBorrow`, 98 `base` should have been paied, but due to the rounding error 1 `elastic` could be discounted for only 1 `base`, (almost) halving the original ratio `elastic`:`base` from 1:98 to 1:195.

Then, if someone wants to borrow assets, a given [`amount`](https://github.com/vesla0x1/defi-hacks/blob/master/mim-spell/src/CauldronV4.sol#L390C33-L390C47), in `elastic` shares, should be converted to `base` shares (1 `elastic` => 195 `base`) and these values are added to `totalBorrow`, making `elastic` = 2, as initially and `base` = 390, being the double (minus 2) of its initial value (196): 
```python
borrow(1) {'elastic': 1, 'base': 195}
 - toBase(1, True) => (1 * 195) / 1 => 195
   - roundUp: (195 * 1) / 195 < 1    => False
 - return => 195
totalBorrow: {'elastic': 2, 'base': 390} # @> base has doubled while elastic stills unchanged
```

The attacker exploited this issue by calling `borrow` and `repay` with a small amount multiple times, increasing `base` shares exponentially, while keeping `elastic` shares 1:
```
initial    => {elastic: 1, base: 98}
borrow(1)  => {elastic: 2, base: 196}
repay(1)   => {elastic: 1, base: 195}
borrow(1)  => {elastic: 2, base: 390}
repay(1)   => {elastic: 1, base: 389}
borrow(1)  => {elastic: 2, base: 778}
repay(1)   => {elastic: 1, base: 777}
borrow(1)  => {elastic: 2, base: 1554}
repay(1)   => {elastic: 1, base: 1553}
...
after calling borrow(1) and repay(1) 90 times
...
repay(1)   => {elastic: 1, base: 60040091905340943332607524865}
borrow(1)  => {elastic: 2, base: 120080183810681886665215049730}
final      => {elastic: 1, base: 120080183810681886665215049729}
```

Since the amount of `base` shares of MiM had increased to (almost) infinity, the entire balance of MiM tokens in Degenbox (5.000.047 when the attack happened) was negligible in comparison this amount of `totalBorrow.base`. This made possible the attacker to bypass the health check in [`CauldronV4.sol#L272`](https://github.com/vesla0x1/defi-hacks/blob/master/mim-spell/src/CauldronV4.sol#L272), since the division for [`totalBorrow.base`](https://github.com/vesla0x1/defi-hacks/blob/master/mim-spell/src/CauldronV4.sol#L272C71-L272C88) will always result in zero and the attacker was able to borrow (and withdraw) all MiM tokens in Degenbox for a very low collateral amount, using another account, causing ~$6.5M loss to the protocol.

## 2. Mitigation
As discussed, the root cause of the problem was a rounding error in [`CauldronV4.sol::_repay`](https://github.com/vesla0x1/defi-hacks/blob/master/mim-spell/src/CauldronV4.sol#L401), introduced when [`BoringRebase.sol::toElastic`](https://github.com/boringcrypto/BoringSolidity/blob/78f4817d9c0d95fe9c45cd42e307ccd22cf5f4fc/contracts/libraries/BoringRebase.sol#L36) is calculated:

$$
x = \frac{(part \times totalBorrow.elastic)}{totalBorrow.base}
$$

This rounding error occurs if (`part` * `totalBorrow.elastic`) < `totalBorrow.base`. Therefore, assuring (`part` * `totalBorrow.elastic`) >= `totalBorrow.base` in [`CauldronV4.sol::_repay`](https://github.com/vesla0x1/defi-hacks/blob/master/mim-spell/src/CauldronV4.sol#L395-L408) should do the [fix](https://github.com/vesla0x1/defi-hacks/blob/fix/mim-spell/src/CauldronV4.sol#L401):

```diff
 // File: CauldronV4.sol
 395:     /// @dev Concrete implementation of `repay`.
 396:     function _repay(
 397:         address to,
 398:         bool skim,
 399:         uint256 part
 400:     ) internal returns (uint256 amount) {
+401:         require(part * totalBorrow.elastic >= totalBorrow.base, "Part amount is not enough to repay.");
 402:         (totalBorrow, amount) = totalBorrow.sub(part, true);
 403:         userBorrowPart[to] = userBorrowPart[to].sub(part);
 404: 
 405:         uint256 share = bentoBox.toShare(magicInternetMoney, amount, true);
 406:         bentoBox.transfer(magicInternetMoney, skim ? address(bentoBox) : msg.sender, address(this), share);
 407:         emit LogRepay(skim ? address(bentoBox) : msg.sender, to, amount, part);
 408:     }
```
