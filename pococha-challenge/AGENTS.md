# ポコチャレ解答集の編集元

編集元はSites `appgprj_6ac5d38d4a1c819198d391565430e75d` です。
サイトの変更はSitesの最新ソース `dist/index.html` に行い、Sitesで編集確認してから公開してください。
公開前にSites側の `node scripts/prepare-github-export.mjs` を必ず実行します。
Sitesの公開が成功した直後、同じ作業内でSitesの `AGENTS.md` にある「公開後の通知」を実行し、`.github/state/pococha-challenge-release.json` を更新してください。Sites側の `scripts/prepare-github-release.mjs` が成功済みデプロイ結果から通知本文を生成します。
この通知ファイルのpushだけが `.github/workflows/sync-pococha-challenge.yml` の起動条件です。定期実行・手動の新規実行・スクリプトや設定変更だけでは起動しません。
通知のSHA-256とSitesの公開済みエクスポートが一致した場合だけ `index.html` を同期します。
SitesからのネイティブWebhookではなく、公開担当エージェントによる公開後の通知が必要です。通知なしの別経路の公開は検知しません。
GitHub側だけの直接編集は避けてください。直接編集された内容は自動で上書きせず同期が停止します。
同期の成功とGitHub Pagesの反映を確認してから完了を報告してください。失敗時は同じ公開通知に対応する失敗ジョブを再実行できます。
更新後はSitesの編集確認用リンクとGitHubのスマホ共有用リンクを毎回案内してください。
Sitesの下書きや未公開バージョンは同期対象ではありません。
