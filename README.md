# Programming vacancies compare

These is script which calculates rating of salaries in hh.ru and superjob.ru and used their API.

### How to install

You need to create `.env` file and write in file parameter `SJ_SECRET_KEY`. These is secret key for SuperJob API.

You can get these secret key in [SuperJob API page](https://api.superjob.ru/). You must register your app in SuperJob.

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### How to use

Open command line (in windows `Win+R` and write `cmd` and `Ok`). Go to directory with program or just write in cmd:

`python <PATH TO PROGRAM>\programming_vacancies_ratings.py `

### References

[HeadHunter API](https://github.com/hhru/api/blob/master/docs_eng/README.md).

[SuperJob API](https://api.superjob.ru/).

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
