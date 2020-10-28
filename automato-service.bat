@echo off
cmd /k "cd /d %CD%\back\ENV\Scripts\ & activate & cd /d  %CD%\back & python .\ENV\Lib\site-packages\huey\bin\huey_consumer.py tasks.huey"