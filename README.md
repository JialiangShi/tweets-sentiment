# Twitter sentiment analysis

The goal of this project is to learn how to pull twitter data, using the [tweepy](http://www.tweepy.org/) wrapper around the twitter API, and how to perform simple sentiment analysis using the [vaderSentiment](https://github.com/cjhutto/vaderSentiment) library.  The tweepy library hides all of the complexity necessary to handshake with Twitter's server for a secure connection.

We also produce a web server running at AWS to display the most recent 100 tweets from a given user and the list of users followed by a given user. For example, in response to URL `/realdonaldtrump`, your web server should respond with a tweet list color-coded by sentiment, using a red to green gradient:

<img src=figures/trump-tweets.png width=750>

Next you will create a page responding to URLs, such as `/following/realdonaldtrump`, that displays the list of users followed by a given user:

<img src=figures/trump-follows.png width=350>

### Authenticating with the twitter API server

Twitter requires that you register as a user and then also create an "app" for which Twitter will give you authentication credentials. These credentials are needed for making requests to the API server. Start by logging in to [twitter app management](https://apps.twitter.com/) then click on "create new app". 

For the website, you can link to your LinkedIn account or something or even your github account. Leave the "callback URL" blank.

Once you have created that app, go to that app page. Click on the  "Keys and Access Tokens" tabs, which shows 4 key pieces that represent your authentication information:

* Consumer Key (API Key)
* Consumer Secret (API Secret)
* Access Token
* Access Token Secret	

Under the Permissions tab, make sure that you have your access as "Read only" for this application. This prevents a bug in your software from doing something horrible to your twitter account!

### Mining for tweets

In file `tweetie.py` (pronounced "tweety pie", get it?) you will create methods to fetch a list of tweets for a given user and a list of users followed by a given user.  Function `fetch_tweets()` returns a dictionary containing:

* `user`: user's screen name
* `count`: number of tweets
* `tweets`: list of tweets

where each tweet is a dictionary containing:

* `id`: tweet ID
* `created`: tweet creation date
* `retweeted`: number of retweets
* `text`: text of the tweet
* `hashtags`: list of hashtags mentioned in the tweet
* `urls`: list of URLs mentioned in the tweet
* `mentions`: list of screen names mentioned in the tweet
* `score`: the "compound" polarity score from vader's `polarity_scores()`

Function `fetch_following()` returns a dictionary containing:

* `name`: user's real name
* `screen_name`: Twitter screen name (e.g., `the_antlr_guy`)
* `followers`: number of followers
* `created`: created date (no time info)
* `image`: the URL of the profile's image
       
This information is needed to generate the HTML for the two different kinds of pages.

## Launching your server at Amazon

When it comes to web server, we couldn't simply run it locally and expect a miracle. We need to launch a Linux instance at Amazon and install our software. 

Creating a server that has all the appropriate software can be tricky so I have recorded a sequence that works for me.

The first thing is to launch a server with different software than the simple  Amazon linux we have been using in class. We need one that has, for example, `numpy` and friends so let's use an *image* (snapshot of a disk with a bunch of stuff installed) that already has machine learning software installed: Use "*Ubuntu Server 16.04 LTS (HVM), SSD Volume Type*":

Create a `t2.medium` size computer (in Oregon; it's cheaper)!

When you try to connect, it will tell you to use user `root` but use `ec2-user` like we did for the other machines.  In other words, here's how I login:
 
```bash
$ ssh -i "mykey.pem" ec2-user@34.203.194.19
```

Then install software we need:

```bash
sudo apt update
sudo apt install python3-pip

pip3 install flask
pip3 install tweepy
pip3 install gunicorn
pip3 install vaderSentiment
pip3 install colour
```

Now, clone your repository into the home directory:

```bash
git clone https://github.com/JialiangShi/tweets-sentiment.git
cd tweets-sentiment
```

You should now be able to run your server:

```bash
$ gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log server:app twitter.csv
```

(Test without `-D` during development so that you can see errors generated by the server; otherwise they appear to be hidden.)

`twitter.csv` is the file with your credentials.

All output goes into `server.log`, even after you log out. The `-D` means put the server in daemon mode, which runs the background.

Don't forget to open up port 5000 in the firewall for the server so that the outside world can access it. Make sure that you test from your laptop!

Make sure the `IP.txt` file as the **public** IP address of your server with `:5000` on the line by itself, such as `54.198.43.135:5000`!

