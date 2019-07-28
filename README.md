# Programming vacancies compare

These is script which calculates rating of salaries in hh.ru and superjob.ru and used their API.

Example of result:

```
+SuperJob Moscow----------+-----------------+---------------------+----------------+
| Language of programming | Vacancies found | Vacancies processed | Average salary |
+-------------------------+-----------------+---------------------+----------------+
| 1C                      | 110             | 69                  | 111101         |
| C                       | 18              | 8                   | 119858         |
| C#                      | 25              | 16                  | 103478         |
| C++                     | 28              | 16                  | 109116         |
| Delphi                  | 11              | 8                   | 114937         |
| Java                    | 22              | 14                  | 131474         |
| JavaScript              | 57              | 40                  | 104592         |
| PHP                     | 47              | 33                  | 105140         |
| PL/SQL                  | 8               | 5                   | 102300         |
| Python                  | 13              | 7                   | 110477         |
+-------------------------+-----------------+---------------------+----------------+

+HeadHunter Moscow--------+-----------------+---------------------+----------------+
| Language of programming | Vacancies found | Vacancies processed | Average salary |
+-------------------------+-----------------+---------------------+----------------+
| 1C                      | 1436            | 638                 | 124777         |
| C                       | 1543            | 516                 | 145443         |
| C#                      | 1032            | 276                 | 146742         |
| C++                     | 1005            | 285                 | 152644         |
| Delphi                  | 107             | 49                  | 118240         |
| Java                    | 1855            | 415                 | 172666         |
| JavaScript              | 2000            | 710                 | 139174         |
| Kotlin                  | 306             | 91                  | 191068         |
| Objective-C             | 164             | 54                  | 177648         |
| Perl                    | 135             | 36                  | 133236         |
| PHP                     | 1084            | 516                 | 124741         |
| PL/SQL                  | 455             | 78                  | 147144         |
| Python                  | 1522            | 360                 | 149382         |
| R                       | 314             | 75                  | 156465         |
| Ruby                    | 216             | 70                  | 160071         |
| Scala                   | 222             | 37                  | 207770         |
| Solidity                | 345             | 94                  | 168379         |
| Swift                   | 250             | 81                  | 173316         |
| Bash                    | 385             | 82                  | 156978         |
| Go                      | 316             | 78                  | 180096         |
| Shell                   | 154             | 26                  | 166134         |
| TypeScript              | 414             | 138                 | 168156         |
+-------------------------+-----------------+---------------------+----------------+
```

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
