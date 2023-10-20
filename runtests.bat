@echo off
for %%f in (tests\*.html) do (
  echo Converting "%%~nf.html" to "%%~nf.md"
  python mubu_converter.py < "%%~f" > "tests\%%~nf.md"
)
echo Conversion complete.
pause