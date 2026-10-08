# ポコチャレ解答集の編集元

編集元はSites `appgprj_6ac5d38d4a1c819198d391565430e75d` です。
サイトの変更はSitesの最新ソース `dist/index.html` に行い、Sitesで編集確認してから公開してください。
公開前にSites側の `node scripts/prepare-github-export.mjs` を必ず実行します。
このディレクトリの `index.html` はGitHub ActionsがSitesの公開済みエクスポートから5分おきに同期します。
GitHub側だけの直接編集は避けてください。直接編集された内容は自動で上書きせず同期が停止します。
同期ワークフローは `.github/workflows/sync-pococha-challenge.yml` です。手動実行にも対応します。
同期の成功とGitHub Pagesの反映を確認してから完了を報告してください。
更新後はSitesの編集確認用リンクとGitHubのスマホ共有用リンクを毎回案内してください。
Sitesの下書きや未公開バージョンは同期対象ではありません。
