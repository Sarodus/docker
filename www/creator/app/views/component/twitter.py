import twitter

from ...extensions import cache
from . import Component


class Twitter(Component):

    type = 'twitter'

    default_config = dict(
        exclude_replies = True,
        count = 100,
    )


    @classmethod
    def register(cls, app):
        super(Twitter, cls).register(app)
        cls.api = twitter.Api(consumer_key=app.config['TWITTER_CONSUMER_KEY'],
                              consumer_secret=app.config['TWITTER_CONSUMER_SECRET'],
                              access_token_key=app.config['TWITTER_ACCESS_TOKEN_KEY'],
                              access_token_secret=app.config['TWITTER_ACCESS_TOKEN_SECRET'])

    def __repr__(self):
        return '<ComponentTwitter>'


    def index(self):
        return self._render_template('wrapper.html', body=self._default())


    def _index(self):
        account_id = self.config.get('account_id')

        user = self._get_user(user_id = account_id)
        timeline = self._get_timeline(user_id = account_id,
                                      count=self.config['count'],
                                      exclude_replies=self.config['exclude_replies'])

        return self._render_template('twitter/feed.html',
            user = user,
            tweets = timeline
        )


    @classmethod
    @cache.memoize()
    def _get_user(cls, **kwargs):
        return cls.api.GetUser(**kwargs)

    @classmethod
    @cache.memoize()
    def _get_timeline(cls, **kwargs):
        return cls.api.GetUserTimeline(**kwargs)
