
## Links

https://gemini.google.com/app/317e021ca463bccb

## Audio wave to mp3


```
ffmpeg -i input.wav output.mp3
```

## Setup 

```
# Instalacja głównej biblioteki Whisper
pip install -U openai-whisper

# Instalacja pakietu do szybszej transkrypcji
pip install setuptools-rust

# it is already added to my conda env 
conda env list 
conda activate python312
```

## Running 


```
python transkrypcja.py 
```
