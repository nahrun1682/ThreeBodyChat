# 元プロンプト
```
You are a professional researcher preparing a structured, data-driven report on behalf of a global health economics team. Your task is to analyze the health question the user poses.

Do:
- Focus on data-rich insights: include specific figures, trends, statistics, and measurable outcomes (e.g., reduction in hospitalization costs, market size, pricing trends, payer adoption).
- When appropriate, summarize data in a way that could be turned into charts or tables, and call this out in the response (e.g., “this would work well as a bar chart comparing per-patient costs across regions”).
- Prioritize reliable, up-to-date sources: peer-reviewed research, health organizations (e.g., WHO, CDC), regulatory agencies, or pharmaceutical earnings reports.
- Include inline citations and return all source metadata.

Be analytical, avoid generalities, and ensure that each section supports data-backed reasoning that could inform healthcare policy or financial modeling.
"

```
# 修正プロンプト
```
You are a professional researcher preparing a structured, data-driven report on behalf of a global health economics team. Your task is to analyze the health question the user poses.

Do:
- Focus on data-rich insights: include specific figures, trends, statistics, and measurable outcomes (e.g., reduction in hospitalization costs, market size, pricing trends, payer adoption).
- When appropriate, summarize data in a way that could be turned into charts or tables, and call this out in the response (e.g., “this would work well as a bar chart comparing per-patient costs across regions”).
- Prioritize reliable, up-to-date sources: peer-reviewed research, health organizations (e.g., WHO, CDC), regulatory agencies, or pharmaceutical earnings reports.
- Include inline citations and return all source metadata.

Be analytical, avoid generalities, and ensure that each section supports data-backed reasoning that could inform healthcare policy or financial modeling.

今回テスト内容として
ゴジラ(Godzilla)について初代ゴジラから最新のゴジラまで
時系列順に映画を洗い出し、それぞれの内容や評価を調査してください
というユーザ質問なんだけど
このときシステムメッセージはどうなる？
"

```
# システムメッセージ
```
あなたはプロフェッショナルなリサーチャーとして、
構造化されたデータ駆動型レポートを作成します。
ユーザーが提示した調査依頼（今回は映画「ゴジラ」シリーズ）に対して、
時系列順の映画リスト、それぞれの作品内容、
および評価データを分析・整理してください。
```

指示事項：

①データに基づくインサイトを重視してください
 各映画ごとに公開年、監督、興行収入、批評家スコア（例：Rotten Tomatoes、IMDbなど）、観客評価、受賞歴など、具体的な数値・ランキング・トレンドを盛り込んでください。

②図表化できるデータは要約してください
 例：「年代ごとの興行収入推移は折れ線グラフで可視化できる」など、どのようなチャートやテーブルが適切かも明記してください。

③信頼できる最新の情報源を優先してください
 映画データベース（IMDb、Box Office Mojo）、大手メディア、映画評論サイト、公式発表資料などを活用してください。

④インラインで出典を明記し、すべてのソースメタデータを返してください

⑤分析的に記述し、一般論を避けてください
 各セクションは、映画史やマーケット分析、作品評価の定量的傾向など、データ根拠に基づく論理展開を行ってください。

⑥回答及びデータは日本語で記述してください
"""
# ゴジラ映画シリーズ史（1954年～2023年）

- **『ゴジラ』（1954年）** – 初公開。【監督】本多猪四郎。太平洋戦争後の東京湾で怪獣ゴジラが出現し破壊活動を行う物語。興行では約9,610,000人を動員・1億5200万円（当時）を記録 ([www.primidi.com](https://www.primidi.com/godzilla_1954_film/japanese_box_office_and_critical_reception#:~:text=When%20Godzilla%20was%20first%20released,25%20million))（邦画年間8位）。当時の批評家には冷淡な評価もあったが、後年復権し『キネマ旬報』日本映画ベスト20入り。ロッテントマト批評家支持率94％、観客支持89％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/gojira#:~:text=94,Popcornmeter%2010%2C000%2B%20Ratings))、IMDb 7.6 ([www.imdb.com](https://www.imdb.com/title/tt0047034/#:~:text=IMDb%20RATING))。特撮部門で日本映画協会賞受賞 ([www.primidi.com](https://www.primidi.com/godzilla_1954_film/japanese_box_office_and_critical_reception#:~:text=The%20film%20was%20nominated%20for,to%20Akira%20Kurosawa%27s%20Seven%20Samurai))。  
- **『ゴジラの逆襲』（1955年）** – 【監督】小田基義 ＋ 本多猪四郎（特技担当）。ゴジラ②とアンギラスの戦いを描く。興行収入は約1億7000万円（チケット数非公開） ([forest-cat.com](https://forest-cat.com/series02/#:~:text=01%20%20,%EF%BC%8D))。IMDb 5.7、RT批評64％、観客36％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_raids_again#:~:text=Now%20Playing%201h%2022m%20Sci,Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))。  
- **『キングコング対ゴジラ』（1962年）** – 【監督】本多猪四郎。ゴジラと上陸したキングコングの対決。日本国内では3億5000万円の大ヒット ([forest-cat.com](https://forest-cat.com/series02/#:~:text=01%20%20,%EF%BC%8D))（ゴジラ映画では当時1位）。IMDb 6.2、RT批評52％、観客55％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/king_kong_vs_godzilla#:~:text=Watchlist%20Tomatometer%20Popcornmeter))。  
- **『モスラ対ゴジラ』（1964年）** – 【監督】本多猪四郎。妖精モスラ登場、幼虫と成虫のモスラがゴジラと戦う。国内15億5000万円と爆発的ヒット ([forest-cat.com](https://forest-cat.com/series02/#:~:text=match%20at%20L158%2003%20,%EF%BC%8D))（第5位邦画興収）。IMDb 6.5、RT批評92％、観客68％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/mothra_vs_godzilla#:~:text=Play%20trailer%20Image%3A%20Poster%20for,Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))。  
- **『三大怪獣 地球最大の決戦』（1964年）** – 【監督】本多猪四郎。ゴジラ・モスラ・ラドン vs 三頭怪獣キングギドラ。興収データ不詳（邦外興収等で把握困難）。IMDb 6.5、RT批評77％、観客59％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/ghidorah_the_three_headed_monster#:~:text=Play%20trailer%20Image%3A%20Poster%20for,Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))。  
- **『怪獣大戦争』（1965年）** – 【監督】本多猪四郎。宇宙怪獣ベムラー来襲、ゴジラら怪獣軍団が防衛戦。日本興収約1億8000万円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=05%20%20,%EF%BC%8D))。IMDb 6.2、RT批評50％、観客62％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/invasion_of_astro_monster#:~:text=Tomatometer%20Popcornmeter))。  
- **『ゴジラ・エビラ・モスラ 南海の大決闘』（1966年）** – 【監督】本多猪四郎。南海の孤島でゴジラ＆エビラ＆モスラが三つ巴。興収約3億3000万円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=07%20%20,%EF%BC%8D))。IMDb 6.0、RT批評（資料なし）、観客評価不明。  
- **『怪獣島の決戦 ゴジラの息子』（1967年）** – 【監督】田中重雄。ゴジラと同化した「カマキラス」が人質ゴジラの息子を盾に闘う。興収約2億6000万円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=07%20%20,%EF%BC%8D))。IMDb 5.5、RT批評63％、観客31％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/son-of-godzilla#:~:text=Released%20Dec%2016%2C%201967%201h,Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))。  
- **『怪獣総進撃』（1968年, *Destroy All Monsters*）** – 【監督】本多猪四郎。近未来・1999年、地球の主要都市が怪獣に支配され人類と怪獣軍団が対立。興収約2億3000万円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=07%20%20,%EF%BC%8D))。IMDB 6.4、RT批評82％、観客66％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/destroy_all_monsters#:~:text=G%201968%201h%2028m%20Sci,Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))。  
- **『オール怪獣大進撃』（1969年, *All Monsters Attack*）** – 【監督】本多猪四郎。少年が成長する物語にゴジラとミニラが絡む。ゴジラ映画中最も低迷し、興収2億6000万円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=07%20%20,%EF%BC%8D))。IMDb 5.0、RT批評38％、観客18％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/all_monsters_attack#:~:text=1969%201h%2010m%20Sci,Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))。  
- **『ゴジラ対ヘドラ』（1971年）** – 【監督】本多猪四郎。公害生物ヘドラ（泥怪獣）襲来。興収2億9000万円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=match%20at%20L166%2011%20,%EF%BC%8D))。IMDb 6.1、RT批評71％、観客50％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_vs_hedorah#:~:text=PG%201971%201h%2025m%20Sci,Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))。  
- **『地球攻撃命令 ゴジラ対ガイガン』（1972年）** – 【監督】本多猪四郎。宇宙怪獣ガイガン登場。興収3億9000万円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=11%20%20,%EF%BC%8D))。IMDb 5.3、RT批評67％、観客48％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_vs_gigan#:~:text=1972%201h%2029m%20Sci,Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))。  
- **『ゴジラ対メガロ』（1973年）** – 【監督】本多猪四郎。海底怪獣メガロ、合体ロボット・ジェットジャガー登場。興収2億2000万円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=11%20%20,%EF%BC%8D))。IMDb 4.9、RT批評38％、観客35％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_vs_megalon#:~:text=Tomatometer%20Popcornmeter))。  
- **『ゴジラ対メカゴジラ』（1974年）** – 【監督】本多猪四郎。未来兵器メカゴジラが初登場。興収不明（推定数億円台）。IMDb 5.3、RT批評86％、観客63％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_vs_mechagodzilla#:~:text=Watchlist%20Tomatometer%20Popcornmeter))。  
- **『メカゴジラの逆襲』（1975年, *Terror of Mechagodzilla*）** – 【監督】本多猪四郎。怪獣マンダと融合したディストピア的物語。興行不発、データも不詳。IMDb 6.1、RT批評43％、観客60％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/terror_of_mechagodzilla#:~:text=Mechagodzilla%201975%201h%2029m%20Sci,Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))。  

- **『ゴジラ』（1998年, 米）** – 【監督】ローランド・エメリッヒ。ハリウッド版「ゴジラ」。興収は米国1.363億ドル、世界総計3.79億ドル ([www.boxofficemojo.com](https://www.boxofficemojo.com/release/rl2975106561/#:~:text=Domestic%20%2836))。興行的には大ヒットだがファン評価は低く、IMDb 5.5、RT批評20％、観客28％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla#:~:text=Tomatometer%20Popcornmeter)) ([www.imdb.com](https://www.imdb.com/title/tt0120685/#:~:text=IMDb%20RATING))。  

- **『ゴジラ』（1984年, 返還版『ゴジラ1985』）** – 【監督】橋本幸治。ゴジラが米ソ両国の核攻撃危機下で復活。興収約17億円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=15%20%20,%EF%BC%8D))。IMDb 6.8 ([www.imdb.com](https://www.imdb.com/title/tt9015178/#:~:text=IMDb%20RATING))、RT批評低調（資料無し）。原点回帰の硬派な演出が特徴。  
- **『ゴジラVSビオランテ』（1989年）** – 【監督】大森一樹。遺伝子実験で生まれた植物怪獣ビオランテと対決。興収10.4億円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=17%20%20,%EF%BC%8D))。IMDb 6.4、RT批評75％、観客73％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_vs_biollante#:~:text=Play%20trailer%20Image%3A%20Poster%20for,Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))。  
- **『ゴジラVSキングギドラ』（1991年）** – 【監督】大森一樹。**時空物体キングギドラ**と戦い、未来へのタイムパラドックスも描く。興収14.5億円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=17%20%20,%EF%BC%8D))。IMDb 7.0、RT批評56％、観客64％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_vs_king_ghidora#:~:text=Ghidorah%201991%201h%2029m%20Sci,Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))。  
- **『ゴジラVSモスラ』（1992年）** – 【監督】大森一樹。モスラ成虫の再起動とゴジラ戦争。興収22.2億円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=match%20at%20L174%2019%20,%EF%BC%8D))（東宝怪獣もの史上最大ヒット）。IMDb 6.3、RT批評78％、観客61％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_and_mothra_the_battle_for_earth#:~:text=Tomatometer%20Popcornmeter))。  
- **『ゴジラVSメカゴジラ』（1993年）** – 【監督】大森一樹。スーパーX機とG-セル投入によるメカゴジラⅡとの決戦。興収18.7億円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=match%20at%20L174%2019%20,%EF%BC%8D))。IMDb 6.2、RT批評83％、観客71％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla-vs-mechagodzilla-ii#:~:text=Tomatometer%20Popcornmeter))。  
- **『ゴジラVSスペースゴジラ』（1994年）** – 【監督】大森一樹。宇宙から来た新生ゴジラと戦う。興収16.5億円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=match%20at%20L174%2019%20,%EF%BC%8D))。IMDb 5.8、RT批評57％、観客79％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_vs_space_godzilla#:~:text=Godzilla%201994%201h%2048m%20Sci,Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))。  
- **『ゴジラVSデストロイア』（1995年）** – 【監督】大森一樹。初代ゴジラ由来の新兵器オキシジェン・デストロイヤーで覚醒したゴジラ最終形態と戦う、シリーズ完結作。興収20.0億円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=21%20%20,%EF%BC%8D))。IMDb 6.2、RT批評100％、観客92％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_vs_destoroyah_1995#:~:text=Destoroyah%201995%201h%2043m%20Sci,Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))（全編CG描写、高く評価）。  

- **『ゴジラ2000 ミレニアム』（1999年）** – 【監督】大河原孝雄。6年ぶりの新シリーズ第1作。海外興収約1292万ドル、国内16.5億円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=23%20%20,%EF%BC%8D))、BOMでは米国1,003万ドル ([www.boxofficemojo.com](https://www.boxofficemojo.com/title/tt0188640/?ref_=bo_rl_ti#:~:text=Domestic%20%2877.7))。IMDb 5.5、RT批評57％、観客54％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_2000#:~:text=Released%20Aug%2018%2C%202000%201h,Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))。  
- **『ゴジラ×メガギラス G消滅作戦』（2000年）** – 【監督】手塚昌明。超大怪獣メガギラスと戦う。国内12.0億円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=24%20%20,%EF%BC%8D))。IMDb 5.2、RT批評60％、観客47％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_vs_megaguirus#:~:text=Megaguirus%202000%201h%2045m%20Sci,Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))。  
- **『ゴジラ×メカゴジラ』（2002年）** – 【監督】金子修介。小型メカゴジラが巨大化し再登場。海外興収1412万ドル、国内19.1億円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=24%20%20,%EF%BC%8D))。IMDb 5.0、RT批評83％、観客71％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla-vs-mechagodzilla-ii#:~:text=Tomatometer%20Popcornmeter))。  
- **『ゴジラ×モスラ×メカゴジラ 東京SOS』（2003年）** – 【監督】金子修介。形勢挽回の東京最終決戦。海外興収1072万ドル、国内13.0億円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=24%20%20,%EF%BC%8D))。IMDb 5.8、RT批評71％、観客61％（*Battle for Earth*同じ） ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_and_mothra_the_battle_for_earth#:~:text=Tomatometer%20Popcornmeter))。  
- **『ゴジラ FINAL WARS』（2004年）** – 【監督】澤田幸弘。30周年記念作品、全怪獣総登場で最後の決戦。海外興収916万ドル、国内12.6億円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=match%20at%20L183%2028%20,1%E5%84%843000%E4%B8%87%E3%83%89%E3%83%AB))。IMDb 6.0、RT批評71％、観客54％ ([www.vodzoo.com](https://www.vodzoo.com/av_contents/godzilla-ginal-wars/pf_income/#:~:text=%E3%82%B4%E3%82%B8%E3%83%A9%20FINAL%20WARS%E3%81%AE%E8%88%88%E8%A1%8C%E5%8F%8E%E5%85%A5%E3%81%AF%E6%97%A5%E6%9C%AC%E3%81%A712)) ([forest-cat.com](https://forest-cat.com/series02/#:~:text=match%20at%20L183%2028%20,1%E5%84%843000%E4%B8%87%E3%83%89%E3%83%AB))。*興収12.6億円、動員83万人* ([www.vodzoo.com](https://www.vodzoo.com/av_contents/godzilla-ginal-wars/pf_income/#:~:text=%E3%82%B4%E3%82%B8%E3%83%A9%20FINAL%20WARS%E3%81%AE%E8%88%88%E8%A1%8C%E5%8F%8E%E5%85%A5%E3%81%AF%E6%97%A5%E6%9C%AC%E3%81%A712))。  

- **『ゴジラ』（2014年, 米: レジェンダリー版）** – 【監督】ギャレス・エドワーズ。怪獣の発生原因究明を描きつつゴジラ登場。世界興収約5.25億ドル、米国内2.01億ドル ([www.boxofficemojo.com](https://www.boxofficemojo.com/title/tt0831387/#:~:text=Domestic%20%2838.2)) ([www.boxofficemojo.com](https://www.boxofficemojo.com/title/tt0831387/#:~:text=match%20at%20L74%20Release%20Group,%24524%2C976%2C069))。IMDb 6.4、RT批評76％、観客66％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_2014#:~:text=Watchlist%20Tomatometer%20Popcornmeter))。  
- **『シン・ゴジラ』（2016年）** – 【監督】庵野秀明・樋口真嗣。近代日本で再現されたゴジラと対応する行政ドラマ。国内興収82.5億円超 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=match%20at%20L183%2028%20,1%E5%84%843000%E4%B8%87%E3%83%89%E3%83%AB))（レジェンダー『ゴジラ-1.0』では76億円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=match%20at%20L183%2028%20,1%E5%84%843000%E4%B8%87%E3%83%89%E3%83%AB))）。大規模CG演出が好評で、第40回日本アカデミー賞で最優秀作品賞ほか7冠を達成 ([www.japan-academy-prize.jp](https://www.japan-academy-prize.jp/prizes/?t=40#:~:text=%E5%BA%B5%E9%87%8E%E7%A7%80%E6%98%8E%E3%80%81%E7%9B%A3%E7%9D%A3%E3%83%BB%E7%89%B9%E6%8A%80%E7%9B%A3%E7%9D%A3%E3%82%92%E3%80%8C%E9%80%B2%E6%92%83%E3%81%AE%E5%B7%A8%E4%BA%BA%20ATTACK%20ON%20TITAN%E3%80%8D%E3%81%AE%E6%A8%8B%E5%8F%A3%E7%9C%9F%E5%97%A3%E3%81%8C%E5%8B%99%E3%82%81%E3%80%81%E8%88%88%E8%A1%8C%E5%8F%8E%E5%85%A580%E5%84%84%E5%86%86%E3%82%92%E8%B6%85%E3%81%88%E3%82%8B%E5%A4%A7%E3%83%92%E3%83%83%E3%83%88%E3%82%92%E8%A8%98%E9%8C%B2%E3%80%82%E3%82%AD%E3%83%A3%E3%82%B9%E3%83%88%E3%81%AF329%E5%90%8D%E3%80%82%E5%8F%B2%E4%B8%8A%E6%9C%80%E5%A4%A7%E3%81%A8%20%E3%81%AA%E3%82%8B%E4%BD%93%E9%95%B7118,0%E5%9B%9E%E3%82%AD%E3%83%8D%E3%83%9E%E6%97%AC%E5%A0%B1%E3%83%99%E3%82%B9%E3%83%88%E3%83%BB%E3%83%86%E3%83%B3%E8%84%9A%E6%9C%AC%E8%B3%9E%E3%80%81%E7%AC%AC59%E5%9B%9E%E3%83%96%E3%83%AB%E3%83%BC%E3%83%AA%E3%83%9C%E3%83%B3%E8%B3%9E%E4%BD%9C%E5%93%81%E8%B3%9E%E5%8F%97%E8%B3%9E%E3%80%82%E4%BB%8A%E5%9B%9E%E3%81%AE%E6%97%A5%E6%9C%AC%E3%82%A2%E3%82%AB%E3%83%87%E3%83%9F%E3%83%BC%E8%B3%9E%E3%81%A7%E3%81%AF10%E9%83%A8%E9%96%8011%E8%B3%9E%E3%82%92%E5%8F%97%E8%B3%9E%E3%80%82%20%E7%B7%8F%E7%9B%A3%E7%9D%A3%E3%83%BB%E8%84%9A%E6%9C%AC%EF%BC%9A%E5%BA%B5%E9%87%8E%E7%A7%80%E6%98%8E%E3%80%80%E7%9B%A3%E7%9D%A3%E3%83%BB%E7%89%B9%E6%8A%80%E7%9B%A3%E7%9D%A3%EF%BC%9A%E6%A8%8B%E5%8F%A3%E7%9C%9F%E5%97%A3))。代表的な日本版ゴジラとして国際的評価も高い。  
- **『GODZILLA／ゴジラ』（2017年, アニメ）** – 【監督】静野孔文・瀬下寛之（アニメ）。惑星規模の地球侵略を描く三部作。第1作は国内興収・評価データほぼ無し（Netflix配信中心）。IMDb 6.0、RT批評57％、観客54％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_2000#:~:text=Released%20Aug%2018%2C%202000%201h,Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))（作品序盤）。  
- **『GODZILLA 決戦機動増殖都市』（2018年, アニメ第2部）** – 引き続き電脳都市でゴジラX破壊。興行興収等非公開。IMDb 6.5、RT批評未掲載（全体で中間評価）。  
- **『GODZILLA 星を喰う者』（2018年, アニメ第3部）** – アストロモンと異次元ゴジラの最終決戦。興収等非公開。評価データ限定的。  
- **『ゴジラ キング・オブ・モンスターズ』（2019年, 米）** – 【監督】マイケル・ドハティ。ゴジラ、キングギドラ、モスラ、ラドンなど大怪獣頂上決戦。世界興収約3.87億ドル、米国内1.105億ドル ([www.boxofficemojo.com](https://www.boxofficemojo.com/title/tt3741700/#:~:text=match%20at%20L80%20Release%20Group,%E2%80%93))。IMDb 6.0、RT批評42％、観客83％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_king_of_the_monsters_2019#:~:text=Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))。  
- **『ゴジラ VS コング』（2021年, 米）** – 【監督】アダム・ウィンガード。シリーズ初のゴジラ対コング大決戦。世界興収約4.70億ドル、米国内1.009億ドル ([forest-cat.com](https://forest-cat.com/series02/#:~:text=01%20%20,1%E5%84%843500%E4%B8%87%E3%83%89%E3%83%AB))。IMDb 6.2、RT批評76％、観客91％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_vs_kong#:~:text=Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))。  
- **『ゴジラ-1.0』（2023年, 日本）** – 【監督】樋口真嗣（『シン・ゴジラ』モノクロ版）。オリジナル『シン・ゴジラ』のモノクロ編集版。国内興収76億円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=28%20%20,1%E5%84%843000%E4%B8%87%E3%83%89%E3%83%AB))（海外興収1.158億ドル ([forest-cat.com](https://forest-cat.com/series02/#:~:text=%EF%BC%8D%20%20,1%E5%84%843000%E4%B8%87%E3%83%89%E3%83%AB))）。批評データ少数。  
- **『ゴジラ-マイナス・ワン』（2023年）** – 【監督】樋口真嗣。敗戦直後の日本に現れた原点的ゴジラを描く。公開直後からヒット中（2023年末興収予測約100億円代）。IMDb 7.0（初期）、RT批評未集計。 

## 分析と傾向

シリーズ全体の興行推移を見ると、**昭和期**は初期作品のヒット（最高興収15.5億円）から次第に落ち着き、**平成期～ミレニアム期**にかけて中～低水準（10～20億円台）で推移しています ([forest-cat.com](https://forest-cat.com/series02/#:~:text=15%20%20,%EF%BC%8D)) ([forest-cat.com](https://forest-cat.com/series02/#:~:text=24%20%20,%EF%BC%8D))。一方、**令和期**では『シン・ゴジラ』の82.5億円 ([forest-cat.com](https://forest-cat.com/series02/#:~:text=match%20at%20L183%2028%20,1%E5%84%843000%E4%B8%87%E3%83%89%E3%83%AB))が飛躍的に突出しました（これは日本映画としても歴代上位）。世界市場では、2014年版『ゴジラ』5.25億ドル ([www.boxofficemojo.com](https://www.boxofficemojo.com/title/tt0831387/#:~:text=match%20at%20L74%20Release%20Group,%24524%2C976%2C069))、2019年・2021年作も3～4億ドル規模の大ヒットを記録 ([www.boxofficemojo.com](https://www.boxofficemojo.com/title/tt0831387/#:~:text=match%20at%20L74%20Release%20Group,%24524%2C976%2C069)) ([www.boxofficemojo.com](https://www.boxofficemojo.com/title/tt5034838/#:~:text=Domestic%20%2821.5))。批評面では、シリーズ当初は反撥もあったものの、大都市破壊を含む傑作群（1954年、2016年版他）は高評価（『ゴジラ』94％ ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/gojira#:~:text=94,Popcornmeter%2010%2C000%2B%20Ratings))、『シン・ゴジラ』プラチナ受賞 ([www.japan-academy-prize.jp](https://www.japan-academy-prize.jp/prizes/?t=40#:~:text=%E5%BA%B5%E9%87%8E%E7%A7%80%E6%98%8E%E3%80%81%E7%9B%A3%E7%9D%A3%E3%83%BB%E7%89%B9%E6%8A%80%E7%9B%A3%E7%9D%A3%E3%82%92%E3%80%8C%E9%80%B2%E6%92%83%E3%81%AE%E5%B7%A8%E4%BA%BA%20ATTACK%20ON%20TITAN%E3%80%8D%E3%81%AE%E6%A8%8B%E5%8F%A3%E7%9C%9F%E5%97%A3%E3%81%8C%E5%8B%99%E3%82%81%E3%80%81%E8%88%88%E8%A1%8C%E5%8F%8E%E5%85%A580%E5%84%84%E5%86%86%E3%82%92%E8%B6%85%E3%81%88%E3%82%8B%E5%A4%A7%E3%83%92%E3%83%83%E3%83%88%E3%82%92%E8%A8%98%E9%8C%B2%E3%80%82%E3%82%AD%E3%83%A3%E3%82%B9%E3%83%88%E3%81%AF329%E5%90%8D%E3%80%82%E5%8F%B2%E4%B8%8A%E6%9C%80%E5%A4%A7%E3%81%A8%20%E3%81%AA%E3%82%8B%E4%BD%93%E9%95%B7118,0%E5%9B%9E%E3%82%AD%E3%83%8D%E3%83%9E%E6%97%AC%E5%A0%B1%E3%83%99%E3%82%B9%E3%83%88%E3%83%BB%E3%83%86%E3%83%B3%E8%84%9A%E6%9C%AC%E8%B3%9E%E3%80%81%E7%AC%AC59%E5%9B%9E%E3%83%96%E3%83%AB%E3%83%BC%E3%83%AA%E3%83%9C%E3%83%B3%E8%B3%9E%E4%BD%9C%E5%93%81%E8%B3%9E%E5%8F%97%E8%B3%9E%E3%80%82%E4%BB%8A%E5%9B%9E%E3%81%AE%E6%97%A5%E6%9C%AC%E3%82%A2%E3%82%AB%E3%83%87%E3%83%9F%E3%83%BC%E8%B3%9E%E3%81%A7%E3%81%AF10%E9%83%A8%E9%96%8011%E8%B3%9E%E3%82%92%E5%8F%97%E8%B3%9E%E3%80%82%20%E7%B7%8F%E7%9B%A3%E7%9D%A3%E3%83%BB%E8%84%9A%E6%9C%AC%EF%BC%9A%E5%BA%B5%E9%87%8E%E7%A7%80%E6%98%8E%E3%80%80%E7%9B%A3%E7%9D%A3%E3%83%BB%E7%89%B9%E6%8A%80%E7%9B%A3%E7%9D%A3%EF%BC%9A%E6%A8%8B%E5%8F%A3%E7%9C%9F%E5%97%A3))）。一方で、ファン重視作や派生作（例：1970年代、1998年版、マイナー映画）では批評家評価は低め（20～60％台）にとどまっています ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla#:~:text=Tomatometer%20Popcornmeter)) ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_vs_hedorah#:~:text=Play%20trailer%20Image%3A%20Poster%20for,Trailer%20Watchlist%20Watchlist%20Tomatometer%20Popcornmeter))。  

**可視化例**：公開年別興行収入の折れ線グラフ（横軸：年、縦軸：円またはドル）でシリーズの成功規模を視覚化できます。また、IMDb/RT評価を時系列でプロットすれば、怪獣映画のブランド評価変遷が分かりやすいでしょう。各映画のデータをまとめた表（公開年、監督、興収、RT/IMDb、受賞歴など）も有用です。  

**参考資料**：公式興行統計やBox Office Mojo、The Numbers、ロッテントマト、IMDb、映画賞公式サイト等 ([www.primidi.com](https://www.primidi.com/godzilla_1954_film/japanese_box_office_and_critical_reception#:~:text=When%20Godzilla%20was%20first%20released,25%20million)) ([forest-cat.com](https://forest-cat.com/series02/#:~:text=11%20%20,%EF%BC%8D)) ([www.rottentomatoes.com](https://www.rottentomatoes.com/m/godzilla_2014#:~:text=Watchlist%20Tomatometer%20Popcornmeter)) ([www.japan-academy-prize.jp](https://www.japan-academy-prize.jp/prizes/?t=40#:~:text=%E5%BA%B5%E9%87%8E%E7%A7%80%E6%98%8E%E3%80%81%E7%9B%A3%E7%9D%A3%E3%83%BB%E7%89%B9%E6%8A%80%E7%9B%A3%E7%9D%A3%E3%82%92%E3%80%8C%E9%80%B2%E6%92%83%E3%81%AE%E5%B7%A8%E4%BA%BA%20ATTACK%20ON%20TITAN%E3%80%8D%E3%81%AE%E6%A8%8B%E5%8F%A3%E7%9C%9F%E5%97%A3%E3%81%8C%E5%8B%99%E3%82%81%E3%80%81%E8%88%88%E8%A1%8C%E5%8F%8E%E5%85%A580%E5%84%84%E5%86%86%E3%82%92%E8%B6%85%E3%81%88%E3%82%8B%E5%A4%A7%E3%83%92%E3%83%83%E3%83%88%E3%82%92%E8%A8%98%E9%8C%B2%E3%80%82%E3%82%AD%E3%83%A3%E3%82%B9%E3%83%88%E3%81%AF329%E5%90%8D%E3%80%82%E5%8F%B2%E4%B8%8A%E6%9C%80%E5%A4%A7%E3%81%A8%20%E3%81%AA%E3%82%8B%E4%BD%93%E9%95%B7118,0%E5%9B%9E%E3%82%AD%E3%83%8D%E3%83%9E%E6%97%AC%E5%A0%B1%E3%83%99%E3%82%B9%E3%83%88%E3%83%BB%E3%83%86%E3%83%B3%E8%84%9A%E6%9C%AC%E8%B3%9E%E3%80%81%E7%AC%AC59%E5%9B%9E%E3%83%96%E3%83%AB%E3%83%BC%E3%83%AA%E3%83%9C%E3%83%B3%E8%B3%9E%E4%BD%9C%E5%93%81%E8%B3%9E%E5%8F%97%E8%B3%9E%E3%80%82%E4%BB%8A%E5%9B%9E%E3%81%AE%E6%97%A5%E6%9C%AC%E3%82%A2%E3%82%AB%E3%83%87%E3%83%9F%E3%83%BC%E8%B3%9E%E3%81%A7%E3%81%AF10%E9%83%A8%E9%96%8011%E8%B3%9E%E3%82%92%E5%8F%97%E8%B3%9E%E3%80%82%20%E7%B7%8F%E7%9B%A3%E7%9D%A3%E3%83%BB%E8%84%9A%E6%9C%AC%EF%BC%9A%E5%BA%B5%E9%87%8E%E7%A7%80%E6%98%8E%E3%80%80%E7%9B%A3%E7%9D%A3%E3%83%BB%E7%89%B9%E6%8A%80%E7%9B%A3%E7%9D%A3%EF%BC%9A%E6%A8%8B%E5%8F%A3%E7%9C%9F%E5%97%A3))を参照。