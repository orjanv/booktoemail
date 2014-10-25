## booktoemail
booktoemail.sh is a bash utility to download the ascii version of a book and find haikus in it using the [haikufinder](https://github.com/jdf/haikufinder "haikufinder") program and NLTK toolkit. The script takes two arguments:

```bash
$ ./booktoemail.sh http://www.gutenberg.org/files/2591/2591.txt user@host.com
```

## booktoblog
booktoblog is a bash utility like that blogs the haikus found to a blogger blog using the googlecl tool. It also uses the findhaikus utility as the booktoemail.sh script does. The script takes one argument:

```bash
$ booktoblog.sh samplenumbers.txt
```

#### Crontab
Make your script run daily with crontab

```bash
$ crontab -e
```

Add a line as follows

```bash
# 
# m h  dom mon dow   command
0 7 * * * cd /path/to/your/script; ./booktoblog.sh samplenumbers.txt
```

