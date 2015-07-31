# okumura
for okumra (raspberry pi)

# 導入手順
- gitからソースを落とす
```
git clone https://github.com/ragiko/okumura.git
```
- フォルダ内に音楽(~.mp3, ~.wav)を入れる
- ad.pyの音楽ファイルの名前を変更 (現在はdrop.wavにしてある)

## NOTE
- play_timeは再生時間を表しているので適宜変更
- hdmiに音出力が喰われるので、ライン出力に固定するのがよい
```
# 参考(http://s2jp.com/2013/12/raspberry-pi-sound/)
sudo amixer cset numid=3 1
# test
aplay /usr/share/sounds/alsa/Front_Center.wav
```
