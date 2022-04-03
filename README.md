## ライブラリ

pandas, matplotlib を利用している。  

## どのようにして CSV から 1 分辺りのコメント量を求めるのか？
Python の Pandas を用いると出来る。  
Pandas を利用すると文字列になっている時間を、日付データに変換することが出来る。  
Pandas の to_datetime() 関数を用いることで datetime 型になり、これが実現出来る。  
関数内で日付を表すフォーマットを指定する必要がある。  
コメントの時間に関しては、例として **2022-03-27T18:17:57+09:00** と保存されている。  
これは ISO 8601 と呼ばれる規格の JST と呼ばれるタイムゾーンらしい。  
これを Pandas で使うには、フォーマットを自分で作成し、パーサーを利用する必要がある？  
パーサーを用いると、Grouper() で 1 分間のコメント数にまとめることが出来る。  

## 1 分ごとのコメント数に集計する

**pandas.Grouper()** 関数を用いる。  

例  
```py
df.groupby(pd.Grouper(key='date', freq='1min')).count().reset_index()
```