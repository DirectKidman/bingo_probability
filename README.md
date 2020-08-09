# Bingo の確率を求めるプログラム

これはビンゴでn個数字が出た時に、ビンゴが出る確率がどのくらいかを求めるプログラムです。
既存しているプログラムはみたことがないので、100％正しい保証はありません。

エラーがあれば教えてください。

## 使い方

```python
from bingo_prob import Bingo
bingo = Bingo(SIZE,RANGE)
```

ここでSIZEとは正方形の一辺の幅（初期値は5）
RANGEは一つの縦の列に入る数字の範囲（初期値は15）

実はビンゴの縦の列には入る数字の範囲が決まっていて、一番左側の列は1~15というようになっている。

## アルゴリズム

縦、横、斜めをbit全探索し、ビンゴになるかどうか組み合わせで判断。
包除原理を用いて重複したビンゴを除いてあります。
