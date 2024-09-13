from lxml import etree, html

# サンプルHTMLを読み込む
html_content = """
<table class="c-table c-table--form rstinfo-table__table">
      <tbody>
        <tr>
          <th>店名</th>
          <td>
            <div class="rstinfo-table__name-wrap">
              <span>黒毛和牛とタンとハラミ 焼肉ごりちゃん 福島店</span>
            </div>
            
          </td>
        </tr>


        <tr>
          <th>ジャンル</th>
          <td>
              <span>焼肉、ホルモン、韓国料理</span>
          </td>
        </tr>
          <tr>
            <th>
                予約・<br>
                お問い合わせ
            </th>
            <td>
                <p class="rstinfo-table__tel-num-wrap">
    <strong class="rstinfo-table__tel-num">050-5589-5224</strong>
    <input type="hidden" name="js-tel-type" id="js-tel-type" value="ppc" autocomplete="off"></p>

            </td>
          </tr>

          <tr>
            <th>予約可否</th>
            <td>
                  <p class="rstinfo-table__reserve-status">予約可</p>
                  <p class="rstinfo-table__reserve-notice">ご予約頂き誠に有難う御座います。<br>注意事項が御座います。<br>ご予約時間の15分過ぎられても、ご連絡がなくお店にご来店がない場合、自動でキャンセルさせて頂きます。ご了承お願い致します。<br>Thank you very much for your reservation.<br>There are precautions.<br>Even if 15 minutes after the reservat</p>
            </td>
          </tr>
        <tr>
          <th>住所</th>
          <td>
                <p class="rstinfo-table__address"><span><a href="/osaka/" class="listlink">大阪府</a></span><span><a href="/osaka/C27103/rstLst/" class="listlink">大阪市福島区</a><a href="/osaka/C27103/C79411/rstLst/" class="listlink">福島</a>5-8-14</span> <span>吉紹ビル 7F</span></p>

              <div class="rstinfo-table__map-wrap">
                <div class="rstinfo-table__map js-catalyst-rstinfo-map">
                    <a href="https://tabelog.com/osaka/A2701/A270108/27130478/dtlmap/"><img alt="黒毛和牛とタンとハラミ 焼肉ごりちゃん 福島店 - 地図" class="js-map-lazyload rstinfo-table__map-image lazy-loaded loaded" data-original="https://maps.googleapis.com/maps/api/staticmap?channel=201000002&amp;key=AIzaSyCFZGUaDWgiusOQeFpnVLT2uPM2R6Mq7J8&amp;hl=ja&amp;center=34.696236337978874,135.4873582774346&amp;style=feature:landscape%7Celement:geometry%7Clightness:25&amp;style=feature:poi%7Celement:geometry%7Clightness:25&amp;style=feature:poi%7Celement:labels.icon%7Ccolor:0xd2d2d2&amp;style=feature:poi%7Celement:labels.text.fill%7Ccolor:0x949499&amp;style=feature:road%7Clightness:25&amp;style=feature:road%7Celement:labels%7Csaturation:-100%7Clightness:40&amp;style=feature:transit.station.airport%7Celement:geometry%7Clightness:25&amp;style=feature:water%7Celement:geometry%7Clightness:25&amp;markers=color:red%7C34.696236337978874,135.4873582774346&amp;zoom=15&amp;size=490x145&amp;signature=Lvegp8RR3JvdVvqv-eDQQr4JH88=" src="https://maps.googleapis.com/maps/api/staticmap?channel=201000002&amp;key=AIzaSyCFZGUaDWgiusOQeFpnVLT2uPM2R6Mq7J8&amp;hl=ja&amp;center=34.696236337978874,135.4873582774346&amp;style=feature:landscape%7Celement:geometry%7Clightness:25&amp;style=feature:poi%7Celement:geometry%7Clightness:25&amp;style=feature:poi%7Celement:labels.icon%7Ccolor:0xd2d2d2&amp;style=feature:poi%7Celement:labels.text.fill%7Ccolor:0x949499&amp;style=feature:road%7Clightness:25&amp;style=feature:road%7Celement:labels%7Csaturation:-100%7Clightness:40&amp;style=feature:transit.station.airport%7Celement:geometry%7Clightness:25&amp;style=feature:water%7Celement:geometry%7Clightness:25&amp;markers=color:red%7C34.696236337978874,135.4873582774346&amp;zoom=15&amp;size=490x145&amp;signature=Lvegp8RR3JvdVvqv-eDQQr4JH88=" data-was-processed="true"></a>
                </div>

                <div class="rstinfo-table__map-link">
                  <span class="rstinfo-table__map-link-item rstinfo-table__map-link-item--bigmap">
                      <a class="js-catalyst-rstinfo-maplink" href="https://tabelog.com/osaka/A2701/A270108/27130478/dtlmap/">大きな地図を見る</a>
                  </span>
                    <span class="rstinfo-table__map-link-item rstinfo-table__map-link-item--peripheral">
                      <a class="js-catalyst-rstinfo-peripheral-maplink" href="https://tabelog.com/osaka/A2701/A270108/27130478/peripheral_map/">周辺のお店を探す</a>
                    </span>
                </div>
              </div>

          </td>
        </tr>
          <tr>
            <th>交通手段</th>
            <td>
              <p>JR福島駅から徒歩3分<br>阪神福島駅から徒歩１分<br>JR新福島駅から徒歩3分</p>
              <p>福島駅から125m</p>
            </td>
          </tr>

        <tr>
          <th>営業時間</th>
          <td>
                <ul class="rstinfo-table__business-list">
                    <li class="rstinfo-table__business-item">
                      <ul class="rstinfo-table__business-dtl is-nolabel">
                          <li class="rstinfo-table__business-dtl-text ">
                            17:00 - 00:00
                              <p>L.O. 料理23:00 ドリンク23:30</p>
                          </li>
                      </ul>
                    </li>
                </ul>

                <div class="rstinfo-table__business-other">
                  <ul class="rstinfo-table__business-list">
                    <li class="rstinfo-table__business-item">■ 定休日<br>不定休※2024年5月7日,8日は店休日</li>
                  </ul>
                </div>
          </td>
        </tr>

          <tr>
            <th>予算</th>
            <td>
              <div class="rstinfo-table__budget">
                  <p class="rstinfo-table__budget-item">
                    <i class="c-rating-v3__time c-rating-v3__time--dinner" aria-label="Dinner" role="img"></i>
                    <em>￥5,000～￥5,999</em>
                  </p>
              </div>
            </td>
          </tr>
        <tr>
          <th>予算<small>（口コミ集計）</small></th>
          <td>
            <div class="rstinfo-table__budget">
                <span class="rstinfo-table__budget-item">
                  <i class="c-rating-v3__time c-rating-v3__time--dinner" aria-label="Dinner" role="img"></i>
                  <em>￥6,000～￥7,999</em>
                </span>
            </div>
              <p class="rstinfo-table__notice">
                <a href="/osaka/A2701/A270108/27130478/dtlratings/#price-range" class="c-link-arrow"><span>利用金額分布を見る</span></a>
              </p>
          </td>
        </tr>
          <tr>
            <th>支払い方法</th>
            <td>
                <div class="rstinfo-table__pay-item">
                  <p>カード可</p>
                    <p class="rstinfo-table__notice">
                      （VISA、Master、JCB、AMEX、Diners）
                    </p>
                </div>
                <div class="rstinfo-table__pay-item">
                  <p class="rstinfo-table__each-info">電子マネー不可</p>
                </div>
                <div class="rstinfo-table__pay-item">
                  <p>QRコード決済可</p>
                    <p class="rstinfo-table__notice">
                    （PayPay、d払い）
                    </p>
                </div>
            </td>
          </tr>

          <tr>
            <th>領収書（適格簡易請求書）</th>
            <td>
              適格請求書（インボイス）対応の領収書発行が可能<br>
              登録番号：T5120001241898<br>
              <p class="rstinfo-table__notice">
                ※最新の登録状況は国税庁インボイス制度適格請求書発行事業者公表サイトをご確認いただくか、店舗にお問い合わせください。
              </p>
            </td>
          </tr>
          <tr>
            <th>サービス料・<br>チャージ</th>
            <td><p>お一人様チャージ代¥110-頂いております</p></td>
          </tr>
      </tbody>
    </table>"""
    

# HTMLをパース
tree = html.fromstring(html_content)


def get_xpath(element):
    """要素のXPATHを取得する関数"""
    components = []
    while element is not None and element.tag is not etree.Comment:
        siblings = element.getparent().findall(
            element.tag) if element.getparent() is not None else []
        if len(siblings) > 1:
            index = siblings.index(element) + 1
            components.append(f"{element.tag}[{index}]")
        else:
            components.append(element.tag)
        element = element.getparent()
    components.reverse()
    return "/" + "/".join(components)


# テーブル内の全ての<td>要素を取得
td_elements = tree.xpath(
    '//table[@class="c-table c-table--form rstinfo-table__table"]//td')

# 各<td>のXPATHを表示
for idx, td in enumerate(td_elements, start=1):
    xpath = get_xpath(td)
    print(f"データ項目 {idx}: {xpath}")
