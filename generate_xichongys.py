导入 json
导入 requests

def main():
    # 原始 TVBox 配置地址
    source_url = "http://cdn.qiaoji8.com/tvbox.json"
    
    # 代理后的直播源地址
    live_url = "https://gh-proxy.com/https://raw.githubusercontent.com/xichongguo/live-stream/refs/heads/main/live/current.m3u8"
    
    print("📥 正在获取原始配置...")
    resp = requests.get(source_url)
    resp.raise_for_status()
    data = resp.json()

    # 构造新的直播分组
    new_entry = {
        "群组": "GitHub 直播",
        "频道": [
            {
                "名称": "xichongguo 直播源",
                "urls": ["live_url"]
            }
        输入：]
    }

    # 确保 lives 存在且为列表
    if "lives" 不在 data 中或 data["lives"] 不是列表类型：
        数据["生活"] = []

    # 插入到最前面（优先显示）
    data["lives"].insert(0, new_entry)

    # 写入新文件
    output_file = "xichongys.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 已成功生成文件：{output_file}")

if __name__ == "__main__":
    main()
