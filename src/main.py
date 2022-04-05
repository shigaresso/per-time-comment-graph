import sys
# プログラム実行時に __pycache__ を作らないようにする
sys.dont_write_bytecode = True

import pandas
import matplotlib.pyplot as plot
import config


# python3 main.py ./d1rn4jl998v.csv のようにして使う
def main():
    # Pandas で使いやすいデータに変換する
    data_frame = create_data_frame_from_csv()

    # コメントされた時間を集計しやすい形に変換
    data_frame[config.getTime] = convert_data_time(data_frame, config.getTime)

    # 検索ワードを入れている場合、検索ワードのみでグラフを作成する
    data_frame = comment_search(data_frame, config.comment, config.search_word)

    # ターミナルに検索ワードが書かれている時間を表示
    search_word_screen_terminal(data_frame, config.getTime, config.comment)

    # 1 分毎のコメント数を集計する
    count = data_frame.groupby(pandas.Grouper(key=config.getTime, freq="1min")).count().reset_index()
    # グラフの横軸の為に行数分のデータタイムインデックスを作成
    x, y = create_coordinates(count, config.comment)

    create_graph(x, y)

def search_word_screen_terminal(data_frame, getTime, comment):
    # NaN 部分を削除し、1分毎にまとめる
    print_frame = data_frame.dropna().groupby(pandas.Grouper(key=getTime, freq="1min")).count()
    # コメントの部分が 0 の行は削除する
    print(print_frame[print_frame[comment] != 0])


def create_data_frame_from_csv():
    csv_path = sys.argv[1]
    # CSV を DataFrame として読み込む
    data_frame = pandas.read_csv(csv_path, encoding="utf_8")
    return data_frame


def comment_search(data_frame, comment, search_word):
    if (search_word):
        searched_frame = data_frame[data_frame[comment].str.contains(search_word, na=True)]
    else:
        searched_frame = data_frame
    return searched_frame
    

def convert_data_time(data_frame, getTime):
    # datetime 型にするためには時間のフォーマットを指定する必要がある
    format = "%Y-%m-%dT%H:%M:%S+09:00"
    # 時刻を datetime 型に変換する
    return pandas.to_datetime(data_frame[getTime], format=format)


def create_coordinates(count, comment):
    # x 座標の配列を用意
    x = list(range(len(count)))
    # y 座標の配列を用意
    y = count[comment].tolist()
    return x, y

def create_graph(x, y):
    # グラフを描画
    plot.plot(x, y, "o-")
    plot.xlabel("time")
    plot.ylabel("comment")
    # グラフの表示
    plot.show()

main()