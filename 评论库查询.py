import sqlite3


def remove_duplicate_comments():
    # 连接数据库
    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()

    # 遍历所有歌曲，检查是否有重复评论
    cursor.execute("SELECT id, name, artist, album FROM songs")
    songs = cursor.fetchall()
    for song in songs:
        song_id = song[0]
        song_name = song[1]
        artist = song[2]
        album = song[3]

        print(f"\n歌曲 {song_id}-{song_name}-{artist}-{album} 的评论：")

        # 检查是否有重复评论
        cursor.execute(f"SELECT COUNT(*) FROM comments WHERE music_id=? GROUP BY content HAVING COUNT(*) > 1",
                       (song_id,))
        duplicates = cursor.fetchall()

        if len(duplicates) == 0:
            print("没有重复评论")
        else:
            print(f"共检测到 {len(duplicates)} 条重复评论，开始删除...")
            for count in duplicates:
                # 获取相同评论的记录列表
                cursor.execute(f"SELECT id FROM comments WHERE music_id=? GROUP BY content HAVING COUNT(*)=?",
                               (song_id, count[0]))
                to_delete = cursor.fetchall()[1:]

                # 删除相同评论的多余记录
                for record in to_delete:
                    cursor.execute(f"DELETE FROM comments WHERE id=?", (record[0],))
            conn.commit()
            print(f"共删除了 {len(to_delete)} 条评论")

        # 输出所有评论
        cursor.execute(f"SELECT content, time FROM comments WHERE music_id=?", (song_id,))
        comments = cursor.fetchall()

        for comment in comments:
            print(f"{comment[0]}\t{comment[1]}")

    # 关闭数据库
    conn.close()

if __name__ == '__main__':
    remove_duplicate_comments()

