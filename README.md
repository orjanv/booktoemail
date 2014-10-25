## booktoemail
booktoemail.sh is a bash utility to download the ascii version of a book and find haikus in it using the [findhaikus](https://github.com/jdf/haikufinder "findhaikus") program. The script takes 2 arguments

```bash
$ ./booktoemail.sh http://www.gutenberg.org/files/2591/2591.txt user@host.com
```

## booktoblog
booktoblog is a bash utility like that blogs the haikus found to a blogger blog using the googlecl tool. It also uses the findhaikus utility as the booktoemail.sh script does.

```bash
$ booktoblog.sh filename
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
0 7 * * * cd /path/to/your/script; ./booktoblog.sh filename
```

