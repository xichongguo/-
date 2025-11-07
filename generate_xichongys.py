import json
import requests

def main():
    source_url = "http://cdn.qiaoji8.com/tvbox.json"
    live_url = "https://gh-proxy.com/https://raw.githubusercontent.com/xichongguo/live-stream/refs/heads/main/live/current.m3u8"
    
    print("📥 正在获取原始配置...")
    resp = requests.get(source_url)
    resp.raise_for_status()
    data = resp.json()

    new_entry = {
        "group": "GitHub 直播",
        "channels": [
            {
                "name": "xichongguo 直播源",
                "urls": [live_url]
            }
        ]
    }

    if "lives" not in data or not isinstance(data["lives"], list):
        data["lives"] = []

    data["lives"].insert(0, new_entry)

    with open("xichongys.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ 已成功生成文件：xichongys.json")

if __name__ == "__main__":
    main()
