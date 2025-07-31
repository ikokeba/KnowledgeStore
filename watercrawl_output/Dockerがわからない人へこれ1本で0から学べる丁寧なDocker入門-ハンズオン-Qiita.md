## Why not login to Qiita and try out its useful features?

We'll deliver articles that match you.

You can read useful information later.

[Login](/login?callback_action=login_or_signup&redirect_to=%2FSicut_study%2Fitems%2F4f301d000ecee98e78c9&realm=qiita)[Sign up](/signup?callback_action=login_or_signup&redirect_to=%2FSicut_study%2Fitems%2F4f301d000ecee98e78c9&realm=qiita)Later

[1155](/Sicut_study/items/4f301d000ecee98e78c9/likers)

Go to list of users who liked

1344

Share on X(Twitter)

Share on Facebook

[](https://b.hatena.ne.jp/entry/s/qiita.com/Sicut_study/items/4f301d000ecee98e78c9 "Hatena Bookmark")

Add to Hatena Bookmark

more_horiz

Delete article

close

Deleted articles cannot be recovered.

Draft of this article would be also deleted.

Are you sure you want to delete this article?

CancelDeletedelete

info

More than 1 year has passed since last update.

[お題は不問！Qiita Engineer Festa 2024で記事投稿！ Qiita Engineer Festa20242024年7月17日まで開催中！ ](https://qiita.com/official-events/16baee61b1d8bd4aac5a)

[![](https://qiita-user-profile-images.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F810513%2Fprofile-images%2F1714917423?ixlib=rb-4.0.0&auto=compress%2Cformat&lossless=0&w=48&s=095cc9bbf82664800fa49550359629c3)@Sicut_study(渡邉 臣 | JISOU)](/Sicut_study)in[![](https://qiita-organization-images.imgix.net/https%3A%2F%2Fs3-ap-northeast-1.amazonaws.com%2Fqiita-organization-image%2Fdb464ee832f8806a5f89e94b446c72fa3df3a38c%2Foriginal.jpg%3F1712546356?ixlib=rb-4.0.0&auto=compress%2Cformat&s=4045fb264410c4ead6a5b173ad9af053)JISOU | Reactプログラミングコーチング](/organizations/jisou)

# Dockerがわからない人へ。これ1本で0から学べる丁寧なDocker入門

  * [Docker](/tags/docker)
  * [ハンズオン](/tags/%e3%83%8f%e3%83%b3%e3%82%ba%e3%82%aa%e3%83%b3)



Last updated at 2024-07-09Posted at 2024-07-08

#  __はじめに

**私のエンジニアとしての初仕事はDockerでした。辛かったのをいまでも思い出します**

みなさんこんにちは、Watanabe Jin([@Sicut_study](/Sicut_study "Sicut_study"))です。

みなさんはエンジニア始めたての時にどんなことで苦労したでしょうか？

  * GitHub
  * Docker
  * Kubernetes
  * AWS



など色々あるかと思いましたが、「環境構築」というのは多くの人がつまづく箇所かと思います。  
プログラミングの勉強をするにはそもそもの開発環境がないとできないことも多いです。

またAWSなどのクラウドを利用してデプロイをするときにも再度登場して苦しめられます。

今回はそんな初心者には考え方や使いどころがわかりづらい**Docker** について**例え話を活用** しながら説明していきたいと思います。

Dockerが難しいと思うのは、「概念がよくわからない」「説明を読んでも使いどころのイメージがつかない」というのがあるかと思います。  
この記事では「例え話」「ハンズオン」を駆使しながら解説しております。

エンジニアをやる上でDockerの技術は必須だと考えます。ぜひとも使えるようになっていただいてご自身の勉強に活用いただけたらと思います。

#  __対象読者

  * Dockerという言葉を聞いたことがある人
  * Dockerを少し使ったことがある人
  * 環境構築を楽に行いたい人
  * エンジニアとして1つレベルアップしたい人
  * 難しい説明で挫折した人



#  __目次

  1. Dockerとは何か？なぜ使うのか？
  2. Dockerの導入
  3. コンテナを起動してみる
  4. Dockerfileでイメージを作ろう
  5. APIをイメージで起動してみる
  6. Docker Composeで楽に起動しよう



#  __1\. Dockerとは何か？なぜ使うのか？

まずはよくあるDokerの説明から行います(知らない方は難しいやつです)

> Dockerは、コンテナ技術を利用してアプリケーションを効率的にデプロイ、スケール、および管理するためのプラットフォームです。Dockerは、ソフトウェアを「コンテナ」と呼ばれる独立したユニットにパッケージ化します。このコンテナは、アプリケーションコード、ランタイム、ライブラリ、および依存関係をすべて含んでおり、どの環境でも一貫して動作します

個人的にDockerが難しいのは「Docker自体」を勉強しようと本を読んだり、ネットを調べても難しい言葉がたくさんあってイメージがつかないことです。

今回は**ゲーム(Switch)** を使って例え話をします

では先程の文章をゲームで例えてみましょう

> Dockerをゲーム機(Switch)に例えます。ゲーム機では色々なゲームソフトをストアからインストール(ソフトの購入)できます。このゲーム1つ1つをコンテナといい、それぞれのゲームにはすでにプログラミングがされており、使う人はどんなコードで書かれているか理解しなくてもゲームを起動するだけで遊べます。また他人のゲーム機(他のDocker環境)にソフト(カートリッジ)を入れても同じく動作します  
  
---  
[![image.png](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F810513%2F1e3cf7dc-889e-dfa9-573c-87fd872c1f41.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=12b7607aff6a6d009a66be2f76263097)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F810513%2F1e3cf7dc-889e-dfa9-573c-87fd872c1f41.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=12b7607aff6a6d009a66be2f76263097)  
Docker(Switch)で複数のコンテナ(ゲーム)が存在する  
---  
[![image.png](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F810513%2Fafc0d289-93a8-e080-7023-7a9ec97f3e03.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=2add9e22e6c142298a3d73f67e4f0de4)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F810513%2Fafc0d289-93a8-e080-7023-7a9ec97f3e03.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=2add9e22e6c142298a3d73f67e4f0de4)  
カセットはどのSwitchでも動作する  
  
なんとなくDockerについてのイメージがついたところで **なぜ使うのか？** を説明します

Dockerを利用することで以下のようなメリットがあります。

###  __効率的なデプロイ

ゲームソフトをカートリッジにパッケージ化しておくことで、どのゲーム機でも簡単にそのゲームをプレイできるようになります。

同様に、Dockerコンテナを使えば、どのコンピュータでも簡単にアプリケーションをデプロイできます。

Dockerという環境があれば常にコンテナは動かすことができるというのが重要で、ローカルでコンテナが起動できるならクラウド上のDockerでも起動できます

###  __スケーラビリティ

Dockerは同じアプリケーションの複数のインスタンスを簡単にスケール（増やす）することができます。これにより、多くのユーザーが同時にアプリケーションを利用できるようになります。

これはゲームで例えるのが少し難しかったので実際の例を説明します。  
もしあなたのWebサイトが突然テレビで紹介されて多くのユーザーがアクセスしたとします。

そうなるとアクセスが増加して普通であればアプリケーションは遅くなります。  
しかし、コンテナであればいくらでもコンテナを起動することが可能です

複数コンテナを起動することでアクセスを1つのコンテナでなく、分散させることができるのです

[![image.png](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F810513%2Fe672822e-f049-937c-5f49-57d52a363373.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=71dfe73a482cea55a4920df7505b2184)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F810513%2Fe672822e-f049-937c-5f49-57d52a363373.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=71dfe73a482cea55a4920df7505b2184)

あえて例え話をするなら「フランチャイズのお店」をイメージしてください

> とある有名なラーメン店が1店舗あったとします。  
>  そのお店1つではお客さんを長く待たせてしまうので、フランチャイズ(コンテナ)でお店を作ってお客さんを分散させることにしました  
>  このお店は料理やオペレーションなどがすべてマニュアル化されているので、同じお店を作ることが容易でした

###  __管理のしやすさ

それぞれのゲームソフトが独立しているため、特定のゲーム（アプリケーション）が他のゲームに影響を与えません。

同様に、Dockerコンテナは独立した環境を提供するため、各アプリケーションが他のアプリケーションに影響を与えることなく管理できます。

ポケモンにバグがあったとしても、ドラゴンクエストには影響を及ぼすことはないのです

#  __2\. Dockerを導入してみよう

ここからはみなさんのパソコンにDockerの環境を用意しましょう

Dockerの環境構築は私の中で大きく2つの方法があります。

  * Docker Desktopを利用する
  * コマンドでインストールをする



あまりLinuxコマンドに慣れていないのであれば、まずはDocker Desktopを利用することをおすすめします。  
インストールするだけでDocker環境を構築することができます

もしコマンドに慣れているのであればそちらでも大丈夫です

インストールが完了したら以下のコマンドをターミナルで叩いてみます

Copied!
    
    
    $ docker -v
    Docker version 23.0.1, build a5ee5b1
    

このように表示されれば大丈夫です。

#  __3\. コンテナを起動してみる

いまあなたの目の前にはゲーム機があります。  
ソフトを買って起動したくてワクワクしているはずです  
ここからは実際にコンテナの起動をしながらより理解を深めていきます。

まずは以下のコマンドを実行してみてください

Copied!
    
    
    $ docker pull hello-world
    
    Unable to find image 'hello-world:latest' locally
    latest: Pulling from library/hello-world
    c1ec31eb5944: Pull complete 
    Digest: sha256:94323f3e5e09a8b9515d74337010375a456c909543e1ff1538f5116d38ab3989
    Status: Downloaded newer image for hello-world:latest
    

Copied!
    
    
    $ docker run hello-world
    
    Hello from Docker!
    

まずはゲームソフトをネットから買ってくる操作をしました  
ネット上には多くのイメージ(ゲームソフト)があります。  
今回は「hello-world」というゲームソフトを`pull`コマンドで取得しました

次に`run`コマンドでイメージを起動します。Docker上にイメージを元にコンテナが起動します  
今回のイメージ(hello-world)は`Hello from Docker!`と表示(echo)するものだったのでターミナルに表示されました

では次にデータベースのイメージを起動してみようと思います。

イメージはDocker Hubに色々あります。好きなソフトを簡単に起動できるのでDockerさえあれば簡単にDBも利用できます。(本来ならコマンドで色々インストールして構築する必要があります)

Copied!
    
    
    $ docker pull postgres
    $ docker run --name postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
    

いくつかみなれないものがでてきました

  * \--name : コンテナにpostgresと名前をつけました
  * -e : 環境変数POSGRES_PASSWORDにmysecretpasswordと設定しました
  * -d : バックグラウンド起動 (これがないとログがたくさんでる)



docker runではコンテナに対して設定ができるような引数を使うことができます

DBの環境をもつコンテナが起動してので早速使ってみます

まずはコンテナが起動できているかを確認します

Copied!
    
    
    $ docker ps
    
    CONTAINER ID   IMAGE                            COMMAND                   CREATED         STATUS          PORTS                             NAMES
    b2c5f83206fc   postgres                         "docker-entrypoint.s…"   4 minutes ago   Up 4 minutes    5432/tcp                          postgres
    

`docker ps`でいまDocker環境にあるコンテナの一覧をみることができます  
ここではpostgresという名前でコンテナができていることがわかります

Copied!
    
    
    $ docker exec -it postgres bash
    

まずはコンテナに入ります。  
コンテナはいわば小さなPCのようなもので、そのPCにはすでにDBに必要なものがすべて含まれています。  
そのPCの世界に入ることでDBが利用できます。  
`docker exec -it コンテナ名 bash`でコンテナの中には入れます

入れたらあとはローカルでPosgresをインストールシているときと同じように使えます

Copied!
    
    
    root@b2c5f83206fc:/# psql -U postgres -d postgres
    postgres=# 
    
    exit // Postgresqlから抜ける
    exit //コンテナから抜ける
    

これでローカルにPostgresを入れたときと同じようなことがコンテナを利用してできました。  
本来であれば大変だった環境構築もイメージを利用することで簡単です

ここで疑問が湧いた人もいるかもしれません  
**hello-worldのコンテナがdocker psで表示されない！！**

コンテナには**実行した状態** と**終了した状態** があります。  
hello-worldコンテナは、非常にシンプルなコンテナで、実行するとすぐに終了するように設計されています。

起動が終了しているので表示されなかったのです

Postgresはデータベースサーバーです。  
これは、常に実行されている必要があります。アプリケーションがデータを保存したり取得したりするために、データベースサーバーが常に稼働している必要があるからです。なので常に実行中なのでpsコマンで表示されました

`docker exec -it`でコンテナに入りましたが、このコマンドで入れるコンテナは起動中のものになります。起動が終わるとPC自体もなくなってしまいます

#  __4\. Dockerfileでイメージを作ろう

ではここからはイメージ(ゲームソフト)を自分で作成してみて、Dockerの中で起動してみましょう

ここではゲームの仕様書である**Dockerfile** というものを作成します

Dockerfileは、Dockerイメージをビルドするための設計図です。テキストファイル形式で、各ステップを記述していきます。Dockerfileには、ベースイメージ、アプリケーションのソースコード、依存関係のインストール方法、実行コマンドなどが含まれています。

Dockerfileの基本構成：

FROM：ベースイメージを指定します。  
WORKDIR：作業ディレクトリを設定します。  
COPY：ローカルファイルをコンテナ内にコピーします。  
RUN：コマンドを実行します（例：パッケージのインストール）。  
CMD：コンテナが起動されたときに実行されるデフォルトのコマンドを指定します。

少し難しいと思うので作りながら理解していきましょう

まずは先程使った`hello-world`を自作してみます

Copied!
    
    
    $ touch Dockerfile
    

Copied!
    
    
    # ベースイメージとしてAlpine Linuxを使用
    FROM alpine:latest
    
    # コマンドを実行して「Hello, World!」を表示
    CMD ["echo", "Hello, World!"]
    

Dockerfileの最初の`From`にイメージを書いています  
これはネットにあるイメージです

基本的には0からDockerfileを作ることはなく、他の人が作ったイメージの上からカスタマイズをしてくことが基本になります。

イメージとしては、Switchの「マリオメーカー」といったものでしょうか  
ゲーム自体の基本はあってユーザーはその機能を利用して新しいゲームを作成することができます

ではこの仕様書を使ってゲームソフトにしていきます

Copied!
    
    
    $ docker build -t my-hello-world .
    $ docker run my-hello-world
    

最初のコマンドで設計書からゲームソフトを作成します  
そしてrunで起動すると同じものが起動できるはずです。

#  __5\. APIをイメージで起動する

みなさんの手元にはJavaScriptのフレームワークであるExpressが起動できる環境はありますでしょうか？

なくても大丈夫です。みなさんの手元にはDocker環境があるためExpressの環境があるイメージ(ゲームソフト)があれば実行ができます

Copied!
    
    
    $ mkdir docker-express
    $ cd docker-express
    $ touch app.js
    

次にjsファイルにexpressのAPIサーバーを起動するコードを書いてみます

app.js

Copied!
    
    
    const express = require('express');
    const app = express();
    const port = 3000;
    
    app.get('/', (req, res) => {
      res.send('Hello, World!');
    });
    
    app.listen(port, () => {
      console.log(`App listening at http://localhost:${port}`);
    });
    

せっかくなので試しに手元で起動してみましょう  
もし手元にNode環境がなければ用意して試してほしいですが、DockerがあればNodeがなくてもできますので試すかはおまかせします

Copied!
    
    
    $ npm init -y
    $ npm i express
    $ node app.js
    
    最後はcrtl+Cで止めてください (このあと3000番ポートが利用できなくなります)
    

これでサーバーが起動したのでcurlでAPIを叩いてみます

Copied!
    
    
    curl localhost:3000
    Hello, World
    

ローカルでexpressのAPIを起動できました  
ではこれを**Dockerfile** を使って行いたいと思います。

Copied!
    
    
    $ touch Dockerfile
    

Copied!
    
    
    # ベースイメージを指定
    FROM node:14
    
    # 作業ディレクトリを設定
    WORKDIR /usr/src/app
    
    # package.jsonとpackage-lock.jsonをコピー
    COPY package*.json ./
    
    # 依存関係をインストール
    RUN npm install
    
    # アプリケーションのソースコードをコピー
    COPY app.js .
    
    # アプリケーションを実行
    CMD [ "node", "app.js" ]
    

ではDockerfileを解説していきます

まずは`From node:14`というすでにネットにあるNode.jsのイメージを土台に用意しています。これを用意することでローカルにNode環境があるという前提を実現させます

次に`WORKDIR /usr/src/app`で`cd /usr/src/app`のようなことをしています

そのあとに先程ローカルで作成した`package.json`を`/usr/src/app`にコピーします。package.jsonには先程npm iでいれたexpressが入っています

package.json

Copied!
    
    
    {
      "name": "docker-express",
      "version": "1.0.0",
      "description": "",
      "main": "app.js",
      "scripts": {
        "test": "echo \"Error: no test specified\" && exit 1"
      },
      "keywords": [],
      "author": "",
      "license": "ISC",
      "dependencies": {
        "express": "^4.19.2"
      }
    }
    

なのでわざわざDockerfile内で`npm i express`などはしなくてもコピーだけで問題ありません

次に`COPY app.js .`でコンテナの`/usr/src/app`にいまいるディレクトリ`docker-express`の`app.js`をコピーします

最後にアプリケーションの起動をします  
`CMD [ "node", "app.js" ]`としていますが、`CMD`で書くことでコンテナ起動時に実行されるコマンドをかくことができます

ここまでみるとローカルで起動するまでに行った手順とほとんど変わらないことがわかります

では実際にイメージからAPIを起動してみましょう

Copied!
    
    
    # my-node-appというイメージ名で作成
    $ docker build -t my-node-app .
    
    # 起動
    $ docker run -p 3000:3000 --name my-node-app my-node-app 
    

`-p 3000:3000`という見慣れないものがでてきました  
これはDocker コマンドのオプションで、ホストマシンとコンテナの間でポートをマッピング（バインド）するために使用されます。  
これにより、ホストマシンの特定のポートにアクセスすると、そのリクエストがコンテナ内の対応するポートにリダイレクトされます。

このオプションがないとコンテナ(PC)の中では`localhost:3000`で起動していますが、コンテナと今私たちが操作しているローカルの世界はまったくの独立した世界になるのでローカルの`localhost:3000`とコンテナの`localhost:3000`は別物になるのです

そこでホストマシンのlocalhost:3000にアクセスしたら自動でコンテナのlocalhost:3000に繋いでくれるようにするのが-pコマンドなのです

[![image.png](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F810513%2F7cf0db21-d177-0983-5dbd-608c1630e634.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=cc8dacf0067071ef19bee2b4fa4c9c6c)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F810513%2F7cf0db21-d177-0983-5dbd-608c1630e634.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=cc8dacf0067071ef19bee2b4fa4c9c6c)

Copied!
    
    
    # 別ターミナルを開く
    curl localhost:3000
    Hello, World!
    

では試しに-pをつけずにも試してみましょう  
まずは起動中のコンテナを止めてきます

Copied!
    
    
    $ docker stop my-node-app
    $ docker rm my-node-app
    $ docker run --name my-node-app my-node-app
    

コンテナを止めるには`stop`コマンドが利用できます(ゲームソフトを終了させることができます)  
コンテナは止めても再起動できる状態でソフト自体はゲーム機に残っています(ダウンロードしたソフトはいつでも遊べる)  
なのでrmコマンドでコンテナを完全削除します(ゲームのアンインストール)

ではアクセスしてみます

Copied!
    
    
    $ curl localhost:3000
    curl: (7) Failed to connect to localhost port 3000: 接続を拒否されました
    

`-p 3000:3000`がないためホストマシン(ローカル)の3000番ポートにアクセスしてもコンテナの3000番にはつながらないため接続拒否されました

[![image.png](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F810513%2Fde4bc88d-10bf-d118-7d0c-3867e1c58a1d.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=2c64c1a47470427307cc7cc101344f4d)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F810513%2Fde4bc88d-10bf-d118-7d0c-3867e1c58a1d.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=2c64c1a47470427307cc7cc101344f4d)

試しにコンテナの中に入って同じコマンドを叩いてみましょう

Copied!
    
    
    $ docker exec -it my-node-app bash
    $ curl localhost:3000
    Hello, World!
    

コンテナのなかであればlocalhost:3000でAPIを使うことができるためうまくいきました

#  __6\. Docker Composeで楽に起動しよう

あなたがAPIをこれからexpressで作るとなると、expressのコンテナとDB(postgres)のコンテナ2つを開発のたびに起動する必要があります

Copied!
    
    
    $ docker run -p 3000:3000 --name my-node-app my-node-app 
    $ docker run --name postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
    

しかしこのコマンドかなり長いし、コンテナを1つ1つ`run`で起動しないといけないですし大変だと気づきます

そこで登場するのが`Docker compose`というツールです。Docker Composeは、複数のDockerコンテナを定義し、実行することができます。

さっそくインストールをしましょう

Copied!
    
    
    $ docker compose version
    Docker Compose version v2.27.1
    

Docker Composeは`YAML`というファイル形式で設定を書くことができますので、試しに書いてみましょう

Copied!
    
    
    $ touch docker-compose.yml
    

docker-compose.yml

Copied!
    
    
    version: '3'
    services:
      web:
        build: .
        container_name: my-node-app
        working_dir: /usr/src/app
        volumes:
          - .:/usr/src/app
        ports:
          - "3000:3000"
        depends_on:
          - db
    
      db:
        image: postgres:13
        container_name: postgres-db
        environment:
          POSTGRES_PASSWORD: mysecretpassword
        volumes:
          - pgdata:/var/lib/postgresql/data
    
    volumes:
      pgdata:
    

色々わからないことが多いと思うので解説します

###  __my-node-app

my-node-appはすでにDockerfileがあるので利用してコンテナを起動するように設定を書きました

`build: .`はDockerfile(./Dockerfile)をもとに起動することを書いています。Dockerfileは自明なので`.`のみで場所を教えればDockerfileを探して起動してくれます(コマンドでいうとdocker run my-node-app)

`container_name`でコンテナに名前つけます (--name my-node-app)

`working_dir`でコンテナに入ったときの最初の位置を設定できます (docker exec -it my-node-app bashをするとこのディレクトリの位置にいきます)

`volumes`ではローカルのディレクトリ(docker-express)とコンテナのusr/src/appをマウントしています。これによりdocker-expressにファイルが追加されたら、コンテナにも作成されます。ディレクトリの内容が同期された状態になります

`ports`はコマンドの-p 3000:3000を表しています

`depends_on`は起動する際の依存関係を書いており、`db`という名前のコンテナが起動してからこのコンテナは起動することが設定されています

###  __DB(postgres)

DBの起動はDockerfileを利用せず、すでに用意されているイメージを利用していました  
その場合はこのようにかけます

Copied!
    
    
        image: postgres:13
    

postgresでは環境変数を与える必要があるので`environment`を使って環境変数の設定を行いました (コマンドの-e POSTGRES_PASSWORD=mysecretpassword)

またDBはコンテナを停止してもデータは消えてほしくありません  
そこでデータを**永続化** させるために以下の設定を行います

Copied!
    
    
        volumes:
          - pgdata:/var/lib/postgresql/data
    
    volumes:
      pgdata:
    

それではさっそく起動していきます

Copied!
    
    
    # 先程起動したコンテナを消しておく
    $ docker sotp my-node-app
    $ docker rm my-node-app
    
    $ docker compose up
    # 別ターミナルで実行
    $ docker ps
    
    CONTAINER ID   IMAGE                             COMMAND                   CREATED              STATUS         PORTS                                                 NAMES
    5d5b1011d1db   docker-express-web                "docker-entrypoint.s…"   5 seconds ago        Up 4 seconds   0.0.0.0:3000->3000/tcp, :::3000->3000/tcp             my-node-app
    c2ab945ab873   postgres:13                       "docker-entrypoint.s…"   About a minute ago   Up 4 seconds   5432/tcp                                              postgres-db
    

設定した2つのコンテナをコマンド1つで簡単に起動できました  
これで長いrunコマンドとはおさらばです！

#  __おわりに

今回はたとえ話をしながらDockerというものついて解説して  
実際にハンズオンを行いながらDockerで色々な環境を起動する体験をしていただきました

Dockerを使えるようになると一気に実力をあげることができます。  
大変な環境構築が楽になり、クラウドへのデプロイもできるようになります。

私が成長したのはDockerを理解したところからだったのでぜひハンズオンを生かしてDockerを試していただけたらと思います。

ここまで読んでいただけた方はいいねとストックよろしくお願いします。  
[@Sicut_study](/Sicut_study "Sicut_study") をフォローいただけるととてもうれしく思います。

また明日の記事でお会いしましょう！

#  __JISOUのメンバー募集中

プログラミングコーチングJISOUではメンバーを募集しています。  
日本一のアウトプットコミュニティでキャリアアップしませんか？

気になる方はぜひHPからライン登録お願いします👇

[1155](/Sicut_study/items/4f301d000ecee98e78c9/likers)

Go to list of users who liked

1344

comment4

Go to list of comments

Share on X(Twitter)

Share on Facebook

[](https://b.hatena.ne.jp/entry/s/qiita.com/Sicut_study/items/4f301d000ecee98e78c9 "Hatena Bookmark")

Add to Hatena Bookmark

Register as a new user and use Qiita more conveniently

  1. You get articles that match your needs
  2. You can efficiently read back useful information
  3. You can use dark theme

[What you can do with signing up](https://help.qiita.com/ja/articles/qiita-login-user)

[Sign up](/signup?callback_action=login_or_signup&redirect_to=%2FSicut_study%2Fitems%2F4f301d000ecee98e78c9&realm=qiita)[Login](/login?callback_action=login_or_signup&redirect_to=%2FSicut_study%2Fitems%2F4f301d000ecee98e78c9&realm=qiita)

関連記事 [Recommended by ](https://www.logly.co.jp/privacy.html)

![](//cdn.logly.co.jp/recommend/qiita-image-store.s3.amazonaws.com/a4ad84cb6113002e202d688bfd8ace28.webp?1748836684&oe=jpeg)

[ 開発環境をDockerに乗せる方法とメリットを3ステップで学ぶチュートリアル ](https://qiita.com/KeitaMoromizato/items/ae1a57fc62b41b942d71) by KeitaMoromizato![](//b.logly.co.jp/abc?ac=62t-dwZLZRc_58jiBA5gXA&pt=1&sp=4279493&st=https%3A%2F%2Fqiita.com&lg=similarity&wd=10661&rd=&ct=4)

![](//cdn.logly.co.jp/recommend/s3-ap-northeast-1.amazonaws.com/1d9d213e8c72e3546bf4a843517556fb.webp?1751341637&oe=png)

[ DockerでReactの開発環境を作る ](https://qiita.com/tanaka-tt/items/49628cd423e490120eeb) by tanaka-tt

![](//cdn.logly.co.jp/recommend/qiita-image-store.s3.amazonaws.com/3e4437912a73cf83e97e590ebc59ffaa.webp?1751337780&oe=png)

[ 【入門】DockerでRuby on Rails + PostgreSQL + React + Ty... ](https://qiita.com/takano-h/items/84ae73b41eef83602bd9) by takano-h

![](//cdn.logly.co.jp/recommend/qiita-image-store.s3.amazonaws.com/0e09ce13078c72c88a1494d7c065675c.webp?1748783151&oe=jpeg)

[ Docker-composeを使ってnode.jsの環境構築をしてみたのよ。 ](https://qiita.com/art_porokyu/items/8363334c358c67adb61a) by art_porokyu

## Comments

No comments

Let's comment your feelings that are more than good

[Login](/login?callback_action=login_or_signup&redirect_to=https%3A%2F%2Fqiita.com%2FSicut_study%2Fitems%2F4f301d000ecee98e78c9&realm=qiita)[Sign Up](/signup?callback_action=login_or_signup&redirect_to=https%3A%2F%2Fqiita.com%2FSicut_study%2Fitems%2F4f301d000ecee98e78c9&realm=qiita)

[1155](/Sicut_study/items/4f301d000ecee98e78c9/likers)

Go to list of users who liked

1344

more_horiz

Delete article

close

Deleted articles cannot be recovered.

Draft of this article would be also deleted.

Are you sure you want to delete this article?

CancelDeletedelete

## Login to continue?

### Login or Sign up with social account

Login or Sign up with GitHub Login or Sign up with Google Login or Sign up with X(Twitter)

### Login or Sign up with your email address

[Login with your email addresslogin](/login?callback_action=login_or_signup&redirect_to=%2FSicut_study%2Fitems%2F4f301d000ecee98e78c9&realm=qiita)[Sign up with your email addressperson_add](/signup?callback_action=login_or_signup&redirect_to=%2FSicut_study%2Fitems%2F4f301d000ecee98e78c9&realm=qiita)

close![](//cdn.qiita.com/assets/public/image-qiitan_for_login_modal_glimpse-c148ec9e4debf1f4b880deec194b6fc8.png)
