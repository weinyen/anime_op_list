# Anime OP/ED Playlist

GitHub Pages 上で YouTube の動画リストを表示するサイトです。`playlist.tsv` を元に自動生成されます。

## 機能

- **グリッド表示**: 5 列でサムネイルを並べる表示
- **リスト表示**: 1 列で縦に並べる表示
- **レスポンシブ**: PC/タブレット/スマホに対応

## 要件

### playlist.tsv の形式

- **エンコーディング**: UTF-8（改行コード：LF または CRLF）
- **形式**: 1 行に `タイトル` `タブ文字` `YouTube URL`
- **例**:
  ```text
  オープニングタイトル	https://www.youtube.com/watch?v=xxxxxxxxxxx
  エンディングタイトル	https://youtu.be/xxxxxxx
  ```

### YouTube URL の形式

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`

## 更新方法

1. **編集**: `playlist.tsv` に新しい行を追加または既存行を修正
2. **コミット**:
   ```bash
   git add playlist.tsv
   git commit -m "docs: update playlist"
   ```
3. **プッシュ**:
   ```bash
   git push
   ```
4. **自動生成**: GitHub Actions が自動的に HTML を再生成・デプロイします（1-2 分程度）

## 手動生成

1. [Actions](https://github.com/weinyen/anime_op_list/actions) タブへ移動
2. 左メニューから **"Generate YouTube Playlist Page"** を選択
3. 右上の **"Run workflow"** ボタンをクリック

## デプロイ設定（初回のみ）

1. リポジトリの **Settings → Pages**
2. **Source**: `Deploy from a branch`
3. **Branch**: `main`
4. **Folder**: `docs/`
5. **Save**

## 確認

デプロイ完了後、以下の URL でページが表示されます：
- https://weinyen.github.io/anime_op_list/

## トラブルシューティング

### ページが更新されない

- `playlist.tsv` が UTF-8 で保存されているか確認
- GitHub Actions の実行履歴を確認

### YouTube サムネイルが表示されない

- URL が正しい形式か確認
- 動画が非公開または年齢制限になっている場合、サムネイルが表示されないことがあります

### エンコーディング問題（文字化け）

- `playlist.tsv` の文字コードを UTF-8 に変換：
  ```bash
  iconv -f UTF-16 -t UTF-8 playlist.tsv > playlist_utf8.tsv && mv playlist_utf8.tsv playlist.tsv
  ```