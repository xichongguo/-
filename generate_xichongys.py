import json
import requests
import re

def parse_m3u(content):
    """
    解析 M3U/M3U8 内容，提取频道名称和直播流地址。
    支持格式：
      #EXTINF:-1 tvg-name="CCTV1" ...,CCTV1
      http://example.com/cctv1.m3u8
    """
    channels = []
    lines = content.strip().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#EXTINF"):
            # 尝试提取频道名：优先用 tvg-name，其次用逗号后的内容
            name = "未知频道"
            # 匹配 tvg-name="xxx"
            tvg_match = re.search(r'tvg-name=["\']([^"\']+)["\']', line, re.IGNORECASE)
            if tvg_match:
                name = tvg_match.group(1)
            else:
                # 否则取逗号后的内容
                parts = line.split(',', 1)
                if len(parts) > 1 and parts[1].strip():
                    name = parts[1].strip()
            
            # 下一行应为 URL
            if i + 1 < len(lines):
                url = lines[i + 1].strip()
                if url and not url.startswith("#"):
                    channels.append({
                        "name": name,
                        "urls": [url]
                    })
            i += 2
        else:
            i += 1
    return channels

def main():
    # 1. 获取原始 tvbox.json
    tvbox_url = "http://cdn.qiaoji8.com/tvbox.json"
    print("📥 正在获取原始 TVBox 配置...")
    try:
        resp = requests.get(tvbox_url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"⚠️ 获取原始配置失败: {e}，将创建新配置")
        data = {}

    # 2. 获取并解析远程 M3U8 播放列表
    raw_m3u_url = "https://raw.githubusercontent.com/xichongguo/live-stream/refs/heads/main/live/current.m3u8"
    proxy_m3u_url = f"https://gh-proxy.com/{raw_m3u_url}"
    
    print("📡 正在获取并解析直播源列表...")
    try:
        m3u_resp = requests.get(proxy_m3u_url, timeout=15)
        m3u_resp.raise_for_status()
        m3u_content = m3u_resp.text
        
        if not m3u_content.strip().startswith("#EXTM3U"):
            raise ValueError("返回内容不是有效的 M3U 格式")
        
        channels = parse_m3u(m3u_content)
        print(f"✅ 成功解析 {len(channels)} 个直播频道")
    except Exception as e:
        print(f"❌ 解析直播源失败: {e}")
        # 回退到直接插入 M3U 链接（不推荐，仅作备用）
        channels = [{
            "name": "【错误】请检查直播源",
            "urls": [proxy_m3u_url]
        }]

    # 3. 构造新的直播分组
    new_entry = {
        "group": "GitHub 直播",
        "channels": channels
    }

    # 4. 确保 lives 存在
    if "lives" not in data or not isinstance(data["lives"], list):
        data["lives"] = []

    # 移除已存在的同名分组（避免重复）
    data["lives"] = [item for item in data["lives"] if item.get("group") != "GitHub 直播"]
    
    # 插入到最前面
    data["lives"].insert(0, new_entry)

    # 5. 写入输出文件
    output_file = "xichongys.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"🎉 已成功生成文件：{output_file}")

if __name__ == "__main__":
    main()
