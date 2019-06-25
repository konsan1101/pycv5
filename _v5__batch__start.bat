@ECHO OFF

c:
cd c:\pycv5

taskkill /im python.exe /f       >nul
taskkill /im adintool-gui.exe /f >nul
taskkill /im adintool.exe /f     >nul
taskkill /im julius.exe /f       >nul

ECHO 起動しますか？
PAUSE
ECHO 起動
start /min _v5__batch_python.bat




ECHO シナリオ開始
PAUSE

ping localhost -w 1000 -n 15 >nul
ECHO busy>temp\_work\busy_dev_microphone.txt
ECHO busy>temp\_work\busy_dev_display.txt



:LOOP

ECHO;
ECHO ja,azure,サープアシスタントＡＩを起動しました。
PAUSE
ECHO ja,azure,サープアシスタントＡＩを起動しました。>temp\a3_5tts_txt\speech00_sjis.txt

ECHO;
ECHO ja,azure,ログイン画面です。
ECHO ja,azure,カメラにＱＲコードをかざすとログインできます。
PAUSE
ECHO ja,azure,ログイン画面です。>temp\a3_5tts_txt\speech10_sjis.txt
ECHO ja,azure,カメラにＱＲコードをかざすとログインできます。>temp\a3_5tts_txt\speech11_sjis.txt

ECHO;
ECHO ja,azure,ログイン記録として写真撮影しました。
ECHO ja,azure,今日の笑顔指数は８０点です。
PAUSE
sox _sound_shutter.mp3 -d
ECHO ja,azure,ログイン記録として写真撮影しました。>temp\a3_5tts_txt\speech15_sjis.txt
ECHO ja,azure,今日の笑顔指数は８０点です。>temp\a3_5tts_txt\speech16_sjis.txt

ECHO;
ECHO ja,azure,おはようございます。近藤光男さん。
ECHO ja,azure,本日最初のログインです。出勤処理も自動的に行いました。
ECHO ja,azure,昨日の締め処理が２件残っています。
ECHO ja,azure,本日の出荷件数は２８件です。
ECHO ja,azure,承認申請が３件届いています。
ECHO ja,azure,午後１４時に現場視察の予定があります。
ECHO ja,azure,よろしくお願いします。
PAUSE
ECHO ja,azure,おはようございます。近藤光男さん。>temp\a3_5tts_txt\speech20_sjis.txt
ECHO ja,azure,本日最初のログインです。出勤処理も自動的に行いました。>temp\a3_5tts_txt\speech21_sjis.txt
ECHO ja,azure,昨日の締め処理が２件残っています。>temp\a3_5tts_txt\speech22_sjis.txt
ECHO ja,azure,本日の出荷件数は２８件です。>temp\a3_5tts_txt\speech23_sjis.txt
ECHO ja,azure,承認申請が３件届いています。>temp\a3_5tts_txt\speech24_sjis.txt
ECHO ja,azure,午後１４時に現場視察の予定があります。>temp\a3_5tts_txt\speech25_sjis.txt
ECHO ja,azure,よろしくお願いします。>temp\a3_5tts_txt\speech26_sjis.txt

ECHO;
ECHO ja,azure,検索キーワードの音声入力ができます。どうぞ。
PAUSE
ECHO ja,azure,検索キーワードの音声入力ができます。どうぞ。>temp\a3_5tts_txt\speech30_sjis.txt

ping localhost -w 1000 -n 2 >nul
if exist temp\_work\busy_dev_microphone.txt  del temp\_work\busy_dev_microphone.txt

ping localhost -w 1000 -n 30 >nul
ECHO busy>temp\_work\busy_dev_microphone.txt



ECHO;
ECHO ja,azure,カメラを起動しました。タップすると撮影できます。
PAUSE
ECHO ja,azure,カメラを起動しました。タップすると撮影できます。>temp\a3_5tts_txt\speech50_sjis.txt
if exist temp\_work\busy_dev_display.txt  del temp\_work\busy_dev_display.txt



ping localhost -w 1000 -n 30 >nul
ECHO busy>temp\_work\busy_dev_display.txt



ECHO;
ECHO ja,azure,ログオフしました。
ECHO ja,azure,定時を過ぎていますので、退勤処理も自動的に行いました。
ECHO ja,azure,ご安全に。
PAUSE
ECHO ja,azure,ログオフしました。>temp\a3_5tts_txt\speech90_sjis.txt
ECHO ja,azure,定時を過ぎていますので、退勤処理も自動的に行いました。>temp\a3_5tts_txt\speech91_sjis.txt
ECHO ja,azure,ご安全に。>temp\a3_5tts_txt\speech92_sjis.txt

goto LOOP

exit
