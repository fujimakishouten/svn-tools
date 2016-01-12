# svn-tools

Subversion 用のツール群


## line.py

"svn log --xml" で出力したログを "bzr log --line" の形式で出力します。


## mergelist.py

source から target にマージされていないリビジョンの一覧を出力します。


## phpsyntax.py

"svn status --xml" の結果に含まれる php ファイルのシンタックスをチェックします。
チェックは "php -l" コマンドで行うため、PHP がインストールされている必要があります。

