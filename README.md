# youdaodict
make a little change about youdaodict.
Using google translate in a popup window.
## run this program by using this command:
``` bash
./myYoudao.sh

```
## configuration file description
{
  "useTranslateModule": "true",
  "savePath": "/home/ubuntu/Desktop",
  "cmd": "translate -f en -t zh ",
  "toLang":"zh"
}
useTranslateModule: Use google translate: True/False
savePath: Path to save words that you want to review, it will be named to translate.csv, eg: /home/ubuntu/Desktop/translate.csv
cmd: It is not used now
toLang: The target language you want to translate, 'zh' for chinese
## details
visit [my blog](https://makeitpossible16.github.io/%E6%9C%89%E9%81%93%E5%AD%97%E5%85%B8%E4%BF%AE%E6%94%B9/ubuntu%E4%B8%8B%E5%A6%82%E4%BD%95%E4%BC%98%E9%9B%85%E5%9C%B0%E4%BD%BF%E7%94%A8%E7%BF%BB%E8%AF%91/) for more details.
