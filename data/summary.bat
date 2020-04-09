cd "activities"
FOR /F "delims=|" %%I IN ('DIR "*" /B /O:D') DO SET NewestFile=%%I
cd %NewestFile%
start summary.txt