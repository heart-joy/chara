mkdir output

for %%f in (*.jpg) do (
    ffmpeg -y -i "%%f" ^
    -vf "crop=min(iw\,ih):min(iw\,ih),scale=640:640" ^
    "output\%%~nxf"
)