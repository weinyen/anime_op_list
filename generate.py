#!/usr/bin/env python3
"""Generate static HTML from playlist.tsv for GitHub Pages."""

import csv
import os

def parse_playlist(filepath):
    """Parse playlist.tsv and return list of (title, url) tuples."""
    videos = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) >= 2:
                title = row[0].strip()
                url = row[1].strip()
                if title and url:
                    videos.append((title, url))
    return videos

def extract_video_id(url):
    """Extract YouTube video ID from URL."""
    if 'youtu.be/' in url:
        return url.split('youtu.be/')[-1].split('?')[0].split('&')[0]
    elif 'youtube.com' in url:
        if 'v=' in url:
            return url.split('v=')[1].split('&')[0]
    return ''

def generate_html(videos):
    """Generate HTML content."""
    items = []
    for title, url in videos:
        video_id = extract_video_id(url)
        if video_id:
            items.append({
                'title': title,
                'thumbnail': f'https://img.youtube.com/vi/{video_id}/mqdefault.jpg',
                'url': url
            })

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Anime OP/ED Playlist</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #1a1a2e; color: #eee; min-height: 100vh; }}
    header {{ background: #16213e; padding: 20px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.3); }}
    h1 {{ color: #e94560; font-size: 1.8rem; }}
    .controls {{ display: flex; justify-content: center; gap: 15px; padding: 20px; background: #0f3460; }}
    button {{ background: #16213e; color: #eee; border: 2px solid #e94560; padding: 8px 20px; border-radius: 8px; cursor: pointer; font-size: 1rem; transition: all 0.3s; }}
    button:hover {{ background: #e94560; color: #1a1a2e; }}
    button.active {{ background: #e94560; color: #1a1a2e; }}
    .container {{ padding: 20px; max-width: 1400px; margin: 0 auto; }}
    .grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 20px; }}
    .list {{ display: grid; grid-template-columns: 1fr; gap: 15px; }}
    @media (max-width: 1200px) {{ .grid {{ grid-template-columns: repeat(3, 1fr); }} }}
    @media (max-width: 768px) {{ 
      .grid {{ grid-template-columns: repeat(2, 1fr); }} 
      .container {{ padding: 15px; }}
    }}
    @media (max-width: 480px) {{ 
      .grid {{ grid-template-columns: 1fr; }} 
      h1 {{ font-size: 1.4rem; }}
    }}
    .video-item {{ position: relative; border-radius: 12px; overflow: hidden; background: #16213e; box-shadow: 0 4px 15px rgba(0,0,0,0.3); transition: transform 0.3s, box-shadow 0.3s; }}
    .video-item:hover {{ transform: translateY(-5px); box-shadow: 0 8px 25px rgba(233, 69, 96, 0.4); }}
    .video-item.list-item {{ display: flex; align-items: center; gap: 15px; }}
    .video-item.list-item img {{ width: 120px; height: 68px; flex-shrink: 0; }}
    .video-item.list-item .title {{ font-size: 1rem; }}
    .video-item:not(.list-item) img {{ width: 100%; height: auto; display: block; }}
    .video-item .title {{ position: absolute; bottom: 0; left: 0; right: 0; padding: 20px; background: linear-gradient(to top, rgba(0,0,0,0.9), transparent); color: #fff; font-size: 0.95rem; line-height: 1.4; }}
    .video-item.list-item .title {{ position: static; background: none; padding: 15px; }}
    .play-icon {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 50px; height: 50px; background: rgba(233, 69, 96, 0.9); border-radius: 50%; display: flex; align-items: center; justify-content: center; opacity: 0; transition: opacity 0.3s; }}
    .video-item:hover .play-icon {{ opacity: 1; }}
    .play-icon::before {{ content: '▶'; color: #fff; font-size: 1.2rem; margin-left: 3px; }}
    footer {{ text-align: center; padding: 30px; color: #666; font-size: 0.9rem; }}
  </style>
</head>
<body>
  <header>
    <h1>🎬 Anime OP/ED Playlist</h1>
  </header>
  <div class="controls">
    <button id="gridBtn" class="active" onclick="setView('grid')">Grid</button>
    <button id="listBtn" onclick="setView('list')">List</button>
  </div>
  <div class="container">
    <div class="grid" id="videoContainer">
'''

    for item in items:
        html += f'''      <a href="{item['url']}" target="_blank" class="video-item grid-item">
        <img src="{item['thumbnail']}" alt="{item['title'].replace('"', '&quot;')}">
        <div class="title">{item['title']}</div>
        <div class="play-icon"></div>
      </a>
'''

    html += '''    </div>
    <div class="list" id="listContainer" style="display: none;">
'''

    for item in items:
        html += f'''      <a href="{item['url']}" target="_blank" class="video-item list-item">
        <img src="{item['thumbnail']}" alt="{item['title'].replace('"', '&quot;')}">
        <div class="title">{item['title']}</div>
        <div class="play-icon"></div>
      </a>
'''

    html += f'''    </div>
  </div>
  <footer>
    <p>Generated from playlist.tsv | Total: {len(items)} videos</p>
  </footer>
  <script>
    function setView(view) {{
      document.getElementById('gridBtn').classList.toggle('active', view === 'grid');
      document.getElementById('listBtn').classList.toggle('active', view === 'list');
      document.getElementById('videoContainer').style.display = view === 'grid' ? 'grid' : 'none';
      document.getElementById('listContainer').style.display = view === 'list' ? 'grid' : 'none';
      if (view === 'list') {{
        document.querySelectorAll('.list-item').forEach(item => item.style.opacity = '1');
      }}
    }}
  </script>
</body>
</html>'''
    return html

def main():
    videos = parse_playlist('playlist.tsv')
    html = generate_html(videos)
    os.makedirs('docs', exist_ok=True)
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated docs/index.html with {len(videos)} videos")

if __name__ == '__main__':
    main()
