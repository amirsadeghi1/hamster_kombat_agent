@echo off
:loop
(
echo n
echo n
echo n
echo n
echo n
) | python hamster.py
if %errorlevel% neq 0 (
    echo ^[[33m...
)
goto loop