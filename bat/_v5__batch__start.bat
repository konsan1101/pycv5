@ECHO OFF

c:
cd c:\pycv5

taskkill /im python.exe /f       >nul
taskkill /im adintool-gui.exe /f >nul
taskkill /im adintool.exe /f     >nul
taskkill /im julius.exe /f       >nul

ECHO �N�����܂����H
PAUSE
ECHO �N��
start /min _v5__batch_python.bat




ECHO �V�i���I�J�n
PAUSE

ping localhost -w 1000 -n 15 >nul
ECHO busy>temp\_work\busy_dev_microphone.txt
ECHO busy>temp\_work\busy_dev_display.txt



:LOOP

ECHO;
ECHO ja,azure,�T�[�v�A�V�X�^���g�`�h���N�����܂����B
PAUSE
ECHO ja,azure,�T�[�v�A�V�X�^���g�`�h���N�����܂����B>temp\a3_5tts_txt\speech00_sjis.txt

ECHO;
ECHO ja,azure,���O�C����ʂł��B
ECHO ja,azure,�J�����ɂp�q�R�[�h���������ƃ��O�C���ł��܂��B
PAUSE
ECHO ja,azure,���O�C����ʂł��B>temp\a3_5tts_txt\speech10_sjis.txt
ECHO ja,azure,�J�����ɂp�q�R�[�h���������ƃ��O�C���ł��܂��B>temp\a3_5tts_txt\speech11_sjis.txt

ECHO;
ECHO ja,azure,���O�C���L�^�Ƃ��Ďʐ^�B�e���܂����B
ECHO ja,azure,�����̏Ί�w���͂W�O�_�ł��B
PAUSE
sox _sound_shutter.mp3 -d
ECHO ja,azure,���O�C���L�^�Ƃ��Ďʐ^�B�e���܂����B>temp\a3_5tts_txt\speech15_sjis.txt
ECHO ja,azure,�����̏Ί�w���͂W�O�_�ł��B>temp\a3_5tts_txt\speech16_sjis.txt

ECHO;
ECHO ja,azure,���͂悤�������܂��B�ߓ����j����B
ECHO ja,azure,�{���ŏ��̃��O�C���ł��B�o�Ώ����������I�ɍs���܂����B
ECHO ja,azure,����̒��ߏ������Q���c���Ă��܂��B
ECHO ja,azure,�{���̏o�׌����͂Q�W���ł��B
ECHO ja,azure,���F�\�����R���͂��Ă��܂��B
ECHO ja,azure,�ߌ�P�S���Ɍ��ꎋ�@�̗\�肪����܂��B
ECHO ja,azure,��낵�����肢���܂��B
PAUSE
ECHO ja,azure,���͂悤�������܂��B�ߓ����j����B>temp\a3_5tts_txt\speech20_sjis.txt
ECHO ja,azure,�{���ŏ��̃��O�C���ł��B�o�Ώ����������I�ɍs���܂����B>temp\a3_5tts_txt\speech21_sjis.txt
ECHO ja,azure,����̒��ߏ������Q���c���Ă��܂��B>temp\a3_5tts_txt\speech22_sjis.txt
ECHO ja,azure,�{���̏o�׌����͂Q�W���ł��B>temp\a3_5tts_txt\speech23_sjis.txt
ECHO ja,azure,���F�\�����R���͂��Ă��܂��B>temp\a3_5tts_txt\speech24_sjis.txt
ECHO ja,azure,�ߌ�P�S���Ɍ��ꎋ�@�̗\�肪����܂��B>temp\a3_5tts_txt\speech25_sjis.txt
ECHO ja,azure,��낵�����肢���܂��B>temp\a3_5tts_txt\speech26_sjis.txt

ECHO;
ECHO ja,azure,�����L�[���[�h�̉������͂��ł��܂��B�ǂ����B
PAUSE
ECHO ja,azure,�����L�[���[�h�̉������͂��ł��܂��B�ǂ����B>temp\a3_5tts_txt\speech30_sjis.txt

ping localhost -w 1000 -n 2 >nul
if exist temp\_work\busy_dev_microphone.txt  del temp\_work\busy_dev_microphone.txt

ping localhost -w 1000 -n 30 >nul
ECHO busy>temp\_work\busy_dev_microphone.txt



ECHO;
ECHO ja,azure,�J�������N�����܂����B�^�b�v����ƎB�e�ł��܂��B
PAUSE
ECHO ja,azure,�J�������N�����܂����B�^�b�v����ƎB�e�ł��܂��B>temp\a3_5tts_txt\speech50_sjis.txt
if exist temp\_work\busy_dev_display.txt  del temp\_work\busy_dev_display.txt



ping localhost -w 1000 -n 30 >nul
ECHO busy>temp\_work\busy_dev_display.txt



ECHO;
ECHO ja,azure,���O�I�t���܂����B
ECHO ja,azure,�莞���߂��Ă��܂��̂ŁA�ދΏ����������I�ɍs���܂����B
ECHO ja,azure,�����S�ɁB
PAUSE
ECHO ja,azure,���O�I�t���܂����B>temp\a3_5tts_txt\speech90_sjis.txt
ECHO ja,azure,�莞���߂��Ă��܂��̂ŁA�ދΏ����������I�ɍs���܂����B>temp\a3_5tts_txt\speech91_sjis.txt
ECHO ja,azure,�����S�ɁB>temp\a3_5tts_txt\speech92_sjis.txt

goto LOOP

exit
