import math
import simplekml
import xml.etree.ElementTree as ET

def generate_parabolic_kml(start_lat, start_lon, end_lat, end_lon, height, num_points, output_file):
    kml = simplekml.Kml()

    path_coords = []
    for i in range(num_points + 1):
        t = i / num_points
        lat = start_lat + (end_lat - start_lat) * t
        lon = start_lon + (end_lon - start_lon) * t
        alt = 4 * height * (t - t**2)  # 放物線の高さ
        path_coords.append((lon, lat, alt))  # タプルのリストを使用

    # KML に座標を追加
    linestring = kml.newlinestring(name="Parabolic Path")
    linestring.coords = path_coords  # 文字列ではなくタプルのリストを渡す
    linestring.altitudemode = simplekml.AltitudeMode.absolute

    # KMLファイルを一旦保存
    temp_file = "temp.kml"
    kml.save(temp_file)

    # KMLのXMLを読み込んで `coordinates` に改行を追加
    tree = ET.parse(temp_file)
    root = tree.getroot()

    for coord in root.findall(".//{http://www.opengis.net/kml/2.2}coordinates"):
        text = coord.text.strip()
        formatted_text = "\n".join(text.split())  # 改行を追加
        coord.text = "\n" + formatted_text + "\n"

    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    
    print(f"KMLファイル '{output_file}' を生成しました（coordinates の改行済み）")

# サンプルデータ
start_lat, start_lon = 35.0, 135.0   # 開始位置
end_lat, end_lon = 35.5, 135.5       # 終了位置
height = 5000                        # 最大高さ
num_points = 50                      # 軌道の分割数
output_file = "parabolic_path.kml"   # 出力ファイル名

generate_parabolic_kml(start_lat, start_lon, end_lat, end_lon, height, num_points, output_file)

'''
■AIやり取り
①開始位置と終了位置の緯度経度を指定して放物線上のPATHを描いたKMLを生成するプログラムのサンプルを提示して。

②coordinatesの可読性を上げるため改行を入れるように修正して

simplekml の coords は リスト である必要があり、改行を追加するには KML の coordinates を直接編集する必要があります。
修正するには、linestring.coords に タプルのリスト を渡し、KML の XML 文字列を編集して coordinates 要素に改行を追加する方法を使います。
修正ポイント:
- linestring.coords にタプルのリストを渡す → simplekml はリスト構造を期待しているので、文字列ではなくリストを使う。
- xml.etree.ElementTree を使って coordinates 要素を改行 → ET.parse() でKMLを解析し、coordinates の値を修正して改行を追加。

'''
