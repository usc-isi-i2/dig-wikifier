# Setting up redis on your server
The most straightforward way to setup redis on your Linux/CentOS server is to do the following -
```
1. wget http://download.redis.io/redis-stable.tar.gz
2. tar xvzf redis-stable.tar.gz
3. cd redis-stable
4. make
```


Once these steps are complete copy [this](https://github.com/usc-isi-i2/dig-wikifier/blob/master/redis/redis-5.0.0/config/6379.conf) file into the redis folder
and then try to run redis server as follows -

```
nohup redis-5.0.0/src/redis-server path/to/6379.conf &
```

That should vary depending on the version of TAR file you download from the server. Please change the command accordingly. This should generally work on most
CentOS and Linux systems and get you started. If you face issues however please refer to the official documentation [here](https://redis.io/topics/quickstart)

**Note: You do not require any extensive setup of redis, except enabling BGSAVE (background save) So following any REDIS quickstart tutorial should help you get the redis server setup**
