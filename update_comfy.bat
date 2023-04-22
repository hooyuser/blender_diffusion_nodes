@echo off
set source=..\ComfyUI\comfy
set destination=comfy

if not exist %destination% (
  mkdir %destination%
)

xcopy /s/e/v/y %source% %destination%