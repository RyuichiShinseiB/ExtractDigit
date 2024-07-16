# Extract digit from 7 segments display
## Preparation
### Download
Clone this repository
```bash
git clone https://github.com/RyuichiShinseiB/ExtractDigit.git
```
Or, download zip file
![How_to_download_repository](./refs/images/How_to_download_repository_zip.png)


### Requirements package installing
- pip user
```sh
pip install -r requirements.txt
```
- poetry user
```sh
poetry install
```

## Usage
次のコマンドを実行してください。
```sh
python ./extract_digit/main.py
```
次に、画像一枚を対象に解析するか、対象のフォルダ内の全画像を解析するか、あるいは終了するかを選びます。
選択後、ウィンド画面で解析対象のファイルまたはフォルダを選択します。

## Feature
- [ ] Allow shell scripts to execute it.
## Note
どのセグメントが点灯しているか判断するために次の画像のように、セグメントと番号の対応を付けた。
![各セグメントと番号の対応関係](./refs/images/7segments_display.svg)

表示部分のアスペクト比は4桁の場合>1.7
