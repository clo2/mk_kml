import math
import simplekml

def create_sphere_surface_kml(center_lat, center_lon, center_alt, radius, segments=20):
    # KMLオブジェクトを作成
    kml = simplekml.Kml()
    
    # 球の中心座標（緯度、経度、高度）
    # radius: 球の半径（メートル）
    # segments: 球の分割数（緯度・経度の分割数）

    # 球の表面をポリゴンで近似
    for i in range(segments):
        for j in range(segments):
            # ポリゴンの4つの頂点を計算
            lat1 = center_lat + (radius / 111320) * math.cos(math.pi * i / segments) * math.cos(2 * math.pi * j / segments)
            lon1 = center_lon + (radius / (111320 * math.cos(math.radians(center_lat)))) * math.cos(math.pi * i / segments) * math.sin(2 * math.pi * j / segments)
            alt1 = center_alt + radius * math.sin(math.pi * i / segments)

            lat2 = center_lat + (radius / 111320) * math.cos(math.pi * (i + 1) / segments) * math.cos(2 * math.pi * j / segments)
            lon2 = center_lon + (radius / (111320 * math.cos(math.radians(center_lat)))) * math.cos(math.pi * (i + 1) / segments) * math.sin(2 * math.pi * j / segments)
            alt2 = center_alt + radius * math.sin(math.pi * (i + 1) / segments)

            lat3 = center_lat + (radius / 111320) * math.cos(math.pi * (i + 1) / segments) * math.cos(2 * math.pi * (j + 1) / segments)
            lon3 = center_lon + (radius / (111320 * math.cos(math.radians(center_lat)))) * math.cos(math.pi * (i + 1) / segments) * math.sin(2 * math.pi * (j + 1) / segments)
            alt3 = center_alt + radius * math.sin(math.pi * (i + 1) / segments)

            lat4 = center_lat + (radius / 111320) * math.cos(math.pi * i / segments) * math.cos(2 * math.pi * (j + 1) / segments)
            lon4 = center_lon + (radius / (111320 * math.cos(math.radians(center_lat)))) * math.cos(math.pi * i / segments) * math.sin(2 * math.pi * (j + 1) / segments)
            alt4 = center_alt + radius * math.sin(math.pi * i / segments)

            # KMLのポリゴンを作成
            pol = kml.newpolygon(name=f"segment_{i}_{j}")
            pol.outerboundaryis = [
                (lon1, lat1, alt1),
                (lon2, lat2, alt2),
                (lon3, lat3, alt3),
                (lon4, lat4, alt4),
                (lon1, lat1, alt1)  # 閉じるために最初の点を繰り返す
            ]
            pol.altitudemode = simplekml.AltitudeMode.absolute  # 絶対高度
            pol.extrude = 0  # 地面まで伸ばさない（表面のみ）
            pol.style.polystyle.color = simplekml.Color.lightgreen  # ポリゴンの色
            pol.style.polystyle.fill = 1  # 塗りつぶし
            pol.style.polystyle.outline = 1  # 枠線

    # KMLファイルを保存
    kml.save("sphere_surface.kml")

# 球の中心座標と半径を指定して実行
create_sphere_surface_kml(
    center_lat=35.0,  # 緯度
    center_lon=135.0,  # 経度
    center_alt=0,  # 高度m
#    radius=10000,  # 半径m
    radius=500000,  # 半径m
    segments=20  # 緯度・経度の分割数
#    segments=100  # 緯度・経度の分割数(やや重いが球に近づく)
)


'''
■AI(Grok)やりとり
球をkmlフォーマットで描画するためのプログラムのサンプルを教えて

プログラムの説明
ライブラリ: simplekmlを使用してKMLファイルを簡単に生成します。インストールはpip install simplekmlで行います。

球の近似: 球を緯度・経度のグリッドで分割し、各グリッドをポリゴン（四角形）として表現します。segmentsの値を増やすと、より滑らかな球になりますが、ファイルサイズが大きくなります。

座標計算:
緯度・経度の変換には、地球の曲率を考慮し、1度あたり約111.32km（111320m）として近似。

高度はcenter_altにradiusを加算し、球の表面を計算。

KMLの設定:
ポリゴンの色や塗りつぶし、枠線を設定。

altitudemodeをabsoluteに設定し、絶対高度で表示。

extrudeを有効にすると、ポリゴンが地面まで伸びます（視覚効果として）。
→extrude = 0により、ポリゴンは地面に接続せず、球の表面のみを形成

出力: sphere.kmlファイルが生成され、Google Earthや他のKML対応ツールで開けます。

'''