Bot to grab reference art from twitter
======================================

Usage
-----
With docker
^^^^^^^^^^^
- Edit environment variables
- Build docker file with `docker build -t pytwitloader .`
- Run container while mounting an empty data directory: `docker run -v /local/data/dir:/data pytwit` 

TODO
----
- Figure out why there's a filesize error
- Be able to specify minimum date value (download everything past date x)
- Rewrite get_liked_tweets() as a generator
- Parallelize this