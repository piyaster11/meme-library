# Meme Library · คลังมีม
Mockup meme library (personal use). Live: https://piyaster11.github.io/meme-library/

## Add a meme
1. Put the image in `img/` (jpg/webp, max ~800px).
2. Add an entry to `data/memes.json`:
```json
{"id":"my-meme","name":"My Meme","name_th":"มีมของฉัน","tags":["funny","ตลก"],"occasions":["work","friday"],"rank":81,"img":"img/my-meme.jpg","source":"where it came from"}
```
Occasion keys: work, monday, friday, payday, broke, birthday, thanks, sorry, love, food, sad, happy, shocked, agree, disagree, songkran, newyear, loykrathong.
3. Commit & push to `gh-pages`.

Credits: templates via Imgflip popular templates; images belong to their owners; tags are our own labels.
