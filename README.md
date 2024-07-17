# Extract digit from 7 segments display
7セグメントディスプレイから数値を読み取るプログラムです。  \
Note:  \
以下のUsageに書いてあるものは照度計LX1330Bに最適化されたプログラムなので、7セグメントディスプレイに対して行いたい場合はextract_digitのprocessingモジュールとestimateモジュールを活用してプログラムを作成してください。
## Preparation
### Download
このリポジトリをクローンしてください。
```bash
git clone https://github.com/RyuichiShinseiB/ExtractDigit.git
```
あるいは、zipファイルをダウンロード・解凍してください
![How_to_download_repository](./refs/images/How_to_download_repository_zip.png)


### Requirements package installing
- pip を使っている方はこちらを
    ```sh
    pip install -r requirements.txt
    ```
- poetry を使っている方はこちらを
    ```sh
    poetry install
    ```

## Usage
### 解析前
1. ペイントソフトなどでディスプレイ部分を示す四角形の領域の各頂点の位置をメモしておく。
2. ./extract_digit/configs/config.json の以下の`<replace>`部分をメモしていたピクセルの位置に修正する。
```json: config.json
{
    "crop_transform": {
        "crop_area_vertices": {
            "upper_left": {"x": <replace>, "y": <replace>},
            "upper_right": {"x": <replace>, "y": <replace>},
            "lower_right": {"x": <replace>, "y": <replace>},
            "lower_left": {"x": <replace>, "y": <replace>}
        },...
    },...
}
```
### 解析
1. 次のコマンドを実行してください。
```sh
python ./extract_digit/main.py
```
2. 次に、画像一枚を対象に解析するか、対象のフォルダ内の全画像を解析するか、あるいは終了するかを選びます。
3. ウィンド画面で解析対象のファイルまたはフォルダを選択します。  \
    a. フォルダ内全画像の解析を選んだ場合は、続いて保存先のフォルダを選択します。
4. 自動で解析が始まり、検出された数字がコマンドライン上に出力されます。  \
    a. フォルダ内全画像の解析を選んだ場合は、選んだ保存先に"recognized_digits.csv"というファイルも出力されます。

### うまく認識されないとき
./extract_digit/configs/config.json の各パラメータを調整してください。

## TODOs
- config.json の中身の説明を書く。

## Feature
TODOs よりも優先度が低かったり難易度の高いが将来的に追加したい機能や修正点などになります。
- [ ] シェルスクリプトだけで解析できるようにする
- [ ] GUI操作でできるようにする。
    - 特に、最初のクロップする領域をGUI内で指定できるようにしたい。


## Note
### セグメントの位置と番号の対応について
どのセグメントが点灯しているか判断するために次の画像のように、セグメントと番号の対応を付けた。
![各セグメントと番号の対応関係](./refs/images/7segments_display.svg)

