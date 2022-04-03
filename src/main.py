import pandas
import sys
import matplotlib.pyplot as plot

# python3 main.py ./d1rn4jl998v.csv のようにして使う
def main():
    # Pandas で使いやすいデータに変換する
    data_frame = create_data_frame_from_csv()

    getTime = "getTime"
    # コメントされた時間を集計しやすい形に変換
    data_frame[getTime] = convert_data_time(data_frame, getTime)
    # 1 分毎のコメント数を集計する
    count = data_frame.groupby(pandas.Grouper(key=getTime, freq="1min")).count().reset_index()

    comment = "message"
    # 枠内で 1 分間にされた最大コメント数
    max_comment = count[comment].max()

    # グラフの横軸の為に行数分のデータタイムインデックスを作成
    x, y = create_coordinates(count, comment)

    create_graph(x, y)
    

def create_data_frame_from_csv():
    csv_path = sys.argv[1]
    # CSV を DataFrame として読み込む
    data_frame = pandas.read_csv(csv_path, encoding="utf_8")
    return data_frame


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