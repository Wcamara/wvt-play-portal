# WVT Play Portal

Portal independente do `radar-saas` para testar o fluxo de Device Key e cadastro de playlists.

## Teste local

```bash
cd /home/vangogh/Documents/wvt-play-portal
python3 -m http.server 8787
```

Abra `http://127.0.0.1:8787`, informe qualquer Device Key e PIN de teste e cadastre uma URL M3U ou Xtream. Esta primeira versão usa `localStorage` apenas para validar a experiência; a próxima etapa troca o armazenamento por uma API/Banco separado antes da publicação no GitHub Pages.
