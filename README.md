# ssad_alimtalk

## 개발환경

* Python 3.7.0

## 개발환경 설정

```shell
$ pyenv shell 3.7.0
$ mkvirtualenv ssad
$ workon ssad
$ pip install -r requirements.pip
```

## cron 설정하기

cron에 `ssad_alimtalk`을 등록하여 동작시키기 위해서는 다음 두가지 조건을 만족해야한다.

1. `ssad_alimtalk`은 `가상환경`을 사용하기 때문에 cron에서 이를 사용하기위해 `가상환경`디렉토리의 `python`파일을 사용해야한다. 
2. 월 ~ 금요일까지 오후 3시40분에 `ssad_alimtalk`이 동작해야하므로 이에대한 설정이 필요하다.
3. cron에 등록 된 `ssad_alimtalk`의 성공/실패에 대한 로그가 남아야한다.

```shell
$ export EDITOR=vim; crontab -e
45 15 * * 1-5 export SLACK_INCOMING_HOOK="slack incoming web hook url"; /Users/greenfrog/.virtualenvs/ssad/bin/python3.7 /Users/greenfrog/develop/ssad_alimtalk/src/main.py 2> /Users/greenfrog/ssad_alimtalk_failure.log 1> /Users/greenfrog/ssad_alimtalk_success.log 
```


## Reference(s)

* [KaKaoDevelopers - 로그인](https://developers.kakao.com/docs/restapi/user-management#%EB%A1%9C%EA%B7%B8%EC%9D%B8)
* [crontab guru](https://crontab.guru/#41_15_*_*_1-5)
