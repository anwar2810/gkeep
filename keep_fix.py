import gkeepapi
import os

def main():
    # 這裡會從您設定的 GitHub Secrets 讀取帳密
    username = os.getenv('KEEP_USERNAME')
    password = os.getenv('KEEP_PASSWORD')

    keep = gkeepapi.Keep()
    
    try:
        success = keep.login(username, password)
    except Exception as e:
        print(f"登入過程發生錯誤: {e}")
        return

    if not success:
        print("登入失敗，請檢查 GitHub Secrets 的帳密設定。")
        return

    # 華叔的分類邏輯 (關鍵字: {標籤名, 顏色})
    # 顏色代碼: Blue(藍), Green(綠), Yellow(黃), Purple(紫), Red(紅)
    categories = {
        '冷砍鋸': {'label': '冷砍鋸生意', 'color': gkeepapi.node.ColorValue.Blue},
        '1688': {'label': '冷砍鋸生意', 'color': gkeepapi.node.ColorValue.Blue},
        '轉子': {'label': '冷砍鋸生意', 'color': gkeepapi.node.ColorValue.Blue},
        '工地': {'label': '工地項目', 'color': gkeepapi.node.ColorValue.Green},
        '神明': {'label': '家事計畫', 'color': gkeepapi.node.ColorValue.Yellow},
        '大壯': {'label': 'AI創作', 'color': gkeepapi.node.ColorValue.Purple},
        '翠花': {'label': 'AI創作', 'color': gkeepapi.node.ColorValue.Purple}
    }

    notes = keep.all()

    for note in notes:
        # 只處理「未封存」的筆記
        if not note.archived:
            # 將標題與內容結合起來搜尋關鍵字
            combined_text = (note.title + note.text).lower()
            
            for keyword, config in categories.items():
                if keyword in combined_text:
                    # 獲取或建立標籤
                    lbl = keep.findLabel(config['label']) or keep.createLabel(config['label'])
                    note.labels.add(lbl)
                    note.color = config['color']
                    print(f"已整理筆記: {note.title or '無標題'} -> 分類為: {config['label']}")

    # 同步變更回 Google 雲端
    keep.sync()
    print("Google Keep 系統化整理任務已完成！")

if __name__ == "__main__":
    main()
