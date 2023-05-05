import requests
import sqlite3

# 连接到 SQLite 数据库
conn = sqlite3.connect('music.db')
cursor = conn.cursor()

def add_song_detail(song_id):
    # 向服务器发送 GET 请求，获取歌曲详情数据
    url = "http://localhost:3000/song/detail?ids=" + str(song_id)
    response = requests.get(url)
    if response.status_code != 200:
        print("请求失败")
        return None

    # 解析返回的 JSON 数据
    data = response.json()
    if len(data["songs"]) == 0:
        print("未找到指定歌曲")
        return None

    # 提取歌曲详情数据
    song_detail = {}
    song_detail["id"] = int(data["songs"][0]["id"])
    song_detail["name"] = data["songs"][0]["name"]
    song_detail["album"] = data["songs"][0]["al"]["name"]
    song_detail["artists"] = [ar["name"] for ar in data["songs"][0]["ar"]]

    # 向服务器发送 GET 请求，获取歌曲评论数据
    url = "http://localhost:3000/comment/music?id=" + str(song_id)
    response = requests.get(url)
    if response.status_code != 200:
        print("请求失败")
        return None

    # 解析返回的 JSON 数据，提取前十条评论
    data = response.json()
    comments = []
    if "hotComments" in data:
        for comment in data["hotComments"][:10]:
            comments.append((song_detail["id"], comment["content"], comment["time"]))

    # 将歌曲详情和评论数据添加到数据库
    conn = sqlite3.connect("music.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO songs (id, name, album, artist) VALUES (?, ?, ?, ?)",
                   (song_detail["id"], song_detail["name"], song_detail["album"], " / ".join(song_detail["artists"])))
    cursor.executemany("INSERT INTO comments (music_id, content, time) VALUES (?, ?, ?)", comments)
    conn.commit()
    conn.close()

    # 输出提示信息
    print("歌曲 " + str(song_detail["id"]) + " 已成功添加到数据库。")

    return song_detail
add_song_detail(1306923998)

# 关闭连接
cursor.close()
conn.close()
